from passlib.hash import sha256_crypt
from .database import db
from .utils import new_uuid


class User(db.Model):
    user_id = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(80))

    @staticmethod
    def create(email: str, password: str):
        return User(user_id=new_uuid(), email=email, password=sha256_crypt.hash(password))

    def verify(self, password):
        return sha256_crypt.verify(password, self.password)

    def __repr__(self):
        return f'{self.user_id}:{self.email}'
