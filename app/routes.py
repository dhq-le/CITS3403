from flask import render_template, session, redirect, url_for, request
from app import application
from app.forms import LoginForm
from app.models import WorkoutPlan, Workout

@application.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        if form.username.data == 'testuser' and form.password.data == '123456':
            session['logged_in'] = True
            session['username'] = form.username.data
            return redirect(url_for('index'))
        error = 'Invalid username or password.'
    elif request.method == 'POST':
        error = 'Form validation failed.'
    return render_template('login.html', form=form, error=error)

@application.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    plans = [
        WorkoutPlan(session['username'], ["Push-ups", "Squats", "Lunges"]),
        WorkoutPlan(session['username'], ["Running", "Cycling", "Swimming"]),
    ]
    return render_template('home.html', plans=plans)

@application.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@application.route('/profile')
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    workout_history = [
        Workout('2025-04-27', 'Bench Press', '4x10', '60kg', 200),
        Workout('2025-04-26', 'Deadlift', '5x5', '100kg', 300),
        Workout('2025-04-25', 'Squats', '4x8', '80kg', 250),
        Workout("2025-04-25", "Running", "30min", "-", 400),
        Workout("2025-04-24", "Cycling", "45min", "-", 350),
    ]
    
    return render_template('profile.html', username=session['username'], workout_history=workout_history)

