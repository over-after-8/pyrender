from flask import Flask
from flask_login import LoginManager

from render.models.user import User
from render.www import auth


def create_app(app):
    app.register_blueprint(auth.bp)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    return app
