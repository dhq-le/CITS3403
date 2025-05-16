from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, ValidationError, SelectField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Regexp, NumberRange, Length, Optional
import datetime
import json
from pathlib import Path


max_date = datetime.date.today()
def validate_date(form, field):
        if field.data and field.data > max_date:
                raise ValidationError("Date cannot be in the future.")


class LoginForm(FlaskForm):
        username = StringField('username', validators=[DataRequired(), Length(1, 64)])
        password = PasswordField('password', validators=[DataRequired()])
        submit   = SubmitField('Login')

class SignUpForm(FlaskForm):
        username = StringField('Username', validators=[
                DataRequired(),
                Regexp( ##regex rule for usernames
                        r'^\w+$', message="Username must contain only letters, numbers, or underscores.")
        ])
        password = PasswordField('Password', validators=[
                DataRequired(),
                Length(min=8, message="Password must be at least 8 characters long.")
        ])
        height = IntegerField('Height (in cm)', validators=[
                DataRequired(),
                NumberRange(min=0, message="Height must be greater than zero.")
        ])
        weight = IntegerField('Weight (in kg)', validators=[
                DataRequired(),
                NumberRange(min=0, message="Weight must be greater than zero.")
        ])
        dob = DateField('Date of Birth', validators=[validate_date],
                        render_kw={"max": max_date.strftime('%Y-%m-%d')})
        submit = SubmitField('Sign Up!')

class MuscleForm(FlaskForm):
        muscle = SelectField('Target Muscle Group', validators=[DataRequired()])
        submit = SubmitField('Get Exercises')

        def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                # Load muscle groups from local JSON
                json_path = Path(__file__).resolve().parent.parent / 'static' / 'data' / 'exercises.json'
                if json_path.exists():
                        with open(json_path) as f:
                                data = json.load(f)
                                self.muscle.choices = [(key, key.capitalize()) for key in data.keys()]
                else:
                        self.muscle.choices = []

class WorkoutForm(FlaskForm):
        exercise = StringField('Exercise', validators=[DataRequired()])
        date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
        sets = IntegerField('Sets', validators=[DataRequired(), NumberRange(min=0, message="Sets must be 0 or greater.")])
        reps = IntegerField('Reps', validators=[DataRequired(), NumberRange(min=0, message="Reps must be 0 or greater.")])
        # calories_burned = IntegerField('Calories Burned', validators=[DataRequired()]) this will be worked on the backend
        weights = IntegerField('Weight', validators=[DataRequired()])
        completion_status = BooleanField('Completion Status')
        next = HiddenField()  # <-- Add this line
        submit = SubmitField('Save Workout')


class AddFriendForm(FlaskForm):
        friend_username = StringField(
                'username',
                validators=[DataRequired(), Length(1, 64)]
        )
        submit = SubmitField('Add friend')

class EditProfileForm(FlaskForm):
        username = StringField('Username', validators=[
                DataRequired(),
                Regexp( ##regex rule for usernames
                        r'^\w+$', message="Username must contain only letters, numbers, or underscores.")
        ])
        password = PasswordField('Password', validators=[
                Length(min=8, message="Password must be at least 8 characters long.")
        ])
        height = IntegerField('Height (in cm)', validators=[
                Optional(),
                NumberRange(min=0, message="Height must be greater than zero.")
        ])
        dob = DateField('Date of Birth', validators=[Optional(), validate_date],
                        render_kw={"max": max_date.strftime('%Y-%m-%d')})
        submit = SubmitField('Update Profile')