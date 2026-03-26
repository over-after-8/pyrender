from flask import render_template
from flask_login import login_required

from render.builder.viewmodel import EmptyViewModel


class VMHome(EmptyViewModel):

    @login_required
    def index(self):
        return render_template("home.html")

    def register(self, flask_app_or_bp):
        super().register(flask_app_or_bp)
        self.bp.route("/", methods=["GET"])(self.index)
