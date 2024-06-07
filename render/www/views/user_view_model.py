import json

from flask import request, url_for, render_template, redirect
from flask_login import login_required, current_user

from render.builder.utils import outside_url_for
from render.builder.viewmodel import ViewModel
from render.models.user import User


class UserViewModel(ViewModel):
    list_fields = ["id", "user_name", "full_name", "roles", "is_active", "created_at", "updated_at"]
    search_fields = ["user_name", "full_name"]
    add_fields = ["user_name", "full_name", "password", "is_active"]
    show_fields = ["user_name", "full_name", "is_active", "roles", "created_at", "updated_at"]
    edit_fields = ["full_name", "is_active", "roles"]
    disabled_edit_fields = ["user_name"]
    add_url_func = outside_url_for(".user_add")

    actions = {
        "change_password": outside_url_for(".user_change_password")
    }

    def register(self, flask_app_or_bp):
        self.bp.route("/<int:item_id>/user_change_password", methods=["GET", "POST"])(self.user_change_password)
        self.bp.route("/user_add", methods=["GET", "POST"])(self.user_add)
        super().register(flask_app_or_bp)

    @login_required
    def user_change_password(self, item_id):
        if request.method == "GET":
            user_item = User.get(item_id)
            res = {
                "user_name": user_item.user_name,
                "submit_url": url_for(".user_change_password", item_id=item_id)
            }
            return render_template("render/admin/user_change_password.html",
                                   title="Change Password",
                                   model=json.dumps(res)), 200
        else:
            password = request.json.get("password", None)
            User.update_password(item_id, password)
            return json.dumps({"status": "success"}), 200

    @login_required
    def user_add(self):
        if request.method == "GET":
            return render_template("render/admin/user_add.html", title="Add User"), 200
        else:
            user_name = request.form.get("user_name", None)
            password = request.form.get("password", None)
            if user_name is None or password is None:
                return json.dumps({"status": "failed"}), 400
            User.add(user_name, password, current_user.id)
            return redirect(self.list_view_model.search_url_func())
