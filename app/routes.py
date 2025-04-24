from app import application
from app.models import WorkoutPlan
from flask import render_template, request, session, redirect, url_for

# Simple in-memory credentials dictionary
USER_DATA = {
    'username': 'testuser',
    'password': '123456',
}
 
# Login route
@application.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USER_DATA['username'] and password == USER_DATA['password']:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            error = 'Username or password is incorrect.'
    return render_template('login.html', error=error)

# Modified index route to require login
@application.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    plans = [
        WorkoutPlan(session['username'], ["Push-ups", "Squats", "Lunges"]),
        WorkoutPlan(session['username'], ["Running", "Cycling", "Swimming"]),
    ]
    return render_template('homepage.html', plans=plans) # this is server side rendering


# Optional logout route
@application.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))