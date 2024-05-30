from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint("admin", __name__, url_prefix="/admin", template_folder="templates/render/admin",
               static_folder="static/render")


@bp.route("/")
@login_required
def index():
    return render_template("admin_index.html", title="Admin Page"), 200
