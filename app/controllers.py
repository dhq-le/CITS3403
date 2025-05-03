from flask import render_template, session, redirect, url_for, request, flash
from app.forms import *
from app.models import WorkoutPlan, Workout, Usernames, Friends
from app import db
import hashlib

## sign up page
def signup():
    form = SignUpForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            ## check against database, ensure these dont already exist
            if usernames.query.filter_by(username=username) is not None: ##### this is untested, make signup page and test
				error = "Username is already taken."
            ## add password salting and hashing
            new_user = Usernames(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()

## login page
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

    workout_history = Workout.query.filter_by(username=session['username']).all()
    return render_template('profile.html', username=session['username'], workout_history=workout_history)

## start course page
def log_workout():
    form = WorkoutForm()
    if form.validate_on_submit():
        workout = Workout(
        	username=session['username'],
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
