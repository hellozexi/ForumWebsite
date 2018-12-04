from flask_testing import TestCase
from datetime import datetime
from urllib.parse import urlencode
from forum import create_app
from forum.database import db
from forum.modules import User, Post, Section


class TestGetPosts(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.drop_all()
        db.create_all()

        user = User.create('xua@wustl.edu', 'strong_password')
        # post = Post.create('sports', datetime.now(), "do some sport!")
        self.user_id = user.user_id
        db.session.add(user)
        db.session.add(Section.create("sport"))
        db.session.commit()

        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
            })
            self.token = response.json['token']
            client.post('/api/posts', json={
                'post_name': "today's sports",
                'post_time': datetime.now(),
                'section_name': 'sport',
                'context': "sport is great!",
            }, headers={'Authorization': "Token " + self.token})
            client.post('/api/posts', json={
                'post_name': "yesterday's sports",
                'post_time': datetime.now(),
                'section_name': 'sport',
                'context': "sport is great!",
            }, headers={'Authorization': "Token " + self.token})
            client.post('/api/posts', json={
                'post_name': "tomorrow's sports",
                'post_time': datetime.now(),
                'section_name': 'sport',
                'context': "sport is great!",
            }, headers={'Authorization': "Token " + self.token})

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_by_user(self):
        with self.app.test_client() as client:
            response = client.get(f'/api/posts?{urlencode({"user_email": "xua@wustl.edu"})}')
            self.assertEqual(len(response.json), 3)
            names = [post['post_name'] for post in response.json]
            self.assertListEqual(names, ["today's sports", "yesterday's sports", "tomorrow's sports"])

    def test_get_by_section(self):
        with self.app.test_client() as client:
            response = client.get(f'/api/posts?{urlencode({"section_name": "sport"})}')
            self.assertEqual(len(response.json), 3)
            names = [post['post_name'] for post in response.json]
            self.assertListEqual(names, ["today's sports", "yesterday's sports", "tomorrow's sports"])

    def test_get_without_argument(self):
        with self.app.test_client() as client:
            response = client.get(f'/api/posts')
            self.assertStatus(response, 400)
            self.assertEqual(response.json, {'message': 'arguments missing'})

    def test_get_with_other_argument(self):
        with self.app.test_client() as client:
            response = client.get(f'/api/posts?{urlencode({"other": "else"})}')
            self.assertStatus(response, 400)
            self.assertEqual(response.json, {'message': 'arguments missing'})

    def test_too_many_argumernts(self):
        with self.app.test_client() as client:
            response = client.get(f'/api/posts?{urlencode({"user_email": "xua@wustl.edu", "section_name": "sport"})}')
            self.assertStatus(response, 400)
            self.assertEqual(response.json, {'message': 'too many arguments'})
