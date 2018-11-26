from flask_testing import TestCase
from forum import create_app
from forum.database import db
from forum.modules import Section


class TestSection(TestCase):

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
        self.assertEqual(len(Section.query.all()), 0)

        section = Section.create('sports')
        db.session.add(section)
        db.session.commit()
        self.assertEqual(len(Section.query.all()), 1)

        section = Section.create('computer')
        db.session.add(section)
        db.session.commit()
        self.assertEqual(len(Section.query.all()), 2)
