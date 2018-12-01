from flask import Flask
from .database import init_app, rebuild_db

config = {
    'SESSION_TYPE': 'memcached',
    'SQLALCHEMY_DATABASE_URI':
        'mysql+mysqlconnector://wustl_inst:'
        'wustl_pass@ec2-52-14-93-16.us-east-2.compute.amazonaws.com:3306/orm_forum',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    'SESSION_COOKIE_HTTPONLY': True,
    'SECRET_KEY': 'super secret key',
}


def create_app(test_config=None):
    _app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/forum/static")

    _app.config.from_mapping(config)
    if test_config is not None:
        _app.config.from_object(test_config)

    from forum.home import bp_home

    _app.register_blueprint(bp_home)

    with _app.app_context():
        init_app()

    return _app


app = create_app()
