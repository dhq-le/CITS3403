from app import db

class WorkoutPlan:
    def __init__(self, owner, exercises):
        self.owner = owner
        self.exercises = exercises
    def __repr__(self):
        return f"WorkoutPlan(owner={self.owner!r}, exercises={self.exercises!r})"
    

class Workout(db.Model):
    __tablename__ = 'workout_history'
    workout_id = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False) ##add db.ForeignKey('user.username') when user table is added.
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
