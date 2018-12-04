from flask_testing import TestCase
from datetime import datetime
from forum import create_app
from forum.database import db
from forum.modules import User, Post, Section


class TestGetPost(TestCase):
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_by_id(self):
        with self.app.test_client() as client:
            response = client.get(f'/api/post/{self.post_id}')
            self.assertStatus(response, 200)
            post = response.json
            self.assertEqual(post['post_id'], self.post_id)
            self.assertEqual(post['post_name'], "today's sports")
            self.assertEqual(post['post_time'], str(self.time))
            self.assertEqual(post['poster_email'], 'xua@wustl.edu')
            self.assertEqual(post['section_name'], 'sport')
            self.assertEqual(post['context'], "sport is great!")
            self.assertIsInstance(post['comments'], list)

    def test_get_not_exist(self):
        with self.app.test_client() as client:
            response = client.get(f'/api/post/{self.user_id}')
            self.assertStatus(response, 404)
            self.assertEqual(response.json, {'message': 'post not found'})
