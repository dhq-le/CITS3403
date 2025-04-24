class WorkoutPlan:
    def __init__(self, owner, exercises):
        self.owner = owner
        self.exercises = exercises
    def __repr__(self):
        return f"WorkoutPlan(owner={self.owner!r}, exercises={self.exercises!r})"
        