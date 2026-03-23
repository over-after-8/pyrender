from render.builder.utils import outside_url_for
from render.builder.viewmodel import ViewModel


class UserVM(ViewModel):
    list_fields = ["id", "user_name", "full_name", "roles", "modules", "is_active", "created_at", "updated_at"]
    search_fields = ["user_name", "full_name"]
    add_fields = ["user_name", "full_name", "password", "is_active"]
    show_fields = ["user_name", "full_name", "is_active", "roles", "modules", "created_at", "updated_at"]
    edit_fields = ["full_name", "is_active", "roles", "modules"]
    disabled_edit_fields = ["user_name"]
    add_url_func = outside_url_for(".user_add")

    # actions = {
    #     "change_password": outside_url_for(".user_change_password")
    # }

    # def register(self, flask_app_or_bp):
    #     self.bp.route("/<int:item_id>/user_change_password", methods=["GET", "POST"])(self.user_change_password)
    #     self.bp.route("/user_add", methods=["GET", "POST"])(self.user_add)
    #     super().register(flask_app_or_bp)
    #
    # @login_required
    # @check_permission("edit")
    # def user_change_password(self, item_id):
    #     if request.method == "GET":
    #         user_item = User.get(item_id)
    #         res = {
    #             "user_name": user_item.user_name,
    #             "submit_url": url_for(".user_change_password", item_id=item_id)
    #         }
    #         return render_template("admin/user_change_password.html",
    #                                title="Change Password",
    #                                model=json.dumps(res)), 200
    #     else:
    #         password = request.json.get("password", None)
    #         User.update_password(item_id, password)
    #         return json.dumps({"status": "success"}), 200
