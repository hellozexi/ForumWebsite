from flask_testing import TestCase
from datetime import datetime
from forum import create_app
from forum.database import db
from forum.modules import User, Section


class TestCreateComment(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.drop_all()
        db.create_all()

        user = User.create('xua@wustl.edu', 'strong_password')
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
            response = client.post('/api/posts', json={
                'post_name': "today's sports",
                'post_time': datetime(2018, 7, 9, 12, 55, 0),
                'section_name': 'sport',
                'context': "sport is great!",
            }, headers={'Authorization': "Token " + self.token})
            self.post_id = response.json['post_id']

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_comment(self):
        with self.app.test_client() as client:
            response = client.post('/api/comments', json={
                'post_id': self.post_id,
                'comment_time': datetime(2018, 7, 10, 12, 55, 0),
                'context': 'this is great!',
            }, headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 201)
            self.assertIsNotNone(response.json['comment_id'])

    def test_create_missing_time(self):
        with self.app.test_client() as client:
            response = client.post('/api/comments', json={
                'post_id': self.post_id,
                'context': 'this is great!',
            }, headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 400)

    def test_create_wrong_post_time(self):
        with self.app.test_client() as client:
            response = client.post('/api/comments', json={
                'post_id': self.post_id,
                'comment_time': 'wrong time',
                'context': 'this is great!',
            }, headers={'Authorization': "Token " + self.token})

            self.assertStatus(response, 400)
            self.assertEqual(response.json, {'message': 'comment_time not valid'})

    def test_create_missing_post_id(self):
        with self.app.test_client() as client:
            response = client.post('/api/comments', json={
                'comment_time': datetime(2018, 7, 10, 12, 55, 0),
                'context': 'this is great!',
            }, headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 400)

    def test_create_post_not_exist(self):
        with self.app.test_client() as client:
            response = client.post('/api/comments', json={
                'post_id': 'not exist',
                'comment_time': datetime(2018, 7, 10, 12, 55, 0),
                'context': 'this is great!',
            }, headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 400)
            self.assertEqual(response.json, {'message': 'post not exist'})

    def test_create_missing_context(self):
        with self.app.test_client() as client:
            response = client.post('/api/comments', json={
                'post_id': self.post_id,
                'comment_time': datetime(2018, 7, 10, 12, 55, 0),
            }, headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 400)

    def test_create_missing_token(self):
        with self.app.test_client() as client:
            response = client.post('/api/comments', json={
                'post_id': self.post_id,
                'comment_time': datetime(2018, 7, 10, 12, 55, 0),
                'context': 'this is great!',
            })
            self.assertStatus(response, 401)
