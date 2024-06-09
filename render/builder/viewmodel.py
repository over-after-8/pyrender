import json
from functools import reduce, wraps

from flask import Blueprint, render_template, request, redirect, abort
from flask_login import login_required, current_user
from sqlalchemy import and_

from render.builder.utils import outside_url_for, is_relationship, relationship_class
from render.utils.db import provide_session


class SubViewModel:
    def __init__(self, view_model_class):
        self.view_model_class = view_model_class
        self.register()

    def register(self):
        pass


class Field:
    def __init__(self, name, _type):
        self.name = name
        self.type = _type

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type
        }


class AddViewModel(SubViewModel):
    add_fields = []
    field_types = {}
    model_class = None

    def register(self):
        self.model_class = self.view_model_class.model_class
        self.add_fields = self.view_model_class.add_fields

    def to_dict(self):
        fields = map(
            lambda field_name: Field(field_name, type(getattr(self.model_class, field_name).type).__name__).to_dict(),
            self.add_fields)

        return {
            "fields": list(fields)
        }


class EditViewModel(SubViewModel):
    disabled_edit_fields = []
    edit_fields = []
    item = None
    model_class = None

    def register(self):
        self.model_class = self.view_model_class.model_class
        self.edit_fields = self.view_model_class.edit_fields
        self.disabled_edit_fields = self.view_model_class.disabled_edit_fields

    def to_dict(self, session=None):
        item = {}
        relationships = {}

        for field in [*self.edit_fields, *self.disabled_edit_fields]:
            if is_relationship(self.model_class, field):
                item[field] = [list(map(lambda x: x.to_dict(session), getattr(self.item, field))), "Relationship"]
                model_relationship = relationship_class(self.model_class, field)
                relationships[field] = relationship_data(model_relationship, session)
            else:
                item[field] = [getattr(self.item, field), type(getattr(self.model_class, field).type).__name__]

        return {
            "relationships": relationships,
            "disabled_fields": self.disabled_edit_fields,
            "edit_fields": self.edit_fields,
            "item": item
        }


class DetailViewModel(SubViewModel):
    actions = {}
    show_fields = []
    item = None
    model_class = None

    def register(self):
        self.model_class = self.view_model_class.model_class
        self.show_fields = self.view_model_class.show_fields
        self.actions = self.view_model_class.actions

    def map_item(self):
        res = {}
        for field in self.show_fields:
            res[field] = getattr(self.item, field)
        return res

    def to_dict(self):
        acts = {}
        for act in self.actions:
            acts[act] = self.actions[act](item_id=self.item.id)

        field_types = {}
        for field in self.show_fields:
            if is_relationship(self.model_class, field):
                field_types[field] = "Relationship"
            else:
                field_types[field] = type(getattr(self.model_class, field).type).__name__

        return {
            "actions": acts,
            "show_fields": self.show_fields,
            "field_types": field_types,
            "item": self.map_item()
        }


@provide_session
def permissions_by_user(user_id, session=None):
    res = reduce(lambda r, x: r + x.permissions, current_user.roles, [])
    return res


@provide_session
def owned_by(model_class, item_id, session=None):
    res = session.query(model_class).filter(
        and_(model_class.id == item_id, model_class.created_by == current_user.id)).one_or_none()
    return bool(res)


def check_permission(permission):
    def check_func(func):

        if "item_id" in func.__code__.co_varnames:
            @wraps(func)
            def wrap_func(self_object, item_id, *args, **kwargs):
                view_model_name = self_object.__class__.__name__
                required_permission = f"{view_model_name.lower()}.{permission}"
                permissions = permissions_by_user(current_user.id)
                all_permission = list(
                    filter(lambda x: required_permission in x.name and x.name.endswith(".all"), permissions))
                if all_permission:
                    return func(self_object, item_id, *args, **kwargs)

                existed_permission = list(filter(lambda x: required_permission in x.name, permissions))
                if existed_permission:
                    if owned_by(self_object.model_class, item_id):
                        return func(self_object, item_id, *args, **kwargs)
                    else:
                        return abort(403)
                return abort(403)

            return wrap_func
        else:
            @wraps(func)
            def wrap(self_object, *args, **kwargs):
                view_model_name = self_object.__class__.__name__
                required_permission = f"{view_model_name.lower()}.{permission}"
                permissions = permissions_by_user(current_user.id)

                all_permission = list(
                    filter(lambda x: required_permission in x.name and x.name.endswith(".all"), permissions))
                if all_permission:
                    return func(self_object, None, *args, **kwargs)

                existed_permission = list(filter(lambda x: required_permission in x.name, permissions))
                if existed_permission:
                    return func(self_object, current_user.id, *args, **kwargs)
                return abort(403)

            return wrap

    return check_func


@provide_session
def relationship_data(model_class, session=None):
    res = session.query(model_class).all()
    return list(map(lambda x: x.to_dict(session), res))


