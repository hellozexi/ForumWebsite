from flask_testing import TestCase
from datetime import datetime
from forum import create_app
from forum.database import db
from forum.modules import User, Section


class TestModifyComment(TestCase):
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

        self.time = datetime(2018, 9, 10, 13, 00, 00)

        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
            })
            self.token = response.json['token']

            response = client.post('/api/posts', json={
                'post_name': "today's sports",
                'post_time': datetime(2018, 6, 10, 12, 55, 0),
                'section_name': 'sport',
                'context': "sport is great!",
            }, headers={'Authorization': "Token " + self.token})
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

    def test_modify_comment(self):
        with self.app.test_client() as client:
            response = client.put(f'/api/comment/{self.comment_id}', json={
                'context': 'this is worse!'
            }, headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 200)

            response = client.get(f'/api/comment/{self.comment_id}')
            self.assertStatus(response, 200)
            self.assertEqual(response.json['context'], 'this is worse!')
