from flask_testing import TestCase
from datetime import datetime
from forum import create_app
from forum.database import db
from forum.modules import User, Post, Section


class TestModifyPost(TestCase):
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

        self.time = datetime(2018, 9, 10, 13, 00, 00)

        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
            })
            self.token = response.json['token']
            response = client.post('/api/posts', json={
                'post_name': "today's sports",
                'post_time': self.time,
                'section_name': 'sport',
                'context': "sport is great!",
            }, headers={'Authorization': "Token " + self.token})
            self.post_id = response.json['post_id']

    def test_modify_both(self):
        with self.app.test_client() as client:
            response = client.put(f'/api/post/{self.post_id}', json={
                'post_name': "tomorrow's sports",
                'context': "sport is worse!",
            }, headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 200)
            self.assertEqual(response.json['post_id'], self.post_id)

            response = client.get(f'/api/post/{self.post_id}')
            self.assertStatus(response, 200)
            post = response.json
            self.assertEqual(post['post_name'], "tomorrow's sports")
            self.assertEqual(post['context'], "sport is worse!")

    def test_modify_name(self):
        with self.app.test_client() as client:
            response = client.put(f'/api/post/{self.post_id}', json={
                'post_name': "tomorrow's sports",
            }, headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 200)
            self.assertEqual(response.json['post_id'], self.post_id)

            response = client.get(f'/api/post/{self.post_id}')
            self.assertStatus(response, 200)
            post = response.json
            self.assertEqual(post['post_name'], "tomorrow's sports")

    def test_modify_context(self):
        with self.app.test_client() as client:
            response = client.put(f'/api/post/{self.post_id}', json={
                'context': "sport is worse!",
            }, headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 200)
            self.assertEqual(response.json['post_id'], self.post_id)

            response = client.get(f'/api/post/{self.post_id}')
            self.assertStatus(response, 200)
            post = response.json
            self.assertEqual(post['context'], "sport is worse!")

    def test_modify_none(self):
        with self.app.test_client() as client:
            response = client.put(f'/api/post/{self.post_id}', json={

            }, headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 400)
            self.assertEqual(response.json, {'message': 'arguments missing'})

    def test_modify_with_other_argument(self):
        with self.app.test_client() as client:
            response = client.put(f'/api/post/{self.post_id}', json={
                'else': 'something else'
            }, headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 400)
            self.assertEqual(response.json, {'message': 'arguments missing'})

    def test_modify_without_token(self):
        with self.app.test_client() as client:
            response = client.put(f'/api/post/{self.post_id}', json={
                'post_name': "tomorrow's sports",
                'context': "sport is worse!",
            })
            self.assertStatus(response, 401)
