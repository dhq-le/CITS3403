from app import db
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Usernames(UserMixin, db.Model):
    __tablename__ = 'usernames'
    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)  # although not necessary, it is a good practice to have an id column and quicker lookups
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    height = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Integer, nullable=True)
    dob = db.Column(db.Date, nullable=True)
    profile_pic = db.Column(db.String(120), nullable=True)  # this will be a link to the image, not the image itself
    ## if we have time later add email here

    #create a get and set method for the password. 
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password = generate_password_hash(password)

    def check_password(self, password):
      """Verify a plaintext password against the stored hash."""
      return check_password_hash(self.password, password)

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
    timestamp      = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    from_user      = db.relationship('Usernames', foreign_keys=[from_user_id])
    to_user        = db.relationship('Usernames', foreign_keys=[to_user_id])


class WorkoutPlan:
    def __init__(self, exercise, sets, reps, weights):
        self.exercise = exercise
        self.sets = sets
        self.reps = reps
        self.weights = weights
    def __repr__(self):
        return f"WorkoutPlan(exercise={self.exercise!r}, sets={self.sets!r}, reps={self.reps!r}, weights={self.weights!r})"
    

class Workout(db.Model):
    __tablename__ = 'workout_history'
    workout_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usernames.id', name='fk_workouts_user_id'), nullable=False) ##add db.ForeignKey('user.username') when user table is added.
    exercise = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    calories_burned = db.Column(db.Integer)
    weights = db.Column(db.Integer)
    completion = db.Column(db.Boolean, default=False)


    def __repr__(self):
        return (f"Workout(date={self.date!r}, exercise={self.exercise!r}, "
                f"sets={self.sets!r}, reps={self.reps!r}, "
                f"weights={self.weights!r}, calories_burned={self.calories_burned!r})")