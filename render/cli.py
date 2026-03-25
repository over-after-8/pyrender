import logging

import click
from flask import Flask

from render.www.app import create_app

logger = logging.getLogger(__name__)





#
#
# @provide_session
# def init_applications(user, session=None):
#     from render.www.admin import admin_application
#
#     applications = [admin_application]
#     application_objects = list(
#         map(lambda x: Module(name=x.name, created_by=user.id, class_name=fullname(x.__class__)), applications))
#     for a in application_objects:
#         session.add(a)
#
#     update_user = session.query(User).filter(User.id == user.id).one_or_none()
#     update_user.modules = application_objects
#     session.add(update_user)
#
#
# @provide_session
# def init_roles(user, session=None):
#     view_model_classes = list(map(lambda x: x.__name__, inheritors(ViewModel)))
#     base_roles = {
#         "user",
#         "editor",
#         "viewer"
#     }
#
#     def add_roles(roles):
#         for role in roles:
#             session.add(role)
#             session.commit()
#
#     def permissions(vmc, perms):
#         res = [session.query(Permission).filter(Permission.name == f"{vmc.lower()}.{p}").one_or_none()
#                for p in perms]
#         return res
#
#     user_roles = [Role(name=f"{vmc.lower()}.user", created_by=user.id,
#                        permissions=permissions(vmc, {"add", "edit", "delete", "list"}))
#                   for vmc in view_model_classes]
#
#     editor_roles = [Role(name=f"{vmc.lower()}.editor", created_by=user.id,
#                          permissions=permissions(vmc, {"edit.all", "add", "delete.all", "list.all"}))
#                     for vmc in view_model_classes]
#
#     viewer_roles = [
#         Role(name=f"{vmc.lower()}.viewer", created_by=user.id, permissions=permissions(vmc, {"list.all"}))
#         for vmc in view_model_classes]
#
#     add_roles(user_roles + editor_roles + viewer_roles)
#     update_user = session.query(User).filter(User.id == user.id).one_or_none()
#     update_user.roles = user_roles + editor_roles + viewer_roles
#     session.add(update_user)
#
#
# @provide_session
# def init_permissions(user, session=None):
#     view_model_classes = map(lambda x: x.__name__, inheritors(ViewModel))
#     base_permissions = {
#         "edit.all",
#         "delete.all",
#         "edit",
#         "delete",
#         "add",
#         "list",
#         "list.all"
#     }
#
#     def add_permissions(perms):
#         session.bulk_save_objects(perms)
#
#     permissions = [Permission(name=f"{vmc.lower()}.{p}", created_by=user.id) for vmc in view_model_classes for p in
#                    base_permissions]
#     add_permissions(permissions)
#
#
# @provide_session
# def init_db(session=None):
#     from render.models.user import User
#     from sqlalchemy.exc import OperationalError
#
#     try:
#         User.add("a@mail.com", "a", 1)
#         user = session.query(User).filter(User.user_name == "a@mail.com").one_or_none()
#         profile = UserProfile(name=user.user_name, id=user.id)
#         session.add(profile)
#
#         init_permissions(user, session=session)
#         init_roles(user, session=session)
#         init_applications(user, session=session)
#
#     except OperationalError as e:
#         logger.error(e)
#         raise e


@click.group()
def cli():
    pass


@cli.group()
def db():
    pass


@cli.group()
def webserver():
    pass


@cli.group()
def admin():
    pass


@admin.command("create-user")
@click.argument("user_name")
@click.argument("password")
def create_user(user_name, password):
    from render.services.admin.password_manager import PasswordManager
    from render.services.admin.user_service import UserService

    user_service = UserService(PasswordManager())
    user_service.create_user(user_name, password)


@webserver.command("start")
def webserver_start():
    app = Flask(__name__)
    app = create_app(app, [])
    app.run(host="0.0.0.0", port=5000)


@cli.command()
def version():
    print("Hello")
