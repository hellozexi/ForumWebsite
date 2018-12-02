from flask_testing import TestCase
from forum import create_app
from forum.database import db
from forum.modules import User


class TestUserRegister(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register(self):
        with self.app.test_client() as client:
            response = client.post('/api/users', json={
                'email': 'jason@wustl.edu',
                'password': 'strong_password',
            })
            self.assertStatus(response, 201)
            self.assertEqual(response.json, {"message": "success"})
            # register check
            self.assertEqual(len(User.query.all()), 1)
            user = User.query.filter_by(email='jason@wustl.edu').first()
            self.assertTrue(user.verify('strong_password'))

    def test_without_email(self):
        with self.app.test_client() as client:
            response = client.post('/api/users', json={
                'password': 'strong_password',
            })
            self.assertEqual(response.json, {'message': {'email': 'field missing'}})
            self.assertEqual(len(User.query.all()), 0)
            self.assertIsNone(User.query.filter_by(email='jason@wustl.edu').first())

    def test_without_password(self):
        with self.app.test_client() as client:
            response = client.post('/api/users', json={
                'email': 'jason@wustl.edu',
            })
            self.assertEqual(response.json, {'message': {'password': 'field missing'}})
            self.assertEqual(len(User.query.all()), 0)
            self.assertIsNone(User.query.filter_by(email='jason@wustl.edu').first())

    def test_email_already_exist(self):
        with self.app.test_client() as client:
            client.post('/api/users', json={
                'email': 'jason@wustl.edu',
                'password': 'strong_password',
            })
            response = client.post('/api/users', json={
                'email': 'jason@wustl.edu',
                'password': 'strong_password',
            })
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json, {'message': 'user already exist'})
            self.assertEqual(len(User.query.all()), 1)
