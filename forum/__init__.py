from flask import Flask
from flask_restful import Api
from .database import init_app, rebuild_db
from .config import config


def create_app(test_config=None):
    _app = Flask(__name__)
    api = Api(_app, prefix='/api')

    _app.config.from_mapping(config)
    if test_config is not None:
        _app.config.from_object(test_config)

    from forum.home import bp_home
    _app.register_blueprint(bp_home)
    from forum.api import UsersApi, TokensApi, PostsApi, PostApi
    api.add_resource(UsersApi, '/users')
    api.add_resource(TokensApi, '/tokens')
    api.add_resource(PostApi, '/post/<string:post_id>')
    api.add_resource(PostsApi, '/posts')

    from forum.modules import User, Section, Post, Comment
    with _app.app_context():
        init_app()

    return _app


app = create_app()
