from render.exceptions.user_exceptions import UserNotFoundError, PasswordMismatchError
from render.log.logging_mixin import LoggingMixin
from render.models.user import User
from render.utils.db import provide_session


class UserService(LoggingMixin):
    def __init__(self, password_manager):
        self.password_manager = password_manager

    @provide_session
    def create_user(self, user_name, password, session=None):
        user = User(user_name=user_name, password=self.password_manager.generate_password(password))
        session.add(user)

    @provide_session
    def verify_password(self, user_name, password, session=None):
        user = session.query(User).filter(User.user_name == user_name).one_or_none()
        if not user:
            raise UserNotFoundError("User not found")
        return self.password_manager.verify_password(password, user.password)

    @provide_session
    def login(self, user_name, password, session=None):
        user = session.query(User).filter(User.user_name == user_name).one_or_none()
        if not user:
            raise UserNotFoundError("User not found")
        if not self.password_manager.verify_password(password, user.password):
            raise PasswordMismatchError("Password mismatch")
        return user