class ListViewModel(SubViewModel):
    list_fields = []
    field_types = {}
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

    list_template = ""
    detail_template = ""
    edit_template = ""
    delete_template = ""
    add_template = ""

    def __init__(self,
                 model_class,
                 add_view_model=AddViewModel,
                 edit_view_model=EditViewModel,
                 list_view_model=ListViewModel,
                 delete_view_model=DeleteViewModel,
                 detail_view_model=DetailViewModel,
                 list_template="render/list_view.html",
                 detail_template="render/detail_view.html",
                 edit_template="render/edit_view.html",
                 delete_template="render/delete_view.html",
                 add_template="render/add_view.html"):
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
        self.delete_view_model = delete_view_model(self)

        self.list_template = list_template
        self.detail_template = detail_template
        self.edit_template = edit_template
        self.delete_template = delete_template
        self.add_template = add_template

    def register(self, flask_app_or_bp):
        self.bp.route("/list", methods=["GET"])(self.list_items)
        self.bp.route("/add", methods=["GET", "POST"])(self.add_item)
        self.bp.route("/<int:item_id>", methods=["GET"])(self.detail_item)
        self.bp.route("/<int:item_id>/edit", methods=["GET", "POST"])(self.edit_item)
        self.bp.route("/<int:item_id>/delete", methods=["GET", "POST"])(self.delete_item)
        flask_app_or_bp.register_blueprint(self.bp)

    @login_required
    @provide_session
    @check_permission("list")
    def list_items(self, created_by, session=None):
        keyword = request.args.get("keyword", None)
        page = max(int(request.args.get("page", 1)), 1)
        page_size = int(request.args.get("page_size", 20))

        query = session.query(self.model_class)
        if keyword:
            query = query.filter(reduce(lambda r, x: r | x,
                                        [getattr(self.model_class, field).like(f"%{keyword}%") for field in
                                         self.search_fields]))

        if created_by:
            query = query.filter(self.model_class.created_by == created_by)

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
        return render_template(self.list_template, title=f"List {self.model_class.__name__}",
                               model=json.dumps(res.to_dict(), default=str)), 200

    @login_required
    @provide_session
    def add_item(self, session=None):
        if request.method == "GET":
            model = self.add_view_model
            return render_template(self.add_template, title=f"Add {self.model_class.__name__}",
                                   model=json.dumps(model.to_dict(), default=str)), 200
        else:
            kwargs = {}
            for field in self.add_fields:
                kwargs[field] = request.form.get(field, None)
                if "created_by" in dir(self.model_class):
                    kwargs["created_by"] = current_user.id
            item = self.model_class(**kwargs)
            session.add(item)
            return redirect(self.list_view_model.search_url_func()), 302

    @login_required
    @provide_session
    @check_permission("list")
    def detail_item(self, item_id, session=None):
        item = session.query(self.model_class).filter(self.model_class.id == item_id).one_or_none()
        if not item:
            return abort(404)
        res = self.detail_view_model
        res.item = item

        return render_template(self.detail_template, title=f"Detail {self.model_class.__name__}",
                               model=json.dumps(res.to_dict(), default=str)), 200

    @login_required
    @provide_session
    @check_permission("edit")
    def edit_item(self, item_id, session=None):
        if request.method == "GET":
            item = session.query(self.model_class).filter(self.model_class.id == item_id).one_or_none()
            model = self.edit_view_model
            model.edit_fields = self.edit_fields
            model.disabled_edit_fields = self.disabled_edit_fields
            model.item = item
            model_json = json.dumps(model.to_dict(session), default=str)
            return render_template(self.edit_template, title=f"Edit {self.model_class.__name__}",
                                   model=model_json), 200
        else:
            item = session.query(self.model_class).filter(self.model_class.id == item_id).one_or_none()
            for field in self.edit_fields:
                if field in self.disabled_edit_fields:
                    continue

                if is_relationship(self.model_class, field):
                    req_value = request.form.getlist(field)
                    rel_class = relationship_class(self.model_class, field)
                    value = session.query(rel_class).filter(rel_class.id.in_(req_value)).all()
                else:
                    value = request.form.get(field, None)
                    if type(getattr(self.model_class, field).type).__name__ == "Boolean":
                        value = bool(int(request.form.get(field, False)))
                setattr(item, field, value)
            session.add(item)
            return redirect(self.list_view_model.search_url_func()), 302

    @login_required
    @provide_session
    @check_permission("delete")
    def delete_item(self, item_id, session=None):
        item = session.query(self.model_class).filter(self.model_class.id == item_id).one_or_none()
        if request.method == "GET":
            item = session.query(self.model_class).filter(self.model_class.id == item_id).one_or_none()
            if not item:
                return abort(404)
            return render_template(self.delete_template, title=f"Delete {self.model_class.__name__}")
        else:
            session.delete(item)
            return redirect(self.list_view_model.search_url_func()), 302
