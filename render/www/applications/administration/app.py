from flask import Blueprint, redirect, url_for
from flask_login import login_required

from render.builder.application import Application
from render.builder.menu import MenuItem
from render.models.user import User, Module
from render.www.applications.administration.viewmodels.vm_module import VMModule
from render.www.applications.administration.viewmodels.vm_user import VMUser


class Administration(Application):
    def declare_bp(self):
        bp = Blueprint("admin", self.__class__.__module__, url_prefix="/admin", template_folder="templates",
                       static_folder="static")
        return bp

    def init_menu(self):
        self.menu.add_item(MenuItem(name="User", controller="VMUser.list_items", category="Securities"))
        self.menu.add_item(MenuItem(name="Module", controller="VMModule.list_items", category="Securities"))

    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def init_view_model(self):
        VMUser(User).register(self.bp)
        VMModule(Module).register(self.bp)

    def routes(self):
        self.bp.route("/")(self.index)

    @login_required
    def index(self):
        return redirect(url_for(f"{self.bp.name}.VMUser.list_items"))
