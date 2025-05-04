from app import db

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


class Friends(db.Model):
    # This is a composite key table
    __tablename__ = 'friends'
    user_id = db.Column(db.Integer, db.ForeignKey('usernames.id', name='fk_friends_user_id'), primary_key=True, nullable=False)
    friend_username = db.Column(db.String(80), db.ForeignKey('usernames.username', name='fk_friends_username'), primary_key=True, nullable=False)

    # create a relationship to the Usernames table using the user_id foreign key
    user = db.relationship('Usernames', foreign_keys=[user_id], backref='friends')

    def __repr__(self):
        return f"Friends(user_id={self.user_id!r}, friend_username={self.friend_username!r})"


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