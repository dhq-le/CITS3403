import os
from flask import app, jsonify, render_template, session, redirect, url_for, request, flash, current_app
from sqlalchemy import text
from app.forms import *
from app.models import WorkoutPlan, Workout, Usernames, Friendship,FriendRequest
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import json
from pathlib import Path


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
                return render_template('signuphtml', form=form, error=error)
            else:
                hashed = generate_password_hash(password, method='pbkdf2:sha256')
                new_user = Usernames(username=username, password=hashed, height=height, weight=weight, dob=dob)
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('routes.login'))
    return render_template('signup.html', form=form, error=error)   

def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        temp_username = form.username.data.strip()
        if not temp_username:
            error = 'Please enter a username.'
            flash(error, 'error')
        else:
            user = Usernames.query.filter_by(username=temp_username).first()
            if user is None:
                error = 'Username not found.'
                flash(error, 'error')
            elif not check_password_hash(user.password, form.password.data):
                error = 'Incorrect password.'
                flash(error, 'error')
            else:
                session['logged_in'] = True
                session['username'] = temp_username
                session['user_id']  = user.id
                return redirect(url_for('routes.index'))

    elif request.method == 'POST':
        error = 'Form validation failed.'
        flash(error, 'error')
    return render_template('login.html', form=form, error=error)

## logout page
def logout():
    session.clear()
    return redirect(url_for('routes.login'))

## index/dashboard page
def index():
    if not session.get('logged_in') or not Usernames.query.filter_by(username=session['username']).first():
        return redirect(url_for('routes.login'))
    plans = [ ####TODO: REMOVE THIS HARDCODED PART
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
    return render_template('profile.html', user=user, username=session['username'], workout_history=workout_history, 
                           height=user.height, dob=user.dob, friends_count=len(user.friendships), profile_pic=user.profile_pic)

def start_exercise():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))

    form = MuscleForm()
    json_path = Path(__file__).resolve().parent.parent / 'static' / 'data' / 'exercises.json'

    if json_path.exists():
        with open(json_path) as f:
            all_data = json.load(f)
        form.muscle.choices = [(key, key.capitalize()) for key in all_data.keys()]
    else:
        all_data = {}
        form.muscle.choices = []

    exercises = []

    if request.is_json:
        muscle = request.json.get("muscle_id")
        exercises = all_data.get(muscle, [])
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
    user_id = session.get('user_id')
    print("SESSION user_id:", user_id)  # 🔍

    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    query = text("""
        SELECT date, SUM(calories_burned) AS calories
        FROM workout_history
        WHERE user_id = :user_id
        GROUP BY date
        ORDER BY date ASC
    """)
    result = db.session.execute(query, {"user_id": user_id}).fetchall()
    print("QUERY RESULT:", result)  # 🔍

    data = [{"date": str(row.date), "calories": row.calories} for row in result]
    return jsonify(data)


def view_friends():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('routes.login'))

    # 已接受的好友
    friendships = Friendship.query.filter_by(user_id=user_id).all()
    friends     = [fs.friend for fs in friendships]

    # 收到的好友请求
    requests    = FriendRequest.query.filter_by(to_user_id=user_id).all()

    form = AddFriendForm()
    if form.validate_on_submit():
        uname = form.friend_username.data.strip()
        target = Usernames.query.filter_by(username=uname).first()
        if not target:
            flash(f'user "{uname}" not found', 'error')
        elif target.id == user_id:
            flash('you can\'t add youeself', 'error')
        else:
            already_frd = Friendship.query.filter_by(user_id=user_id, friend_id=target.id).first()
            already_req = FriendRequest.query.filter_by(from_user_id=user_id, to_user_id=target.id).first()
            if already_frd:
                flash(f'"{uname}" is already your friend', 'info')
            elif already_req:
                flash(f'already send request to  "{uname}",please wait', 'info')
            else:
                fr = FriendRequest(from_user_id=user_id, to_user_id=target.id)
                db.session.add(fr)
                db.session.commit()
                flash(f'already send friend request to  "{uname}"!', 'success')
        return redirect(url_for('routes.view_friends'))

    return render_template('friends.html',
                           friends=friends,
                           requests=requests,
                           form=form)

def accept_friend(req_id):
    user_id = session.get('user_id')
    fr = FriendRequest.query.get(req_id)
    if fr and fr.to_user_id == user_id:
        # 建立双向好友关系
        db.session.add(Friendship(user_id=user_id,      friend_id=fr.from_user_id))
        db.session.add(Friendship(user_id=fr.from_user_id, friend_id=user_id))
        db.session.delete(fr)
        db.session.commit()
        flash('Request Accept', 'success')
    else:
        flash('error', 'error')
    return redirect(url_for('routes.view_friends'))


def decline_friend(req_id):
    user_id = session.get('user_id')
    fr = FriendRequest.query.get(req_id)
    if fr and fr.to_user_id == user_id:
        db.session.delete(fr)
        db.session.commit()
        flash('Request refused', 'info')
    else:
        flash('error', 'error')
    return redirect(url_for('routes.view_friends'))

UPLOAD_FOLDER = 'static/profile_pics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def edit_profile():
    user = Usernames.query.filter_by(username=session.get('username')).first()
    if not user:
        return redirect(url_for('routes.login'))

    form = EditProfileForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        if form.password.data:
            user.password = generate_password_hash(form.password.data)
        user.height = form.height.data
        user.dob = request.form['dob']  

        file = request.files.get('profile_pic')
        if file and file.filename:
            upload_folder = os.path.join(current_app.root_path, 'static', 'profile_pics')
            os.makedirs(upload_folder, exist_ok=True)

            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            user.profile_pic = filename 

        db.session.commit()
        session['username'] = user.username
        return redirect(url_for('routes.profile'))

    return render_template('edit_profile.html', form=form, user=user)
