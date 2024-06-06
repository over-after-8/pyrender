import argparse
import logging

from render.builder.utils import inheritors
from render.builder.viewmodel import ViewModel
from render.models.permission import Permission
from render.models.role import Role, role_permissions
from render.utils.db import provide_session

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


def init_permissions():
    from render.www.views.permission_view_model import PermissionViewModel
    from render.www.views.role_view_model import RoleViewModel
    from render.www.views.user_view_model import UserViewModel

    view_model_classes = map(lambda x: x.__name__, inheritors(ViewModel))
    base_permissions = {
        "read_everything",
        "create_everything",
        "update_everything",
        "delete_everything",
        "read_owned",
        "update_owned",
        "delete_owned"
    }

    @provide_session
    def add_permissions(perms, session=None):
        session.bulk_save_objects(perms)
        session.commit()

    permissions = [Permission(name=f"{vmc.lower()}_{p}") for vmc in view_model_classes for p in base_permissions]
    add_permissions(permissions)


def db_init(arg):
    from render.models.user import User
    from sqlalchemy.exc import OperationalError

    from render.utils import setting
    from render.models.user import user_roles

    try:
        User.__table__.create(setting.mysql_engine, checkfirst=True)
        Role.__table__.create(setting.mysql_engine, checkfirst=True)
        Permission.__table__.create(setting.mysql_engine, checkfirst=True)
        user_roles.create(setting.mysql_engine, checkfirst=True)
        role_permissions.create(setting.mysql_engine, checkfirst=True)

        User.add("a@mail.com", "a")

        init_permissions()

    except OperationalError as e:
        logger.error(e)
        raise e


class APPFactory(object):
    common_args = {
        "debug": Arg(flags=("-d", "--debug"), help="debug mode")
    }

    apps = [
        Command(func=version, args=[]),
        Command(func=db_init, args=[])
    ]

    @classmethod
    def get_parser(cls):
        parser = argparse.ArgumentParser()
        sub_parsers = parser.add_subparsers(help="types of application")
        for app in APPFactory.apps:
            app.add_to_parser(sub_parsers)
        return parser
