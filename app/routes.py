from flask import render_template, session, redirect, url_for, request
from app import application
from app.forms import LoginForm
from app.models import WorkoutPlan

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
    return render_template('homepage.html', plans=plans)

@application.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))