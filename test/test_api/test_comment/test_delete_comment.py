from flask_testing import TestCase
from datetime import datetime
from forum import create_app
from forum.database import db
from forum.modules import User, Section, Comment


class TestDeleteComment(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.drop_all()
        db.create_all()

        admin = User.create('admin', 'admin', admin=True)
        poster = User.create('xua', 'strong_password')
        user = User.create('xua@wustl.edu', 'strong_password')
        self.user_id = user.user_id
        db.session.add(user)
        db.session.add(poster)
        db.session.add(admin)
        db.session.add(Section.create("sport"))
        db.session.commit()

        self.time = datetime(2018, 9, 10, 13, 00, 00)

        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
            })
            self.token = response.json['token']

            response = client.post('/api/tokens', json={
                'email': 'xua',
                'password': 'strong_password',
            })
            self.poster_token = response.json['token']

            response = client.post('/api/posts', json={
                'post_name': "today's sports",
                'post_time': datetime(2018, 6, 10, 12, 55, 0),
                'section_name': 'sport',
                'context': "sport is great!",
            }, headers={'Authorization': "Token " + self.poster_token})
            self.post_id = response.json['post_id']

            response = client.post('/api/comments', json={
                'post_id': self.post_id,
                'comment_time': self.time,
                'context': 'this is great!',
            }, headers={'Authorization': "Token " + self.token})
            self.comment_id = response.json['comment_id']

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_delete_comment(self):
        self.assertEqual(Comment.query.count(), 1)
        with self.app.test_client() as client:
            response = client.delete(f'/api/comment/{self.comment_id}',
                                     headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 200)
            self.assertEqual(response.json['comment_id'], self.comment_id)

        self.assertEqual(Comment.query.count(), 0)

    def test_delete_without_token(self):
        self.assertEqual(Comment.query.count(), 1)
        with self.app.test_client() as client:
            response = client.delete(f'/api/comment/{self.comment_id}')
            self.assertStatus(response, 401)

        self.assertEqual(Comment.query.count(), 1)

    def test_delete_by_poster(self):
        self.assertEqual(Comment.query.count(), 1)
        with self.app.test_client() as client:
            response = client.delete(f'/api/comment/{self.comment_id}',
                                     headers={'Authorization': "Token " + self.poster_token})
            self.assertStatus(response, 200)
            self.assertEqual(response.json['comment_id'], self.comment_id)

        self.assertEqual(Comment.query.count(), 0)

    def test_delete_by_admin(self):
        self.assertEqual(Comment.query.count(), 1)
        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'admin',
                'password': 'admin',
            })
            token = response.json['token']

            response = client.delete(f'/api/comment/{self.comment_id}',
                                     headers={'Authorization': "Token " + token})
            self.assertStatus(response, 200)
            self.assertEqual(response.json['comment_id'], self.comment_id)

        self.assertEqual(Comment.query.count(), 0)

    def test_delete_by_other(self):
        other = User.create('other', 'strong_password')
        db.session.add(other)
        db.session.commit()
        self.assertEqual(Comment.query.count(), 1)
        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'other',
                'password': 'strong_password',
            })
            token = response.json['token']

            response = client.delete(f'/api/comment/{self.comment_id}',
                                     headers={'Authorization': "Token " + token})
            self.assertEqual(response.json, {'message': "you don't have permission to delete"})
            self.assertStatus(response, 403)

        self.assertEqual(Comment.query.count(), 1)

    def test_delete_wrong_token(self):
        self.assertEqual(Comment.query.count(), 1)
        with self.app.test_client() as client:
            response = client.delete(f'/api/comment/{self.comment_id}',
                                     headers={'Authorization': "Token token"})
            self.assertStatus(response, 401)

        self.assertEqual(Comment.query.count(), 1)
