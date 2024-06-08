from functools import reduce

from flask_login import LoginManager

from render.models.module import Module
from render.models.user import User
from render.utils.db import provide_session
from render.www import auth
from render.www.admin import admin_application
from render.www.utils import path_for


def get_class(class_name):
    from importlib import import_module

    try:
        module_path, class_name = class_name.rsplit('.', 1)
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        raise ImportError(class_name)


def create_app(app, applications):
    app.register_blueprint(auth.bp)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    applications.append(admin_application)

    @login_manager.user_loader
    @provide_session
    def load_user(user_id, session=None):
        user = session.query(User).filter(User.id == user_id).one_or_none()
        roles = user.roles
        permissions = reduce(lambda r, x: r + x.permissions, roles, [])
        modules = user.modules
        return user

    @app.context_processor
    def utility_processor():
        @provide_session
        def load_application_by_user(user_id, session=None):
            user = session.query(User).filter(User.id == user_id).one_or_none()
            return [get_class(x.class_name)(x.name) for x in user.modules]

        def inject_applications(user_id):
            return load_application_by_user(user_id)

        return dict(inject_applications=inject_applications, path_for=path_for)

    for application in applications:
        application.register()
        app.register_blueprint(application.bp)
    return app
