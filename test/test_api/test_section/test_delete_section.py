from flask_testing import TestCase
from datetime import datetime
from forum import create_app
from forum.database import db
from forum.modules import User, Section, Post


class TestDeleteSection(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.drop_all()
        db.create_all()

        user = User.create('xua@wustl.edu', 'strong_password', admin=True)
        self.user_id = user.user_id
        db.session.add(user)
        db.session.commit()

        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
            })
            self.token = response.json['token']
            client.post('/api/sections', json={
                'section_name': 'sport',
            }, headers={'Authorization': "Token " + self.token})

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_delete_section(self):
        self.assertEqual(Section.query.count(), 1)
        with self.app.test_client() as client:
            response = client.delete(f'/api/section/sport',
                                     headers={'Authorization': "Token " + self.token})

            self.assertStatus(response, 200)
            self.assertEqual(response.json['section_name'], 'sport')

        self.assertEqual(Section.query.count(), 0)

    def test_delete_with_post(self):
        self.assertEqual(Section.query.count(), 1)
        with self.app.test_client() as client:
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
            self.assertEqual(Post.query.count(), 3)

            response = client.delete(f'/api/section/sport',
                                     headers={'Authorization': "Token " + self.token})

            self.assertStatus(response, 200)
            self.assertEqual(response.json['section_name'], 'sport')

        self.assertEqual(Section.query.count(), 0)
        self.assertEqual(Post.query.count(), 0)

    def test_delete_by_other(self):
        other = User.create('other', 'strong_password')
        db.session.add(other)
        db.session.commit()
        self.assertEqual(Section.query.count(), 1)
        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'other',
                'password': 'strong_password',
            })
            token = response.json['token']

            response = client.delete(f'/api/section/sport',
                                     headers={'Authorization': "Token " + token})
            self.assertEqual(response.json, {'message': 'user is not admin!'})
            self.assertStatus(response, 403)

        self.assertEqual(Section.query.count(), 1)

    def test_delete_wrong_token(self):
        self.assertEqual(Section.query.count(), 1)
        with self.app.test_client() as client:
            response = client.delete(f'/api/section/sport',
                                     headers={'Authorization': "Token token"})
            self.assertStatus(response, 401)

        self.assertEqual(Section.query.count(), 1)

    def test_delete_without_token(self):
        self.assertEqual(Section.query.count(), 1)
        with self.app.test_client() as client:
            response = client.delete(f'/api/section/sport')
            self.assertStatus(response, 401)

        self.assertEqual(Section.query.count(), 1)
