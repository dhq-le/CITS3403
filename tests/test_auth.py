from flask_login import user_needs_refresh

from tests.base import BaseTestCase
from app.models import Usernames
from app import db


class AuthTestCase(BaseTestCase):
        def test_register_user(self):
                # Set up the app context
                with self.app.app_context():  # Ensure the app context is available
                        # Simulate registration by sending a POST request
                        response = self.client.post('/signup', data={
                                'username': 'newuser',
                                'password': 'StrongPass1!',
                                'height': '175',
                                'weight': '70',
                                'dob': '2000-01-01'
                        }, follow_redirects=True)

                        # Query the database to check if the user was created
                        user = Usernames.query.filter_by(username='newuser').first()

                        self.assertIsNotNone(user)  # Assert that the user is created
                        self.assertEqual(response.status_code, 200)  # Ensure we get a successful response
