from app import db

class WorkoutPlan:
    def __init__(self, owner, exercises):
        self.owner = owner
        self.exercises = exercises
    def __repr__(self):
        return f"WorkoutPlan(owner={self.owner!r}, exercises={self.exercises!r})"
    

class Workout:
    def __init__(self, date, exercise, sets_x_reps, weights, calories_burned):
        self.date = date
        self.exercise = exercise
        self.sets_x_reps = sets_x_reps
        self.weights = weights
        self.calories_burned = calories_burned
    
    def __repr__(self):
        return (f"Workout(date={self.date!r}, exercise={self.exercise!r}, "
                f"sets_x_reps={self.sets_x_reps!r}, weights={self.weights!r}, "
                f"calories_burned={self.calories_burned!r})")
        
class Usernames(db.Model):
    __tablename__ = 'usernames'
    id = db.Column(db.Integer, primary_key=True) # although not necessary, it is a good practice to have an id column and quicker lookups
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    height = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f"Usernames(id={self.id!r}, username={self.username!r}, password={self.password!r}, height={self.height!r}, weight={self.weight!r}, age={self.age!r})"
    
class Friends(db.Model):
    #This is a composite key table
    __tablename__ = 'friends'
    user_id = db.Column(db.Integer, db.ForeignKey('usernames.id'), primary_key=True, nullable=False)
    friend_username = db.Column(db.String(80), db.ForeignKey('usernames.username'), primary_key=True, nullable=False)

    # create a relationship to the Usernames table using the user_id foreign key
    user = db.relationship('Usernames', foreign_keys=[user_id], backref='friends')
    
    def __repr__(self):
        return f"Friends(user_id={self.user_id!r}, friend_username={self.friend_username!r})"