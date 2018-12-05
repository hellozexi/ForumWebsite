from flask_testing import TestCase
from forum import create_app
from forum.database import db
from forum.modules import User, Section, BlockItem


class TestCreateBlock(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.drop_all()
        db.create_all()

        admin = User.create('admin', 'admin', admin=True)
        xua = User.create('xua', 'xua', admin=False)
        db.session.add(xua)
        db.session.add(admin)
        db.session.commit()

        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'admin',
                'password': 'admin',
            })
            self.token = response.json['token']

            client.post('/api/sections', json={
                'section_name': 'sport',
            }, headers={'Authorization': "Token " + self.token})

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_block(self):
        self.assertEqual(BlockItem.query.count(), 0)
        with self.app.test_client() as client:
            response = client.post('/api/blocks', json={
                'section_name': 'sport',
                'user_email': 'xua'
            }, headers={'Authorization': "Token " + self.token})

            self.assertStatus(response, 201)
            self.assertEqual(response.json['section_name'], 'sport')
            self.assertEqual(response.json['email'], 'xua')

        self.assertEqual(BlockItem.query.count(), 1)

    def test_create_block_already_exist(self):
        self.assertEqual(BlockItem.query.count(), 0)
        with self.app.test_client() as client:
            client.post('/api/blocks', json={
                'section_name': 'sport',
                'user_email': 'xua'
            }, headers={'Authorization': "Token " + self.token})
            self.assertEqual(BlockItem.query.count(), 1)
            response = client.post('/api/blocks', json={
                'section_name': 'sport',
                'user_email': 'xua'
            }, headers={'Authorization': "Token " + self.token})
            self.assertStatus(response, 400)
            self.assertEqual(response.json, {'message': 'block already exist'})

        self.assertEqual(BlockItem.query.count(), 1)

    def test_without_token(self):
        self.assertEqual(BlockItem.query.count(), 0)
        with self.app.test_client() as client:
            response = client.post('/api/blocks', json={
                'section_name': 'sport',
                'user_email': 'xua'
            })
            self.assertStatus(response, 401)

        self.assertEqual(BlockItem.query.count(), 0)

    def test_not_admin(self):
        self.assertEqual(BlockItem.query.count(), 0)
        with self.app.test_client() as client:
            response = client.post('/api/tokens', json={
                'email': 'xua',
                'password': 'xua',
            })
            token = response.json['token']

            response = client.post('/api/blocks', json={
                'section_name': 'sport',
                'user_email': 'xua'
            }, headers={'Authorization': "Token " + token})

            self.assertStatus(response, 403)
            self.assertEqual(response.json, {'message': 'user is not admin!'})

        self.assertEqual(BlockItem.query.count(), 0)
