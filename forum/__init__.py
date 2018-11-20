from flask import Flask

config = {
    'SESSION_TYPE': 'memcached',
    'SQLALCHEMY_DATABASE_URI':
        'mysql+mysqlconnector://wustl_inst:'
        'wustl_pass@ec2-52-14-93-16.us-east-2.compute.amazonaws.com:3306/orm_forum',
    'SQLALCHEMY_TRACK_MODIFICATIONS': True,
    'SESSION_COOKIE_HTTPONLY': True,
}


def create_app(test_config=None):
    _app = Flask(__name__)

    _app.secret_key = 'super secret key'
    _app.config.from_mapping(config)
    if test_config is not None:
        _app.config.from_object(test_config)

    from forum.home import bp_home

    _app.register_blueprint(bp_home)

    return _app


app = create_app()
