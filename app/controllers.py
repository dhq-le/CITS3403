
import sqlite3
import requests
from flask import jsonify, render_template, session, redirect, url_for, request, flash
from sqlalchemy import text
from app.forms import *
from app.models import WorkoutPlan, Workout, Usernames, Friends
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


## sign up page
def signup():
    form = SignUpForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            height = form.height.data
            weight = form.weight.data
            dob = form.dob.data
            ## check against database, ensure these dont already exist
            if Usernames.query.filter_by(username=username).first() is not None:
                error = "Username is already taken. Please select a new username."
                return render_template('signup.html', form=form, error=error)
            else:
                hashed = generate_password_hash(password, method='pbkdf2:sha256')
                new_user = Usernames(username=username, password=hashed, height=height, weight=weight, dob=dob)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('routes.login'))
    return render_template('signup.html', form=form, error=error)   

## login page
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        temp_username = form.username.data
        if not temp_username:
            error = 'Please enter a username.'
        else:
            user = Usernames.query.filter_by(username=temp_username).first()
            if user is None:
                error = 'Username not found.'
            elif not check_password_hash(user.password, form.password.data):
                error = 'Incorrect password.'
            else:
                session['logged_in'] = True
                session['username'] = temp_username
                return redirect(url_for('routes.index'))
    elif request.method == 'POST':
        error = 'Form validation failed.'
    return render_template('login.html', form=form, error=error)

## logout page
def logout():
    session.clear()
    return redirect(url_for('routes.login'))

## index/dashboard page
def index():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))
    plans = [
        WorkoutPlan(session['username'], ["Push-ups", "Squats", "Lunges"]),
        WorkoutPlan(session['username'], ["Running", "Cycling", "Swimming"]),
    ]
    return render_template('home.html', plans=plans, username=session['username'])

## profile page
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))
    user = Usernames.query.filter_by(username=session['username']).first()
    workout_history = Workout.query.filter_by(user_id=user.id).all()
    return render_template('profile.html', username=session['username'], workout_history=workout_history)

##API for training

API_NINJAS_KEY = 'zeYa187WE3R+mjgiR3qX5A==lQSGTcv8N1sipKiU'  # Replace with your actual API key

def start_course():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))

    form = MuscleForm()
    # API Ninjas valid muscle names
    muscles = ['abdominals', 'biceps', 'calves', 'chest', 'forearms',
               'glutes', 'hamstrings', 'lats', 'lower_back', 'middle_back',
               'neck', 'quadriceps', 'traps', 'triceps']
    form.muscle.choices = [(m, m.capitalize()) for m in muscles]
    exercises = []

    if request.is_json:
        muscle = request.json.get("muscle_id")
        api_url = f"https://api.api-ninjas.com/v1/exercises?muscle={muscle}"
        response = requests.get(api_url, headers={'X-Api-Key': API_NINJAS_KEY})
        if response.status_code == requests.codes.ok:
            print("API Response:", response.text)
            exercises = response.json()
        else:
            print("API Error:", response.status_code, response.text)
            exercises = []
        return jsonify(exercises=exercises)

    return render_template('exercise.html', form=form, exercises=exercises)
def log_workout():
    form = WorkoutForm()
    if form.validate_on_submit():
        workout = Workout(
        	user_id=Usernames.query.filter_by(username=session['username']).first().id,
            exercise=form.exercise.data,
            date=form.date.data.strftime('%Y%m%d'),
            sets=form.sets.data,
            reps=form.reps.data,
            calories_burned=form.calories_burned.data,
            weights=form.weights.data
        )
        db.session.add(workout)
        db.session.commit()
        flash('Workout logged!')
        return redirect(url_for('routes.index'))
    return render_template('log.html', form=form)

## calorie data chart
def calories_data():
    query = text("""  
        SELECT date, SUM(calories_burned) AS calories
        FROM workout_history
        GROUP BY date
        ORDER BY date ASC
    """)
    result = db.session.execute(query).fetchall()

    data = [{"date": str(row.date), "calories": row.calories} for row in result]
    return jsonify(data)
