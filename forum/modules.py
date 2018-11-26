from passlib.hash import sha256_crypt
from .database import db
from .utils import new_uuid
from datetime import datetime


class User(db.Model):
    user_id = db.Column(db.String(32), primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(80))
    posts = db.relationship('Post', lazy=True, backref='poster', cascade='all,delete')

    @staticmethod
    def create(email: str, password: str):
        return User(user_id=new_uuid(), email=email, password=sha256_crypt.hash(password))

    def verify(self, password):
        return sha256_crypt.verify(password, self.password)

    def __repr__(self):
        return f'{self.user_id}:{self.email}'


class Section(db.Model):
    section_id = db.Column(db.String(32), primary_key=True)
    section_name = db.Column(db.String(100))
    posts = db.relationship('Post', lazy=True, backref='section', cascade='all,delete')

    @staticmethod
    def create(name: str):
        return Section(section_id=new_uuid(), section_name=name)

    def __repr__(self):
        return f'{self.section_name}:{self.section_id}'


class Post(db.Model):

    post_id = db.Column(db.String(32), primary_key=True)
    post_name = db.Column(db.String(100))
    post_time = db.Column(db.DateTime)
    poster_id = db.Column(db.String(32), db.ForeignKey('user.user_id'), nullable=False)
    section_name = db.Column(db.String(100), db.ForeignKey('section.section_name'), nullable=False)

    @staticmethod
    def create(name: str, time: datetime):
        return Post(post_id=new_uuid(), post_name=name, post_time=time)

    def __repr__(self):
        return f'{self.post_name}:{self.post_time}'
