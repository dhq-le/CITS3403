from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, DateField, IntegerField, ValidationError
from wtforms.validators import DataRequired, Regexp, NumberRange,Length
import datetime


max_date = datetime.date.today()
def validate_date(form, field):
	if field.data > max_date:
		raise ValidationError("Date cannot be in the future.")


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('password', validators=[DataRequired()])
    submit   = SubmitField('login')

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

class WorkoutForm(FlaskForm):
	exercise = StringField('Exercise', validators=[DataRequired()])
	date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired(), validate_date],
			render_kw={"max": max_date.strftime('%Y-%m-%d')})
	sets = IntegerField('Sets', validators=[DataRequired()])
	reps = IntegerField('Reps', validators=[DataRequired()])
	calories_burned = IntegerField('Calories Burned', validators=[DataRequired()])
	weights = IntegerField('Weight', validators=[DataRequired()])
	submit = SubmitField('Save Workout')


class AddFriendForm(FlaskForm):
    friend_username = StringField(
        'username',
        validators=[DataRequired(), Length(1, 64)]
    )
    submit = SubmitField('Add friend')