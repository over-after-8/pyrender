from flask_login import LoginManager

from render.models.user import User
from render.www import auth
from render.www.admin import Admin
from render.www.utils import path_for


def create_app(app, applications):
    app.register_blueprint(auth.bp)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    admin = Admin("AdminZone")

    applications.append(admin)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @app.context_processor
    def utility_processor():
        def inject_applications():
            return applications

        return dict(inject_applications=inject_applications, path_for=path_for)

    for application in applications:
        application.register()
        app.register_blueprint(application.bp)
    return app
