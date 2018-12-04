from flask_testing import TestCase
from forum import create_app
from forum.database import db
from forum.modules import User, Section


class TestGetSections(TestCase):
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
                'section_name': 'default',
            }, headers={'Authorization': "Token " + self.token})
            client.post('/api/sections', json={
                'section_name': 'others',
            }, headers={'Authorization': "Token " + self.token})

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_sections(self):
        with self.app.test_client() as client:
            response = client.get('/api/sections')

            self.assertStatus(response, 200)
            self.assertListEqual(response.json, ['default', 'others'])
