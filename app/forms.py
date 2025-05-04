from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Regexp
import datetime


max_date = datetime.date.today()
def validate_date(form, field):
	if field.data > max_date:
		raise ValidationError("Date cannot be in the future.")


class LoginForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')

class SignUpForm(FlaskForm):
	username = StringField('Username', validators=[
		DataRequired(),
		Regexp( ##regex rule for usernames
			r'^\w+$', message="Username must contain only letters, numbers, or underscores.")
	])
	password = StringField('Password', validators=[
		DataRequired(),
		Regexp( ##regex rule for passwords
			r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
			message="Password must be at least 8 characters long and include a letter, a number, and a special character."
		)
	])
	age = DateField('Date of Birth', validators=[validate_date],
		render_kw={"max": max_date.strftime('%Y-%m-%d')})
	height = IntegerField('Height (in cm)', validators=[])
	weight = IntegerField('Weight (in kg)', validators=[])
	submit = SubmitField('Sign Up!')

class WorkoutForm(FlaskForm):
	exercise = StringField('Exercise', validators=[DataRequired()])
	date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
	sets = IntegerField('Sets', validators=[DataRequired()])
	reps = IntegerField('Reps', validators=[DataRequired()])
	calories_burned = IntegerField('Calories Burned', validators=[DataRequired()])
	weights = IntegerField('Weight', validators=[DataRequired()])
	submit = SubmitField('Save Workout')