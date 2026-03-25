from render.builder.db_initialization import DBInitialization, PermissionInitialization, RoleInitialization, ModuleInitialization
from render.models.user import Role
from render.services.admin.password_manager import PasswordManager
from render.services.admin.user_service import UserService
from render.utils.db import provide_session
from render.www.applications.administration.app import Administration
from render.www.applications.administration.viewmodels.vm_module import VMModule
from render.www.applications.administration.viewmodels.vm_permission import VMPermission
from render.www.applications.administration.viewmodels.vm_role import VMRole
from render.www.applications.administration.viewmodels.vm_user import VMUser


class AdministrationPermissionInitialization(PermissionInitialization):
    view_model_classes = [VMModule, VMPermission, VMRole, VMUser]


class AdministrationRoleInitialization(RoleInitialization):
    view_model_classes = [VMModule, VMPermission, VMRole, VMUser]


class AdministrationModuleInitialization(ModuleInitialization):
    applications = [Administration("Administration")]


class AdministrationDB(DBInitialization):
    def __init__(self,
                 permission_initialization: PermissionInitialization,
                 role_initialization: RoleInitialization,
                 module_initialization: ModuleInitialization):
        super().__init__(permission_initialization, role_initialization, module_initialization)

    @provide_session
    def initialize(self, session):
        user_service = UserService(PasswordManager())
        user = user_service.create_user("admin", "admin", session=session)
        admin_role = Role(name="admin")
        user.roles.append(admin_role)


administration_db = AdministrationDB(AdministrationPermissionInitialization(),
                                     AdministrationRoleInitialization(),
                                     AdministrationModuleInitialization())
