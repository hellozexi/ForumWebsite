from flask_testing import TestCase
from forum import create_app
from forum.database import db
from forum.modules import User, Section, Post
from datetime import datetime


class TestPost(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create(self):
        user = User.create('xua@wustl', 'password')
        section = Section.create('sports')

        time = datetime.now()
        post = Post.create("today's sports", time, "hey, let's discuss today's sports!")
        post_id = post.post_id
        user.posts.append(post)
        section.posts.append(post)
        db.session.add(user)
        db.session.add(section)
        db.session.commit()

        post = Post.query.filter_by(post_id=post_id).first()
        self.assertEqual(post.post_time, time)
        self.assertEqual(post.post_name, "today's sports")
        self.assertEqual(post.poster_email, 'xua@wustl')
        self.assertEqual(post.section_name, 'sports')
