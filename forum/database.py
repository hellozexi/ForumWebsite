from flask_sqlalchemy import SQLAlchemy
from flask import current_app


db = SQLAlchemy()


def init_app():
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    db.init_app(current_app)


def rebuild_db():
    """
    run for rebuild database, often run in the python commandline
    :return:
    """
    from forum import create_app
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()
        insert()


def insert():
    from .modules import User, Section
    db.session.add(User.create('admin', 'admin', admin=True))
    db.session.add(Section.create('default'))
    db.session.add(Section.create('others'))
    db.session.commit()
