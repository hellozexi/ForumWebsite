from flask_testing import TestCase
from forum import create_app
from forum.database import db
from forum.modules import User, Section, BlockItem


class TestBlock(TestCase):

    SQLALCHEMY_DATABASE_URI = "sqlite:///db_for_test.db"
    TESTING = True

    def create_app(self):
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create(self):
        self.assertEqual(len(BlockItem.query.all()), 0)
        user = User.create('xua@wustl.edu', 'password')
        section = Section.create('sports')
        block = BlockItem(user_id=user.user_id)
        section.blocks.append(block)
        db.session.add(user)
        db.session.add(section)
        db.session.commit()
        self.assertEqual(len(BlockItem.query.all()), 1)

    def test_search(self):
        user = User.create('xua@wustl.edu', 'password')
        user_id = user.user_id
        section = Section.create('sports')
        block = BlockItem(user_id=user_id)
        section.blocks.append(block)
        db.session.add(user)
        db.session.add(section)
        db.session.commit()

        section = Section.query.filter_by(section_name='sports').first()
        block = BlockItem.query.with_parent(section).filter_by(user_id=user_id).first()
        self.assertIsNotNone(block)
        self.assertEqual(block.user_id, user_id)

    def test_delete(self):
        user = User.create('xua@wustl.edu', 'password')
        user_id = user.user_id
        section = Section.create('sports')
        block = BlockItem(user_id=user_id)
        section.blocks.append(block)
        db.session.add(user)
        db.session.add(section)
        db.session.commit()

        section = Section.query.filter_by(section_name='sports').first()
        block = BlockItem.query.with_parent(section).filter_by(section_name='sports').first()
        self.assertIsNotNone(block)
        self.assertEqual(block.user_id, user_id)

        db.session.delete(block)
        self.assertEqual(len(BlockItem.query.all()), 0)
