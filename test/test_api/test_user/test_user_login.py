from itsdangerous import TimestampSigner
from flask_testing import TestCase
from forum import create_app
from forum.database import db
from forum.modules import User
from forum.api import signer


class TestUserLogin(TestCase):
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
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_login(self):
        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'xua@wustl.edu',
                'password': 'strong_password',
            })
            self.assertStatus(response, 201)
            token = response.json['token']
            self.assertEqual(signer.unsign(token, max_age=99999).decode(), self.user_id)

    def test_email_missing(self):
        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'password': 'strong_password',
            })
            self.assertStatus(response, 400)
            self.assertEqual(response.json, {'message': {'email': 'field missing'}})

    def test_password_missing(self):
        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'xua@wustl.edu',
            })
            self.assertStatus(response, 400)
            self.assertEqual(response.json, {'message': {'password': 'field missing'}})
