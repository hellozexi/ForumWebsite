from flask import abort, g
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
            abort(400, 'user already exist')
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
            abort(400, 'wrong password')
        return {'token': signer.sign(user.user_id).decode()}, 201


class SectionsApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('section_name', type=str, required=True, help='section name missing')

    def get(self):
        sections = Section.query.all()
        return [section.section_name for section in sections], 200

    @auth.login_required
    def post(self):
        args = self.parser.parse_args()
        if not g.user.admin:
            abort(403, 'user is not admin!')
        if Section.query.filter_by(section_name=args['section_name']).count() != 0:
            abort(400, 'section already exist')
        section = Section.create(args['section_name'])
        db.session.add(section)
        db.session.commit()
        return {'section_name': args['section_name']}, 201


class SectionApi(Resource):
    @auth.login_required
    def delete(self, section_name):
        if not g.user.admin:
            abort(403, 'user is not admin!')
        section = Section.query.filter_by(section_name=section_name).first()
        if section is None:
            abort(404, 'section not exist')
        db.session.delete(section)
        db.session.commit()
        return {'section_name': section_name}, 200


class PostsApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('post_name', type=str, required=True, help="post name missing")
        self.parser.add_argument('post_time', type=str, required=True, help="post time missing")
        self.parser.add_argument('section_name', type=str, required=True, help='section name missing')
        self.parser.add_argument('context', type=str, required=True, help='context missing')

        self.id_parser = reqparse.RequestParser()
        self.id_parser.add_argument('section_name', default=None, type=str, help='section name')
        self.id_parser.add_argument('user_id', default=None, type=str, help='user id')
        super(PostsApi, self).__init__()

    def get(self):
        args = self.id_parser.parse_args()
        section_name, user_id = args['section_name'], args['user_id']
        if section_name is None:
            if user_id is None:
                abort(400, 'arguments missing')
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
            if user_id is None:
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
                abort(400, 'too many arguments')

    @auth.login_required
    def post(self):
        args = self.parser.parse_args()
        section = Section.query.filter_by(section_name=args['section_name']).first()
        if section is None:
            abort(404, 'section not exist')
        if not check_datetime(args['post_time']):
            abort(400, 'post_time not valid')
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
        self.parser.add_argument('post_name', default=None, type=str, help="post name")
        self.parser.add_argument('context',  default=None, type=str, help='context')
        super(PostApi, self).__init__()

    @auth.login_required
    def put(self, post_id):
        post = Post.query.filter_by(post_id=post_id).first()
        if post is None:
            abort(404, 'post not found')
        if post.poster_email != g.user.email:
            abort(403, "you don't have permission to modify")
        args = self.parser.parse_args()
        if args['post_name'] is None and args['context'] is None:
            abort(400, 'arguments missing')
        if args['post_name'] is not None:
            post.post_name = args['post_name']
        if args['context'] is not None:
            post.context = args['context']
        return {'post_id': post_id}, 200

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
        post = Post.query.filter_by(post_id=post_id).first()
        if post is None:
            abort(404, 'event not exist')
        if post.poster_email != g.user.email and not g.user.admin:
            # the poster and the admin could delete post
            abort(403, "you don't have permission to delete")
        db.session.delete(post)
        db.session.commit()
        return {'post_id': post_id}, 200


class CommentsApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('post_id', type=str, required=True, help="post id missing")
        self.parser.add_argument('comment_time', type=str, required=True, help="comment time missing")
        self.parser.add_argument('context', type=str, required=True, help='context missing')

        self.id_parser = reqparse.RequestParser()
        self.id_parser.add_argument('post_id', default=None, type=str, help='post id')
        self.id_parser.add_argument('user_id', default=None, type=str, help='user id')
        super(CommentsApi, self).__init__()

    def get(self):
        args = self.id_parser.parse_args()
        post_id, user_id = args['post_id'], args['user_id']
        if post_id is None:
            if user_id is None:
                abort(400, 'arguments missing')
            else:  # with user argument
                user = User.query.filter_by(user_id=user_id).first()
                if user is None:
                    abort(404, 'user not exist')
                return [{
                    'comment_id': comments.comment_id,
                    'post_id': comments.post_id,
                    'comment_time': str(comments.comment_time),
                    'author_email': comments.author_email,
                    'context': comments.context,
                } for comments in user.comments], 200
        else:  # with post id argument
            if user_id is None:
                post = Post.query.filter_by(post_id=post_id).first()
                if post is None:
                    abort(404, 'section not exist')
                return [{
                    'comment_id': comment.comment_id,
                    'post_id': comment.post_id,
                    'comment_time': str(comment.comment_time),
                    'author_email': comment.author_email,
                    'context': comment.context,
                } for comment in post.comments], 200
            else:  # with user argument
                abort(400, 'too many arguments')

    @auth.login_required
    def post(self):
        args = self.parser.parse_args()
        post = Post.query.filter_by(post_id=args['post_id']).first()
        if post is None:
            abort(404, 'post not exist')
        if not check_datetime(args['comment_time']):
            abort(400, 'comment_time not valid')
        with db.session.no_autoflush:
            comment = Comment.create(parser.parse(args['comment_time']), args['context'])
            comment_id = comment.comment_id
            g.user.comments.append(comment)
            post.comments.append(comment)
            db.session.commit()
        return {'comment_id': comment_id}, 201


class CommentApi(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser(bundle_errors=True)
        self.parser.add_argument('context',  default=None, type=str, help='context')
        super(CommentApi, self).__init__()

    @auth.login_required
    def put(self, comment_id):
        comment = Comment.query.filter_by(comment_id=comment_id).first()
        if comment is None:
            abort(404, 'post not found')
        if comment.author_email != g.user.email:
            abort(403, "you don't have permission to modify")
        args = self.parser.parse_args()
        if args['context'] is None:
            abort(400, 'argument missing')
        comment.context = args['context']
        return {'comment_id': comment_id}, 200

    def get(self, comment_id):
        """
        get specific post
        :param comment_id:
        :return:
        """
        comment = Comment.query.filter_by(comment_id=comment_id).first()
        if comment is None:
            abort(404, 'post not found')
        return {
            'comment_id': comment.comment_id,
            'post_id': comment.post_id,
            'comment_time': str(comment.comment_time),
            'author_email': comment.author_email,
            'context': comment.context,
        }, 200

    def delete(self, comment_id):
        """
        delete selected post
        :param comment_id:
        :return:
        """
        comment = Comment.query.with_parent(g.user).filter_by(comment_id=comment_id).first()
        if comment is None:
            abort(404, 'event not exist')
        if comment.post.poster_email != g.user.email and comment.author_email != g.user.email and not g.user.admin:
            # the poster, commenter and the admin could delete comment
            abort(403, "you don't have permission to delete")
        db.session.delete(comment)
        db.session.commit()
        return {'comment_id': comment_id}, 200
