from passlib.context import CryptContext

class BcryptService:

    def __init__(self):
        self._context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify(self, plain_text: str, hashed_text: str):
        return self._context.verify(plain_text, hashed_text)

    def hash(self, plain_text: str):
        return self._context.hash(plain_text)