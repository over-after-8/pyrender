from flask_login import LoginManager

from render.models.permission import Permission
from render.models.role import Role
from render.models.user import User
from render.www import auth, admin
from render.www.views.permission_view_model import PermissionViewModel
from render.www.views.role_view_model import RoleViewModel
from render.www.views.user_view_model import UserViewModel


def create_app(app):
    app.register_blueprint(auth.bp)
    # app.register_blueprint(admin.bp)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    UserViewModel(User).register(admin.bp)
    RoleViewModel(Role).register(admin.bp)
    PermissionViewModel(Permission).register(admin.bp)

    app.register_blueprint(admin.bp)
    return app
