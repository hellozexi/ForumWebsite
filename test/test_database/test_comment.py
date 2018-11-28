from flask_testing import TestCase
from forum import create_app
from forum.database import db
from forum.modules import User, Section, Post, Comment
from datetime import datetime


class TestComment(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_comment(self):
        user = User.create('xua@wustl', 'password')
        section = Section.create('sports')

        post = Post.create("today's sports", datetime.now(), "hey, let's discuss today's sports!")
        post_id = post.post_id
        first = Comment.create(datetime.now(), "it sounds good!")
        second = Comment.create(datetime.now(), "I don't like sports")
        post.comments.append(first)
        post.comments.append(second)
        user.comments.append(first)
        user.comments.append(second)
        user.posts.append(post)
        section.posts.append(post)
        db.session.add(user)
        db.session.add(section)
        db.session.commit()

        post = Post.query.filter_by(post_id=post_id).first()
        self.assertEqual(len(post.comments), 2)
