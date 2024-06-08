from flask import Blueprint, render_template
from flask_login import login_required

from render.builder.application import Application
from render.builder.menu import MenuItem
from render.models.module import Module
from render.models.permission import Permission
from render.models.role import Role
from render.models.user import User
from render.www.views.module_view_model import ModuleViewModel
from render.www.views.permission_view_model import PermissionViewModel
from render.www.views.role_view_model import RoleViewModel
from render.www.views.user_view_model import UserViewModel


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

        self.menu.add_item(MenuItem(name="Modules", controller="ModuleViewModel.list_items", category="Modules"))

    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def init_view_model(self):
        UserViewModel(User).register(self.bp)
        RoleViewModel(Role).register(self.bp)
        PermissionViewModel(Permission).register(self.bp)
        ModuleViewModel(Module).register(self.bp)

    def routes(self):
        self.bp.route("/")(self.index)

    @login_required
    def index(self):
        return render_template("admin_index.html", title="Admin Page"), 200


admin_application = Admin("AdminZone")
