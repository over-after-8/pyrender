from functools import reduce

from render.models.user import Permission, Role, Module
from render.utils.db import provide_session


def fullname(klass):
    module = klass.__module__
    if module == 'builtins':
        return klass.__qualname__
    return module + '.' + klass.__qualname__


class AlreadyInitializedException(Exception):
    pass


class PermissionInitialization:
    view_model_classes = None
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
    def execute(self, session=None):
        permissions = [Permission(name=f"{vmc.__name__.lower()}.{p}")
                       for vmc in self.view_model_classes
                       for p in self.base_permissions]
        session.bulk_save_objects(permissions)


class RoleInitialization:
    view_model_classes = None
    base_roles = {
        "user",
        "editor",
        "viewer"
    }

    @provide_session
    def execute(self, session=None):
        def permissions(vmc, perms):
            return [session.query(Permission).filter(Permission.name == f"{vmc.lower()}.{p}").one_or_none() for p in perms]

        roles = [
            [Role(name=f"{vmc.lower()}.user", permissions=permissions(vmc, {"add", "edit", "delete", "list"})),  # noqa
             Role(name=f"{vmc.lower()}.editor", permissions=permissions(vmc, {"edit.all", "add", "delete.all", "list.all"})),  # noqa
             Role(name=f"{vmc.lower()}.viewer", permissions=permissions(vmc, {"list.all"}))]  # noqa
            for vmc in [x.__name__ for x in self.view_model_classes]]
        for role in reduce(lambda x, y: x + y, roles):
            session.add(role)


class ModuleInitialization:
    applications = None

    @provide_session
    def execute(self, session=None):
        application_objects = [Module(name=x.name, class_name=fullname(x.__class__)) for x in self.applications]
        session.bulk_save_objects(application_objects)


class DBInitialization:
    def __init__(
            self,
            permission_initialization: PermissionInitialization,
            role_initialization: RoleInitialization,
            module_initialization: ModuleInitialization
    ):
        self.permission_initialization = permission_initialization
        self.role_initialization = role_initialization
        self.module_initialization = module_initialization

    @provide_session
    def execute(self, session=None):
        if self.already_initialized():
            raise AlreadyInitializedException("Already initialized")
        self.initialize()
        self.permission_initialization.execute()
        self.role_initialization.execute()
        self.module_initialization.execute()

    @provide_session
    def initialize(self, session=None):
        raise NotImplementedError()

    @provide_session
    def already_initialized(self, session=None):
        return False
