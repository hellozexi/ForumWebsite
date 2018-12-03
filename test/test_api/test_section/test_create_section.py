from flask_testing import TestCase
from forum import create_app
from forum.database import db
from forum.modules import User, Section


class TestCreateSection(TestCase):
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

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_section(self):
        self.assertEqual(Section.query.count(), 0)
        with self.app.test_client() as client:
            response = client.post('/api/sections', json={
                'section_name': 'sport',
            }, headers={'Authorization': "Token " + self.token})

            self.assertStatus(response, 201)
            self.assertEqual(response.json['section_name'], 'sport')

        self.assertEqual(Section.query.count(), 1)
