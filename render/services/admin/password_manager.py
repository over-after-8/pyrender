import bcrypt

class PasswordManager:
    def __init__(self, salt_rounds: int = 12):
        self.salt_rounds = salt_rounds

    def generate_password(self, plain_password: str) -> str:
        salt = bcrypt.gensalt(self.salt_rounds)
        hashed = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
