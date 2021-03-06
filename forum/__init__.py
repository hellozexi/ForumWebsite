from flask import Flask
from flask_restful import Api
from .database import init_app, rebuild_db
from .config import config


def create_app(test_config=None):
    _app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/forum/static")
    api = Api(_app, prefix='/api')

    _app.config.from_mapping(config)
    if test_config is not None:
        _app.config.from_object(test_config)

    from forum.home import bp_home
    _app.register_blueprint(bp_home)
    from forum.api import UsersApi, TokensApi, \
        SectionApi, SectionsApi,\
        BlockApi, BlocksApi, \
        PostsApi, PostApi, \
        CommentsApi, CommentApi
    api.add_resource(UsersApi, '/users')
    api.add_resource(TokensApi, '/tokens')
    api.add_resource(SectionApi, '/section/<string:section_name>')
    api.add_resource(SectionsApi, '/sections')
    api.add_resource(BlockApi, '/block/<string:section_name>')
    api.add_resource(BlocksApi, '/blocks')
    api.add_resource(PostApi, '/post/<string:post_id>')
    api.add_resource(PostsApi, '/posts')
    api.add_resource(CommentApi, '/comment/<string:comment_id>')
    api.add_resource(CommentsApi, '/comments')

    from forum.modules import User, Section, Post, Comment
    with _app.app_context():
        init_app()

    return _app


app = create_app()
