import json
from pathlib import Path
from app import create_app, db
from app.models import Usernames, Friendship, FriendRequest, Workout
from faker import Faker
import random
import datetime

app = create_app()

with app.app_context():
    fake = Faker()
    Faker.seed(0)
    random.seed(0)

    db.drop_all()
    db.create_all()

    # ---------- Load Exercises from JSON ----------
    exercises_path = Path(__file__).resolve().parent / 'app' / 'static' / 'data' / 'exercises.json'
    with open(exercises_path) as f:
        exercises = json.load(f)

    # ---------- USERS ----------
    users = []
    for _ in range(20):
        name = fake.unique.first_name().lower()
        dob = datetime.date(random.randint(1990, 2005), random.randint(1, 12), random.randint(1, 28))

        user = Usernames(
            username=name,
            height=random.randint(150, 200),
            weight=random.randint(50, 100),
            dob=dob,
        )
        user.set_password("password123")
        db.session.add(user)
        users.append(user)

    db.session.commit()
    print("✅ Users created")

    # ---------- FRIENDSHIPS ----------
    friendships = set()
    while len(friendships) < 30:
        u1, u2 = random.sample(users, 2)
        if (u1.id, u2.id) not in friendships and (u2.id, u1.id) not in friendships:
            db.session.add(Friendship(user_id=u1.id, friend_id=u2.id))
            friendships.add((u1.id, u2.id))
    db.session.commit()
    print("✅ Friendships created")

    # ---------- FRIEND REQUESTS ----------
    friend_requests = set()
    while len(friend_requests) < 10:
        sender, receiver = random.sample(users, 2)
        if (sender.id, receiver.id) not in friendships and (sender.id, receiver.id) not in friend_requests:
            db.session.add(FriendRequest(from_user_id=sender.id, to_user_id=receiver.id))
            friend_requests.add((sender.id, receiver.id))
    db.session.commit()
    print("✅ Friend requests created")

    # ---------- WORKOUTS ----------
    for user in users:
        for _ in range(random.randint(2, 5)):
            date = fake.date_between(start_date="-30d", end_date="today")
            muscle_group = random.choice(list(exercises.keys()))
            exercise_dict = random.choice(exercises[muscle_group])
            exercise = exercise_dict['name']
            sets = random.randint(2, 5)
            reps = random.randint(8, 15)
            weights = random.choice([0, 20, 40, 60])
            calories = sets * reps * (1 + weights // 10)

            workout = Workout(
                user_id=user.id,
                date=date,
                exercise=exercise,
                sets=sets,
                reps=reps,
                weights=weights,
                calories_burned=calories,
                completion=random.choice([True, False])
            )
            db.session.add(workout)

    db.session.commit()
    print("✅ Workouts created")
    print("🎉 All tables populated successfully from JSON-based exercises.")
