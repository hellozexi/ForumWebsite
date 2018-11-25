from flask_testing import TestCase
from forum import create_app
from forum.database import db
from forum.modules import User


class TestUser(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_add_user(self):
        self.assertEqual(len(User.query.all()), 0)

        user = User.create('xua@wustl.edu', 'strong_password')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(len(User.query.all()), 1)

        user = User.create('xua@sss.edu', 'strong_password')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(len(User.query.all()), 2)

    def test_query_user_email(self):
        self.assertEqual(len(User.query.all()), 0)

        email, password = 'xua@wustl.edu', 'strong_password'
        user = User.create(email, password)
        user_id = user.user_id
        db.session.add(user)
        db.session.commit()
        self.assertEqual(len(User.query.all()), 1)

        query_email = User.query.filter_by(email=email).first()
        self.assertEqual(query_email.email, email)
        self.assertEqual(query_email.user_id, user_id)
        self.assertTrue(query_email.verify(password))

    def test_query_user_id(self):
        self.assertEqual(len(User.query.all()), 0)

        email, password = 'xua@wustl.edu', 'strong_password'
        user = User.create(email, password)
        user_id = user.user_id
        db.session.add(user)
        db.session.commit()
        self.assertEqual(len(User.query.all()), 1)

        query_email = User.query.filter_by(user_id=user_id).first()
        self.assertEqual(query_email.email, email)
        self.assertEqual(query_email.user_id, user_id)
        self.assertTrue(query_email.verify(password))

    def test_query_user_not_exist(self):
        self.assertIsNone(User.query.filter_by(email='this@xua').first())
        self.assertIsNone(User.query.filter_by(user_id='sdfsdf').first())

    def test_verify_password(self):
        email, password = 'xua@wustl.edu', 'strong_password'
        user = User.create(email, password)
        user_id = user.user_id
        db.session.add(user)
        db.session.commit()

        query_email = User.query.filter_by(user_id=user_id).first()
        self.assertTrue(query_email.verify(password))
