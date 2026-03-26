from flask import Blueprint, redirect, url_for

from render.builder.application import Application
from render.builder.menu import MenuItem
from render.www.applications.home.viewmodels.vm_home import VMHome


class Home(Application):
    def declare_bp(self):
        bp = Blueprint("home", self.__class__.__module__, url_prefix="/home", template_folder="templates",
                       static_folder="static")
        return bp

    def init_menu(self):
        self.menu.add_item(MenuItem(name="Home", controller="VMHome.index", category="Home"))

    def init_view_model(self):
        VMHome().register(self.bp)

    def routes(self):
        self.bp.route("/")(self.index)

    def index(self):
        return redirect(url_for(f"{self.bp.name}.VMHome.index"))
