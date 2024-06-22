import argparse
import logging

import celery

from render.builder.utils import inheritors
from render.builder.viewmodel import ViewModel
from render.models.job import JobRun
from render.models.module import user_modules, Module
from render.models.permission import Permission
from render.models.role import Role, role_permissions
from render.models.user import User
from render.models.user_profile import UserProfile
from render.models.job import Job
from render.utils.config import config
from render.utils.db import provide_session
from render.worker.celery_worker import CeleryWorker

from render.www.views.role_view_model import RoleVM
from render.www.views.user_view_model import UserVM
from render.www.views.permission_view_model import PermissionVM
from render.www.views.module_view_model import ModuleVM
from render.www.views.user_profile_view_model import UserProfileVM
from render.www.views.job_vm import JobVM
from render.www.views.job_run_vm import JobRunVM

logger = logging.getLogger(__name__)


class Parser:
    def add_to_parser(self, parser):
        raise NotImplementedError()


class SubApp(Parser):
    def __init__(self, name, commands):
        super().__init__()
        self.name = name
        self.commands = commands

    def add_to_parser(self, parser):
        app_parser = parser.add_parser(self.name)
        sub_proc = app_parser.add_subparsers(help="a command")
        for command in self.commands:
            command.add_to_parser(sub_proc)


class Command(Parser):
    def __init__(self, func, args):
        super().__init__()
        self.func = func
        self.args = args

    def add_to_parser(self, parser):
        command_parser = parser.add_parser(self.func.__name__)
        command_parser.set_defaults(func=self.func)
        for arg in self.args:
            arg.add_to_parser(command_parser)


class Arg:
    def __init__(self, flags=None, help=None, action=None, default=None, required=None):
        self.flags = flags
        self.kwargs = {}
        for k, v in locals().items():
            if v is None:
                continue
            if k in ("self", "flags"):
                continue
            self.kwargs[k] = v

    def add_to_parser(self, parser):
        parser.add_argument(*self.flags, **self.kwargs)


def version(arg):
    from render.version import version as v
    print(v)


def fullname(klass):
    module = klass.__module__
    if module == 'builtins':
        return klass.__qualname__
    return module + '.' + klass.__qualname__


@provide_session
def init_applications(user, session=None):
    from render.www.admin import admin_application

    applications = [admin_application]
    application_objects = list(
        map(lambda x: Module(name=x.name, created_by=user.id, class_name=fullname(x.__class__)), applications))
    for a in application_objects:
        session.add(a)

    update_user = session.query(User).filter(User.id == user.id).one_or_none()
    update_user.modules = application_objects
    session.add(update_user)


@provide_session
def init_roles(user, session=None):
    view_model_classes = list(map(lambda x: x.__name__, inheritors(ViewModel)))
    base_roles = {
        "user",
        "editor",
        "viewer"
    }

    def add_roles(roles):
        for role in roles:
            session.add(role)
            session.commit()

    def permissions(vmc, perms):
        res = [session.query(Permission).filter(Permission.name == f"{vmc.lower()}.{p}").one_or_none()
               for p in perms]
        return res

    user_roles = [Role(name=f"{vmc.lower()}.user", created_by=user.id,
                       permissions=permissions(vmc, {"add", "edit", "delete", "list"}))
                  for vmc in view_model_classes]

    editor_roles = [Role(name=f"{vmc.lower()}.editor", created_by=user.id,
                         permissions=permissions(vmc, {"edit.all", "add", "delete.all", "list.all"}))
                    for vmc in view_model_classes]

    viewer_roles = [
        Role(name=f"{vmc.lower()}.viewer", created_by=user.id, permissions=permissions(vmc, {"list.all"}))
        for vmc in view_model_classes]

    add_roles(user_roles + editor_roles + viewer_roles)
    update_user = session.query(User).filter(User.id == user.id).one_or_none()
    update_user.roles = user_roles + editor_roles + viewer_roles
    session.add(update_user)


def init_permissions(user):
    view_model_classes = map(lambda x: x.__name__, inheritors(ViewModel))
    base_permissions = {
        "edit.all",
        "delete.all",
        "edit",
        "delete",
        "add",
        "list",
        "list.all"
    }

    @provide_session
    def add_permissions(perms, session=None):
        session.bulk_save_objects(perms)
        session.commit()

    permissions = [Permission(name=f"{vmc.lower()}.{p}", created_by=user.id) for vmc in view_model_classes for p in
                   base_permissions]
    add_permissions(permissions)


def worker(args):
    celery_app = CeleryWorker(config).get_celery_app()
    wk = celery_app.Job(include=["render.worker.tasks"])
    wk.start()


@provide_session
def db_init(arg, session=None):
    from render.models.user import User
    from sqlalchemy.exc import OperationalError

    from render.utils import setting
    from render.models.user import user_roles

    try:
        User.__table__.create(setting.mysql_engine, checkfirst=True)
        Role.__table__.create(setting.mysql_engine, checkfirst=True)
        Permission.__table__.create(setting.mysql_engine, checkfirst=True)
        Module.__table__.create(setting.mysql_engine, checkfirst=True)
        UserProfile.__table__.create(setting.mysql_engine, checkfirst=True)
        Job.__table__.create(setting.mysql_engine, checkfirst=True)
        JobRun.__table__.create(setting.mysql_engine, checkfirst=True)
        user_roles.create(setting.mysql_engine, checkfirst=True)
        role_permissions.create(setting.mysql_engine, checkfirst=True)
        user_modules.create(setting.mysql_engine, checkfirst=True)

        User.add("a@mail.com", "a", 1)
        user = session.query(User).filter(User.user_name == "a@mail.com").one_or_none()
        profile = UserProfile(name=user.user_name, id=user.id)
        session.add(profile)

        init_permissions(user)
        init_roles(user)
        init_applications(user)

    except OperationalError as e:
        logger.error(e)
        raise e


class APPFactory(object):
    common_args = {
        "debug": Arg(flags=("-d", "--debug"), help="debug mode")
    }

    apps = [
        Command(func=version, args=[]),
        Command(func=db_init, args=[]),
        Command(func=worker, args=[])
    ]

    @classmethod
    def get_parser(cls):
        parser = argparse.ArgumentParser()
        sub_parsers = parser.add_subparsers(help="types of application")
        for app in APPFactory.apps:
            app.add_to_parser(sub_parsers)
        return parser

# if __name__ == '__main__':
#     worker([])
