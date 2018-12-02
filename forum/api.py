from flask import abort, g, request
from flask_restful import Resource, reqparse
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimestampSigner, SignatureExpired, BadSignature
from dateutil import parser
from .utils import check_datetime
from .config import config
from .database import db
from .modules import User, Section, Post, Comment


auth = HTTPTokenAuth(scheme='Token')
signer = TimestampSigner(config['SECRET_KEY'])


@auth.verify_token
def verify_token(token):
    try:
        user_id = signer.unsign(token, max_age=config['MAX_AGE']).decode()
    except SignatureExpired:
        return False
        # abort(403, "Signature Expired")
    except BadSignature:
        return False
        # abort(403, "Signature not match")
    g.user = User.query.filter_by(user_id=user_id).first()
    if g.user is None:
        return False
    return True


class UsersApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('email', type=str, required=True, help='field missing')
        self.parser.add_argument('password', type=str, required=True, help='field missing')
        super(UsersApi, self).__init__()

    def post(self):
        content = self.parser.parse_args()
        email, password = content['email'], content['password']
        # check if exist same user
        if User.query.filter_by(email=email).first() is not None:
            abort(403, 'user already exist')
        user = User.create(email, password)
        db.session.add(user)
        db.session.commit()
        return {"message": "success"}, 201


class TokensApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('email', type=str, required=True, help='field missing')
        self.parser.add_argument('password', type=str, required=True, help='field missing')
        super(TokensApi, self).__init__()

    def post(self):
        content = self.parser.parse_args()
        email, password = content['email'], content['password']
        user = User.query.filter_by(email=email).first()
        if user is None:
            abort(404, 'user not exist')
        if not user.verify(password):
            abort(403, 'wrong password')
        return {'token': signer.sign(user.user_id).decode()}, 201


class PostsApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('post_name', type=str, required=True, help="post name missing")
        self.parser.add_argument('post_time', type=str, required=True, help="post time missing")
        self.parser.add_argument('section_name', type=str, required=True, help='section name missing')
        self.parser.add_argument('context', type=str, required=True, help='context missing')
        super(PostsApi, self).__init__()

    def get(self):
        section_name = request.args.get('section_name', default='*', type=str)
        user_id = request.args.get('user_id', default='*', type=str)
        if section_name == '*':
            if user_id == '*':
                abort(403, 'arguments missing')
            else:  # with user argument
                user = User.query.filter_by(user_id=user_id).first()
                if user is None:
                    abort(404, 'user not exist')
                return [{
                    'post_id': post.post_id,
                    'post_name': post.post_name,
                    'post_time': str(post.post_time),
                    'poster_email': post.poster_email,
                    'section_name': post.section_name,
                } for post in user.posts], 200
        else:  # with section argument
            if user_id == '*':
                section = Section.query.filter_by(section_name=section_name).first()
                if section is None:
                    abort(404, 'section not exist')
                return [{
                    'post_id': post.post_id,
                    'post_name': post.post_name,
                    'post_time': str(post.post_time),
                    'poster_email': post.poster_email,
                    'section_name': post.section_name,
                } for post in section.posts], 200
            else:  # with user argument
                abort(403, 'too many arguments')

    @auth.login_required
    def post(self):
        args = self.parser.parse_args()
        section = Section.query.filter_by(section_name=args['section_name']).first()
        if section is None:
            abort(404, 'section not exist')
        if not check_datetime(args['post_time']):
            abort(403, 'post_time not valid')
        with db.session.no_autoflush:
            post = Post.create(args['post_name'], parser.parse(args['post_time']), args['context'])
            post_id = post.post_id
            g.user.posts.append(post)
            section.posts.append(post)
            db.session.commit()
        return {'post_id': post_id}, 201


class PostApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        super(PostApi, self).__init__()

    def get(self, post_id):
        """
        get specific post
        :param post_id:
        :return:
        """
        post = Post.query.filter_by(post_id=post_id).first()
        if post is None:
            abort(404, 'post not found')
        return {
            'post_id': post.post_id,
            'post_name': post.post_name,
            'post_time': str(post.post_time),
            'poster_email': post.poster_email,
            'section_name': post.section_name,
            'context': post.context,
            'comments': [
                {
                    'comment_id': comment.comment_id,
                    'post_id': comment.post_id,
                    'author_email': comment.author_email,
                    'comment_time': str(comment.comment_time),
                    'context': comment.context
                } for comment in post.comments
            ]
        }, 200

    def delete(self, post_id):
        """
        delete selected post
        :param post_id:
        :return:
        """
        post = Post.query.with_parent(g.user).filter_by(post_id=post_id).first()
        if post is None:
            abort(404, 'event not exist')
        db.session.delete(post)
        db.session.commit()
        return {'post_id': post_id}, 200
