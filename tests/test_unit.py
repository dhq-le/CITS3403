import unittest
from app import create_app, db
from app.models import Usernames, Friendship, FriendRequest, Workout
from flask.testing import FlaskClient
from datetime import datetime, timezone

class PageTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.drop_all()
        db.create_all()

        # Create test client
        self.client: FlaskClient = self.app.test_client(use_cookies=True)

        # Create sample users
        self.user1 = Usernames(
            username='alice',
            height=160,
            weight=60
        )
        self.user1.set_password('password1')
        self.user2 = Usernames(
            username='bob',
            height=175,
            weight=80
        )
        self.user2.set_password('password2')
        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    ###### Authentication Test Cases
    def test_register_user(self):
        # Set up the app context
        with self.app_context:  # Ensure the app context is available
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
            self.assertIn(b'Account created successfully', response.data)
            self.assertEqual(response.status_code, 200)  # Ensure we get a successful response


    ###### Login-Dashboard Test Case
    def test_dashboard_access_authenticated(self):
        # Simulate login (ensure you're logging in correctly)
        response = self.client.post(
            '/login',
            data={'username': 'alice',
                  'password': 'password1'},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

        # Access the dashboard
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_access_unauthenticated(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertIn(b'Login', response.data)


    ##### DATABASE TESTS #####
    def test_user_creation(self):
        user = Usernames.query.filter_by(username='alice').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.weight, 60)

    def test_friendship_creation(self):
        friendship = Friendship(user_id=self.user1.id, friend_id=self.user2.id)
        db.session.add(friendship)
        db.session.commit()
        db.session.refresh(friendship)
        self.assertEqual(Friendship.query.count(), 1)
        self.assertEqual(friendship.user.username, 'alice')

    def test_friend_request(self):
        req = FriendRequest(from_user_id=self.user1.id, to_user_id=self.user2.id)
        db.session.add(req)
        db.session.commit()
        result = FriendRequest.query.first()
        db.session.refresh(req)
        self.assertEqual(result.from_user.username, 'alice')
        self.assertEqual(result.to_user.username, 'bob')
        self.assertTrue(isinstance(result.timestamp, datetime))

    def test_workout_creation(self):
        workout = Workout(
            user_id=self.user1.id,
            exercise="Push Ups",
            date=datetime.now(timezone.utc).date(),
            sets=3,
            reps=12,
            calories_burned=100,
            weights=0,
            completion=True
        )
        db.session.add(workout)
        db.session.commit()
        w = Workout.query.first()
        self.assertEqual(w.exercise, "Push Ups")
        self.assertTrue(w.completion)
        self.assertEqual(w.user_id, self.user1.id)
