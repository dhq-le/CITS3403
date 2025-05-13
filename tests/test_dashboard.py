from flask_login import login_user
from app.models import Usernames  # Adjust the import based on your application structure
from tests.base import BaseTestCase

class DashboardTestCase(BaseTestCase):
    def test_dashboard_access_authenticated(self):
        # Get the user
        user = Usernames.query.filter_by(username='existinguser').first()

        # Simulate login (ensure you're logging in correctly)
        self.client.post('/login', data={'username': 'existinguser', 'password': 'password'}, follow_redirects=True)

        # Access the dashboard
        response = self.client.get('/')  # Assuming the dashboard is at this route
        self.assertEqual(response.status_code, 200)  # Expect 200 OK status

    def test_dashboard_access_unauthenticated(self):
        response = self.client.get('/', follow_redirects=True)  # Ensure correct route
        self.assertIn(b'Login', response.data)  # Ensure login message appears

