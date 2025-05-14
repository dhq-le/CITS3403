import unittest
from app import create_app, db
from app.models import Usernames, FriendRequest, Friendship, Workout
from werkzeug.security import generate_password_hash

import unittest
from app import create_app, db
from app.models import Usernames

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.app = create_app('config.TestingConfig')  # Use the test config
        self.client = self.app.test_client()

        with self.app.app_context():  # Ensure app context is pushed
            db.create_all()  # Create all the tables for tests

    def tearDown(self):
        """Tear down test environment"""
        with self.app.app_context():  # Ensure app context is pushed
            db.session.remove()  # Remove session after each test
            db.drop_all()  # Drop all tables after tests


