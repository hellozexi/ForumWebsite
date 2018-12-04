from flask_testing import TestCase
from datetime import datetime
from forum import create_app
from forum.database import db
from forum.modules import User, Post, Section


class TestCreatePost(TestCase):
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_post(self):
        with self.app.test_client() as client:
            time = datetime(2018, 7, 9, 12, 55, 0)
            response = client.post('/api/posts', json={
                'post_name': "today's sports",
                'post_time': time,
                'section_name': 'sport',
                'context': "sport is great!",
            }, headers={'Authorization': "Token " + self.token})

            self.assertStatus(response, 201)
            self.assertIsNotNone(response.json['post_id'])

            post = Post.query.filter_by(post_id=response.json['post_id']).first()
            self.assertIsNotNone(post)
            self.assertEqual(post.post_time, time)
            self.assertEqual(post.post_name, "today's sports")
            self.assertEqual(post.poster_email, 'xua@wustl.edu')
            self.assertEqual(post.section_name, 'sport')
            self.assertEqual(post.context, "sport is great!")

    def test_create_missing_name(self):
        with self.app.test_client() as client:
            response = client.post('/api/posts', json={
                'post_time': datetime(2018, 7, 9, 12, 55, 0),
                'section_name': 'sport',
                'context': "sport is great!",
            }, headers={'Authorization': "Token " + self.token})

            self.assertStatus(response, 400)

    def test_create_missing_post_time(self):
        with self.app.test_client() as client:
            response = client.post('/api/posts', json={
                'post_name': "today's sports",
                'section_name': 'sport',
                'context': "sport is great!",
            }, headers={'Authorization': "Token " + self.token})

            self.assertStatus(response, 400)

    def test_create_wrong_post_time(self):
        with self.app.test_client() as client:
            response = client.post('/api/posts', json={
                'post_name': "today's sports",
                'post_time': 'wrong time',
                'section_name': 'sport',
                'context': "sport is great!",
            }, headers={'Authorization': "Token " + self.token})

            self.assertStatus(response, 400)
            self.assertEqual(response.json, {'message': 'post_time not valid'})

    def test_create_missing_section_name(self):
        with self.app.test_client() as client:
            response = client.post('/api/posts', json={
                'post_name': "today's sports",
                'post_time': datetime(2018, 7, 9, 12, 55, 0),
                'context': "sport is great!",
            }, headers={'Authorization': "Token " + self.token})

            self.assertStatus(response, 400)

    def test_create_section_not_exist(self):
        with self.app.test_client() as client:
            response = client.post('/api/posts', json={
                'post_name': "today's sports",
                'post_time': datetime(2018, 7, 9, 12, 55, 0),
                'section_name': 'not exist!',
                'context': "sport is great!",
            }, headers={'Authorization': "Token " + self.token})

            self.assertStatus(response, 400)
            self.assertEqual(response.json, {'message': 'section not exist'})

    def test_create_missing_context(self):
        with self.app.test_client() as client:
            response = client.post('/api/posts', json={
                'post_name': "today's sports",
                'post_time': datetime(2018, 7, 9, 12, 55, 0),
                'section_name': 'sport',
            }, headers={'Authorization': "Token " + self.token})

            self.assertStatus(response, 400)

    def test_create_missing_token(self):
        with self.app.test_client() as client:
            response = client.post('/api/posts', json={
                'post_name': "today's sports",
                'post_time': datetime(2018, 7, 9, 12, 55, 0),
                'section_name': 'sport',
                'context': "sport is great!",
            })

            self.assertStatus(response, 401)
