from flask_testing import TestCase
from datetime import datetime
from forum import create_app
from forum.database import db
from forum.modules import User, Section


class TestGetComments(TestCase):
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
            response = client.post('/api/posts', json={
                'post_name': "today's sports",
                'post_time': datetime.now(),
                'section_name': 'sport',
                'context': "sport is great!",
            }, headers={'Authorization': "Token " + self.token})
            self.post_id = response.json['post_id']

            client.post('/api/comments', json={
                'post_id': self.post_id,
                'comment_time': datetime(2018, 7, 10, 12, 55, 0),
                'context': 'this is great!',
            }, headers={'Authorization': "Token " + self.token})
            client.post('/api/comments', json={
                'post_id': self.post_id,
                'comment_time': datetime(2018, 8, 10, 12, 55, 0),
                'context': 'this is worse!',
            }, headers={'Authorization': "Token " + self.token})
            client.post('/api/comments', json={
                'post_id': self.post_id,
                'comment_time': datetime(2018, 9, 10, 12, 55, 0),
                'context': 'this is common!',
            }, headers={'Authorization': "Token " + self.token})

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_by_user(self):
        with self.app.test_client() as client:
            response = client.get(f'/api/comments?user_id={self.user_id}')
            self.assertEqual(len(response.json), 3)
            contexts = [comment['context'] for comment in response.json]
            self.assertListEqual(contexts, ['this is great!', 'this is worse!', 'this is common!'])

    def test_get_by_post(self):
        with self.app.test_client() as client:
            response = client.get(f'/api/comments?post_id={self.post_id}')
            self.assertEqual(len(response.json), 3)
            contexts = [comment['context'] for comment in response.json]
            self.assertListEqual(contexts, ['this is great!', 'this is worse!', 'this is common!'])
