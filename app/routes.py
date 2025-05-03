from flask import Blueprint, render_template, session, redirect, url_for, request
from app.forms import LoginForm
from app.models import WorkoutPlan, Workout

routes_blueprint = Blueprint('routes', __name__)

@routes_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        if form.username.data == 'testuser' and form.password.data == '123456':
            session['logged_in'] = True
            session['username'] = form.username.data
            return redirect(url_for('routes.index'))
        error = 'Invalid username or password.'
    elif request.method == 'POST':
        error = 'Form validation failed.'
    return render_template('login.html', form=form, error=error)

@routes_blueprint.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))
    plans = [
        WorkoutPlan(session['username'], ["Push-ups", "Squats", "Lunges"]),
        WorkoutPlan(session['username'], ["Running", "Cycling", "Swimming"]),
    ]
    return render_template('home.html', plans=plans, username=session['username'])

@routes_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@routes_blueprint.route('/profile')
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    #### Temp hardcoded data until we get a working
    workout_history = [
        Workout(date=20250427, exercise='Bench Press', sets=4, reps=10, weights=60, calories_burned=200),
        Workout(date=20250426, exercise='Deadlift', sets=5, reps=5, weights=100, calories_burned=300),
        Workout(date=20250425, exercise='Squats', sets=4, reps=8, weights=80, calories_burned=250),
        Workout(date=20250425, exercise='Running', sets=None, reps=None, weights=None, calories_burned=400),
        Workout(date=20250424, exercise='Cycling', sets=None, reps=None, weights=None, calories_burned=350),
    ]

    return render_template('profile.html', username=session['username'], workout_history=workout_history)

