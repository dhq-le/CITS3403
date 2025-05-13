import unittest
from datetime import datetime
from app import create_app, db
from app.models import Usernames, Friendship, FriendRequest, Workout

class ModelsTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create sample users
        self.user1 = Usernames(username='alice', password='password1', height=160, weight=60)
        self.user2 = Usernames(username='bob', password='password2', height=175, weight=80)
        db.session.add(self.user1)
        db.session.add(self.user2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = Usernames.query.filter_by(username='alice').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.weight, 60)

    def test_friendship_creation(self):
        friendship = Friendship(user_id=self.user1.id, friend_id=self.user2.id)
        db.session.add(friendship)
        db.session.commit()
        self.assertEqual(Friendship.query.count(), 1)
        self.assertEqual(friendship.user.username, 'alice')

    def test_friend_request(self):
        req = FriendRequest(from_user_id=self.user1.id, to_user_id=self.user2.id)
        db.session.add(req)
        db.session.commit()
        result = FriendRequest.query.first()
        self.assertEqual(result.from_user.username, 'alice')
        self.assertEqual(result.to_user.username, 'bob')
        self.assertTrue(isinstance(result.timestamp, datetime))

    def test_workout_creation(self):
        workout = Workout(
            user_id=self.user1.id,
            exercise="Push Ups",
            date=datetime.utcnow().date(),
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

if __name__ == '__main__':
    unittest.main()
