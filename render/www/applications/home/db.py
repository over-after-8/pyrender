from render.builder.db_initialization import DBInitialization, PermissionInitialization, RoleInitialization, ModuleInitialization
from render.utils.db import provide_session
from render.www.applications.home.app import Home
from render.www.applications.home.viewmodels.vm_home import VMHome


class HomePermissionInitialization(PermissionInitialization):
    view_model_classes = [VMHome]


class HomeRoleInitialization(RoleInitialization):
    view_model_classes = [VMHome]


class HomeModuleInitialization(ModuleInitialization):
    applications = [Home("Home")]


class HomeDB(DBInitialization):
    def __init__(self,
                 permission_initialization: PermissionInitialization,
                 role_initialization: RoleInitialization,
                 module_initialization: ModuleInitialization):
        super().__init__(permission_initialization, role_initialization, module_initialization)

    @provide_session
    def initialize(self, session):
        pass


home_db = HomeDB(HomePermissionInitialization(),
                 HomeRoleInitialization(),
                 HomeModuleInitialization())
