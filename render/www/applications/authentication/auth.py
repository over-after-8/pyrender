import json
import logging

from flask import Blueprint, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_login import login_user, login_required, logout_user

from render.exceptions.user_exceptions import PasswordMismatchError, UserNotFoundError
from render.services.admin.password_manager import PasswordManager
from render.services.admin.user_service import UserService

logger = logging.getLogger(__name__)

bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates", static_folder="static")

user_service = UserService(PasswordManager())


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html"), 200
    else:
        username = request.form["username"]
        password = request.form["password"]

        try:
            user = user_service.login(username, password)
            login_user(user)
            return redirect(url_for(".index"))
        except (PasswordMismatchError, UserNotFoundError) as e:
            logger.exception(e)
            flash("Invalid username or password")
            return render_template("login.html", title="Login",
                                   flashed_messages=json.dumps(get_flashed_messages())), 400


@bp.route("/login-success")
@login_required
def index():
    return "Login Success"


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
