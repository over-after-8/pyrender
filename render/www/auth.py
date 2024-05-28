import json

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, get_flashed_messages
from flask_login import login_user, login_required, logout_user

from render.models.user import User

bp = Blueprint("auth", __name__, url_prefix="/auth", template_folder="templates", static_folder="static")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("render/auth/login.html"), 200
    else:
        username = request.form["email"]
        password = request.form["password"]

        user = User.get_by_user_name_password(username, password)
        if user:
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password")
            return render_template("render/auth/login.html", title="Login",
                                   flashed_messages=json.dumps(get_flashed_messages())), 400


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("render/auth/register.html", title="Register",
                               flashed_messages=json.dumps(get_flashed_messages())), 200
    else:
        username = request.form["email"]
        password = request.form["password"]
        repeat_password = request.form["repeatPassword"]

        if password != repeat_password:
            flash("passwords are not match")
            return render_template("render/auth/register.html", title="Register",
                                   flashed_messages=json.dumps(get_flashed_messages())), 400
        if password == repeat_password:
            res = User.add(user_name=username, password=password)
            if res:
                flash("there is an error, please register again or contact administrator")
                return redirect(url_for("auth.register")), 308
            else:
                return redirect(url_for("auth.login"))
