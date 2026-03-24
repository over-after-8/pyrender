from flask import Blueprint, render_template
from flask_login import login_required

from render.builder.application import Application


class Index(Application):

    def declare_bp(self):
        bp = Blueprint("index", __name__, url_prefix="/index", template_folder="templates",
                       static_folder="static")
        return bp

    def init_menu(self):
        # self.menu.add_item(MenuItem(name="User", controller="UserVM.list_items", category="Securities"))
        pass

    def __init__(self, name):
        super().__init__(name)
        self.name = name

    def init_view_model(self):
        # UserVM(User).register(self.bp)
        pass

    def routes(self):
        self.bp.route("/")(self.index)

    @login_required
    def index(self):
        return render_template("admin/admin_index.html", title="Admin Page"), 200

