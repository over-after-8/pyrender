from functools import reduce

from flask import Blueprint, render_template
from flask_login import login_required

from render.builder.utils import outside_url_for
from render.models.permission import Permission
from render.models.role import Role
from render.models.user import User
from render.www.views.permission_view_model import PermissionViewModel
from render.www.views.role_view_model import RoleViewModel
from render.www.views.user_view_model import UserViewModel


class Menu:

    def __init__(self, root):
        self.root = root
        self.items = []

    def add_item(self, menu_item):
        self.items.append(menu_item)

    def get(self):
        # TODO check permissions

        def update_res(res, item):
            if item.category not in res:
                res[item.category] = []
            item.url = outside_url_for(f"{self.root}.{item.controller}")()
            res[item.category].append(item)
            return res

        return reduce(lambda r, x: update_res(r, x), self.items, {})


class MenuItem:
    def __init__(self, controller, name=None, category="no_grouped", icon=None):
        self.category = category
        self.name = name or controller
        self.controller = controller
        self.icon = icon
        self.url = None


class Application:

    def declare_bp(self) -> Blueprint:
        pass

    def __init__(self, name):
        self.name = name
        self.bp = self.declare_bp()
        self.menu = Menu(self.bp.name)

    def get_menu(self):
        self.menu.get()

    def menu_add(self, menu_item):
        self.menu.add_item(menu_item)

    def init_menu(self):
        pass

    def register(self):
        self.init_view_model()
        self.init_menu()

        self.bp.context_processor(lambda: self.utility_process())
        self.routes()

    def init_view_model(self):
        pass

    def utility_process(self):
        def inject_menu():
            return self.menu.get()

        return dict(inject_menu=inject_menu)

    def routes(self):
        pass


class Admin(Application):

    def declare_bp(self):
        bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder="templates/render/admin",
                       static_folder="static/render")
        return bp

    def init_menu(self):
        self.menu.add_item(MenuItem(name="User", controller="UserViewModel.list_items", category="Securities"))
        self.menu.add_item(MenuItem(name="Role", controller="RoleViewModel.list_items", category="Securities"))
        self.menu.add_item(
            MenuItem(name="Permission", controller="PermissionViewModel.list_items", category="Securities"))

    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def init_view_model(self):
        UserViewModel(User).register(self.bp)
        RoleViewModel(Role).register(self.bp)
        PermissionViewModel(Permission).register(self.bp)

    def routes(self):
        self.bp.route("/")(self.index)

    @login_required
    def index(self):
        return render_template("admin_index.html", title="Admin Page"), 200
