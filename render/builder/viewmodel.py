import json
from functools import reduce

from sqlalchemy import inspect, cast, or_

from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from render.builder.utils import outside_url_for
from render.utils.db import provide_session


class SubViewModel:
    def __init__(self, view_model_class):
        self.view_model_class = view_model_class
        self.register()

    def register(self):
        pass


class AddViewModel(SubViewModel):
    pass


class EditViewModel(SubViewModel):
    pass


class DetailViewModel(SubViewModel):
    pass


def is_relationship(model_class, field):
    for rel in inspect(model_class).relationships:
        if rel.key == field:
            return True
    return False


class ListViewModel(SubViewModel):
    list_fields = []
    items = []

    search_url_func = None
    search_fields = []
    keyword = None

    detail_url_func = None
    edit_url_func = None
    add_url_func = None
    delete_url_func = None

    page = 1
    page_size = 20
    total = 0

    model_class = None

    def register(self):
        self.model_class = self.view_model_class.model_class
        self.list_fields = self.view_model_class.list_fields
        self.search_url_func = self.view_model_class.search_url_func
        self.search_fields = self.view_model_class.search_fields
        self.keyword = self.view_model_class.keyword
        self.detail_url_func = self.view_model_class.detail_url_func
        self.edit_url_func = self.view_model_class.edit_url_func
        self.add_url_func = self.view_model_class.add_url_func
        self.delete_url_func = self.view_model_class.delete_url_func
        self.page = self.view_model_class.page
        self.page_size = self.view_model_class.page_size
        self.total = self.view_model_class.total

    def map_item(self, item):
        item.detail_url = self.detail_url_func(item_id=item.id)
        item.edit_url = self.edit_url_func(item_id=item.id)
        item.delete_url = self.delete_url_func(item_id=item.id)
        res = {}
        for field in [*self.list_fields, "detail_url", "edit_url", "delete_url"]:
            res[field] = getattr(item, field)
        return res

    def to_dict(self):
        field_types = {}
        for field in self.list_fields:
            if is_relationship(self.model_class, field):
                field_types[field] = "Relationship"
            else:
                field_types[field] = type(getattr(self.model_class, field).type).__name__

        return {
            "add_url": self.add_url_func(),
            "list_fields": self.list_fields,
            "field_types": field_types,
            "items": list(map(lambda x: self.map_item(x), self.items)),
            "search_url": self.search_url_func(),
            "keyword": self.keyword,
            "page": self.page,
            "page_size": self.page_size,
            "total": self.total
        }


class DeleteViewModel(SubViewModel):
    pass


class ViewModel:
    model_class = None

    disabled_edit_fields = []
    edit_fields = []

    actions = {}
    show_fields = []
    search_fields = []
    add_fields = []

    item = None

    list_fields = []
    items = []
    search_url_func = None
    detail_url_func = None
    edit_url_func = None
    add_url_func = None
    delete_url_func = None
    keyword = None
    page = 1
    page_size = 20
    total = 0
    template_folder = "templates"
    static_folder = "static"

    bp: Blueprint = None
    list_view_model: ListViewModel = None

    def __init__(self, model_class, add_view_model=AddViewModel, edit_view_model=EditViewModel,
                 list_view_model=ListViewModel, delete_view_model=DeleteViewModel, detail_view_model=DetailViewModel):
        self.model_class = model_class
        self.__class__.bp = Blueprint(self.__class__.__name__, __name__,
                                      url_prefix=f'/{self.__class__.__name__}',
                                      template_folder=self.template_folder,
                                      static_folder=self.static_folder)

        self.add_url_func = self.add_url_func or outside_url_for(".add_item")

        self.search_url_func = outside_url_for(".list_items")
        self.detail_url_func = outside_url_for(".detail_item")
        self.edit_url_func = outside_url_for(".edit_item")
        self.delete_url_func = outside_url_for(".delete_item")

        self.list_view_model = list_view_model(self)
        self.add_view_model = add_view_model(self)
        self.edit_view_model = edit_view_model(self)
        self.detail_view_model = detail_view_model(self)

    def register(self, flask_app_or_bp):
        self.bp.route("/list", methods=["GET"])(self.list_items)
        self.bp.route("/add", methods=["GET", "POST"])(self.add_item)
        self.bp.route("/<int:item_id>", methods=["GET"])(self.detail_item)
        self.bp.route("/<int:item_id>/edit", methods=["GET", "POST"])(self.edit_item)
        self.bp.route("/<int:item_id>/delete", methods=["GET", "POST"])(self.delete_item)
        flask_app_or_bp.register_blueprint(self.bp)

    @login_required
    @provide_session
    def list_items(self, session=None):
        keyword = request.args.get("keyword", None)
        page = max(int(request.args.get("page", 1)), 1)
        page_size = int(request.args.get("page_size", 20))

        query = session.query(self.model_class)
        if keyword:
            query = query.filter(reduce(lambda r, x: r | x,
                                        [getattr(self.model_class, field).like(f"%{keyword}%") for field in
                                         self.search_fields]))

        if "owner_id" in dir(self.model_class):
            query = query.filter(
                or_(self.model_class.owner_id == current_user.id, self.model_class.permission.op('&')(0b100))
            )

        query = query.order_by(self.model_class.id.desc())
        total = query.count()
        query = query.offset((page - 1) * page_size).limit(page_size)
        items = query.all()

        res = self.list_view_model
        res.items = items
        res.keyword = keyword
        res.page = page
        res.page_size = page_size
        res.total = total
        return render_template("render/list_view.html", title=f"List {self.model_class.__name__}",
                               model=json.dumps(res.to_dict(), default=str)), 200

    def add_item(self):
        return "add_item"

    def detail_item(self):
        return "detail_item"

    def edit_item(self):
        return "edit_item"

    def delete_item(self):
        return "delete_item"
