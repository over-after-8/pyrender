from enum import Enum
from functools import reduce, wraps

from flask_login import current_user
from sqlalchemy import and_

from render.exceptions.user_exceptions import UserNotFoundError
from render.models.user import User
from render.utils.db import provide_session


class Perm(Enum):
    LIST_ITEM = "list_items"
    ADD_ITEM = "add_item"
    EDIT_ITEM = "edit_item"
    DELETE_ITEM = "delete_item"
    DETAIL_ITEM = "detail_item"


class AccessDeniedError(Exception):
    pass


@provide_session
def permissions_by_user(user_id, session=None):
    user = session.query(User).filter(User.id == user_id).one_or_none()
    if user:
        return reduce(lambda r, x: r + x.permissions, user.roles, [])
    raise UserNotFoundError("User not found")


@provide_session
def owned_by(model_class, item_id, session=None):
    res = session.query(model_class).filter(
        and_(model_class.id == item_id, model_class.created_by == current_user.id)).one_or_none()
    return bool(res)


class PermissionChecker:
    def check(self, user, required_permission, resource_id=None, model_class=None):
        raise NotImplementedError()


class PermissionCheckerByItem(PermissionChecker):
    def check(self, user, required_permission, resource_id=None, model_class=None):
        permissions = permissions_by_user(user.id)
        has_all = any(required_permission in p.name and p.name.endswith(".all") for p in permissions)
        if has_all:
            return True
        has_specific = any(required_permission in p.name for p in permissions)
        if has_specific and resource_id and model_class:
            if owned_by(model_class, resource_id):
                return True
        return False


class PermissionCheckerByRole(PermissionChecker):
    def check(self, user, *args, **kwargs):
        if hasattr(user, "roles"):
            return bool(list(filter(lambda x: x == "admin", map(lambda x: x.name, user.roles))))
        return False


class PermissionCheckerByUser(PermissionChecker):
    def check(self, user, required_permission, resource_id=None, model_class=None):
        permissions = permissions_by_user(user.id)
        return any(required_permission in p.name for p in permissions)


class PermissionCheckerFactory:
    @staticmethod
    def validate(user, func, self_object, item_id, required_permission):
        admin_checker = PermissionCheckerByRole()
        if admin_checker.check(user):
            return True

        if "item_id" in func.__code__.co_varnames:
            checker = PermissionCheckerByItem()
        else:
            checker = PermissionCheckerByUser()

        return checker.check(
            user=user,
            required_permission=required_permission,
            resource_id=item_id,
            model_class=getattr(self_object, "model_class", None)
        )


def check_permission(permission_action):
    def decorator(func):
        @wraps(func)
        def wrapper(self_object, *args, **kwargs):
            view_model_name = self_object.__class__.__name__.lower()
            required_permission = f"{view_model_name}.{permission_action.value}"
            item_id = kwargs.get("item_id") or (args[0].item_id if args else None)

            is_allowed = PermissionCheckerFactory.validate(
                user=current_user,
                func=func,
                self_object=self_object,
                item_id=item_id,
                required_permission=required_permission
            )

            if not is_allowed:
                raise AccessDeniedError()

            return func(self_object, *args, **kwargs)

        return wrapper

    return decorator
