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
        