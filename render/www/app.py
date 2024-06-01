from typing import List

from flask_login import LoginManager

from render.models.user import User
from render.www import auth
from render.www.admin import Admin, Application


def create_app(app):
    app.register_blueprint(auth.bp)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    admin = Admin("AdminZone")

    applications: List[Application] = [
        admin
    ]

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @app.context_processor
    def utility_processor():
        def inject_applications():
            return applications

        return dict(inject_applications=inject_applications)

    admin.register()
    app.register_blueprint(admin.bp)
    return app
