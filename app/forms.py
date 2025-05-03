from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class WorkoutForm(FlaskForm):
	exercise = StringField('Exercise', validators=[DataRequired()])
	date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
	sets = IntegerField('Sets', validators=[DataRequired()])
	reps = IntegerField('Reps', validators=[DataRequired()])
	calories_burned = IntegerField('Calories Burned', validators=[DataRequired()])
	weights = IntegerField('Weight', validators=[DataRequired()])
	submit = SubmitField('Save Workout')