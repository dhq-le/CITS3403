from app import db
from datetime import datetime


class Usernames(db.Model):
    __tablename__ = 'usernames'
    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)  # although not necessary, it is a good practice to have an id column and quicker lookups
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    height = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    dob = db.Column(db.Integer, nullable=True)
    ## if we have time later add email here

    def __repr__(self):
        return f"Usernames(id={self.id!r}, username={self.username!r}, password={self.password!r}, height={self.height!r}, weight={self.weight!r}, dob={self.dob!r})"


class Friendship(db.Model):
    __tablename__ = 'friendships'
    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('usernames.id'), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey('usernames.id'), nullable=False)
    user   = db.relationship('Usernames', foreign_keys=[user_id], backref='friendships')
    friend = db.relationship('Usernames', foreign_keys=[friend_id])

class FriendRequest(db.Model):
    __tablename__ = 'friend_requests'
    id             = db.Column(db.Integer, primary_key=True)
    from_user_id   = db.Column(db.Integer, db.ForeignKey('usernames.id'), nullable=False)
    to_user_id     = db.Column(db.Integer, db.ForeignKey('usernames.id'), nullable=False)
    timestamp      = db.Column(db.DateTime, default=datetime.utcnow)
    from_user      = db.relationship('Usernames', foreign_keys=[from_user_id])
    to_user        = db.relationship('Usernames', foreign_keys=[to_user_id])


class WorkoutPlan:
    def __init__(self, owner, exercises):
        self.owner = owner
        self.exercises = exercises
    def __repr__(self):
        return f"WorkoutPlan(owner={self.owner!r}, exercises={self.exercises!r})"
    

class Workout(db.Model):
    __tablename__ = 'workout_history'
    workout_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usernames.id', name='fk_workouts_user_id'), nullable=False) ##add db.ForeignKey('user.username') when user table is added.
    exercise = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    calories_burned = db.Column(db.Integer)
    weights = db.Column(db.Integer)


    def __repr__(self):
        return (f"Workout(date={self.date!r}, exercise={self.exercise!r}, "
                f"sets={self.sets!r}, reps={self.reps!r}, "
                f"weights={self.weights!r}, calories_burned={self.calories_burned!r})")