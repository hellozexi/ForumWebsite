from flask_testing import TestCase
from datetime import datetime
from urllib.parse import urlencode
from forum import create_app
from forum.database import db
from forum.modules import User


class TestBlockComment(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.drop_all()
        db.create_all()

        admin = User.create('admin', 'admin', admin=True)
        xua = User.create('xua', 'xua', admin=False)
        db.session.add(xua)
        db.session.add(admin)
        db.session.commit()

        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'admin',
                'password': 'admin',
            })
            self.token = response.json['token']

            client.post('/api/sections', json={
                'section_name': 'sport',
            }, headers={'Authorization': "Token " + self.token})

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

    def test_block_comment(self):
        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'xua',
                'password': 'xua',
            })
            token = response.json['token']

            response = client.post('/api/comments', json={
                'post_id': self.post_id,
                'comment_time': datetime(2018, 7, 10, 12, 55, 0),
                'context': 'this is great!',
            }, headers={'Authorization': "Token " + token})
            self.assertStatus(response, 201)

            response = client.post('/api/blocks', json={
                'section_name': 'sport',
                'user_email': 'xua'
            }, headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 201)

            response = client.post('/api/comments', json={
                'post_id': self.post_id,
                'comment_time': datetime(2018, 10, 10, 12, 55, 0),
                'context': 'this is super great!',
            }, headers={'Authorization': "Token " + token})
            self.assertStatus(response, 403)

    def test_unblock_comment(self):
        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'xua',
                'password': 'xua',
            })
            token = response.json['token']

            response = client.post('/api/comments', json={
                'post_id': self.post_id,
                'comment_time': datetime(2018, 7, 10, 12, 55, 0),
                'context': 'this is great!',
            }, headers={'Authorization': "Token " + token})
            self.assertStatus(response, 201)

            response = client.post('/api/blocks', json={
                'section_name': 'sport',
                'user_email': 'xua'
            }, headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 201)

            response = client.post('/api/comments', json={
                'post_id': self.post_id,
                'comment_time': datetime(2018, 10, 10, 12, 55, 0),
                'context': 'this is super great!',
            }, headers={'Authorization': "Token " + token})
            self.assertStatus(response, 403)

            response = client.delete(f'/api/block/sport?{urlencode({"user_email": "xua"})}',
                                     headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 200)

            response = client.post('/api/comments', json={
                'post_id': self.post_id,
                'comment_time': datetime(2018, 10, 10, 12, 55, 0),
                'context': 'this is super great!',
            }, headers={'Authorization': "Token " + token})
            self.assertStatus(response, 201)
