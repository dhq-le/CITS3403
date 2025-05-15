import os
from flask import jsonify, render_template, session, redirect, url_for, request, flash, current_app
from sqlalchemy import text
from app.forms import *
from app.models import WorkoutPlan, Workout, Usernames, Friendship,FriendRequest
from app import db
from werkzeug.utils import secure_filename
import json
from pathlib import Path
from datetime import date

from flask_login import login_user, logout_user, login_required, current_user

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
                new_user = Usernames(username=username, height=height, weight=weight, dob=dob)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                db.session.flush()
                flash('Account created successfully', 'success')
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
            elif not user.check_password(form.password.data):
                error = 'Incorrect password.'
                flash(error, 'error')
            else:
                login_user(user)
                flash('Login successful.', 'success')
                return redirect(url_for('routes.index'))

    elif request.method == 'POST':
        error = 'Form validation failed.'
        flash(error, 'error')
    return render_template('login.html', form=form, error=error)

## logout page
def logout():
    logout_user()
    return redirect(url_for('routes.login'))

## index/dashboard page
@login_required
def index():
    user = current_user
    plans = []
    workout_plans = Workout.query.filter(
        Workout.user_id == user.id,
        Workout.completion == False,
        Workout.date == date.today()
    ).all()

    for plan in workout_plans:
        plans.append(WorkoutPlan(exercise=plan.exercise, sets=plan.sets, reps=plan.reps, weights=plan.weights))
    return render_template('home.html', plans=plans, username=user.username)

## profile page
@login_required
def profile():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))
    user = current_user
    workout_history = Workout.query.filter(
        Workout.user_id == user.id,
        Workout.completion == True
    ).all()
    return render_template('profile.html', user=user, username=session['username'], workout_history=workout_history, 
                           height=user.height, dob=user.dob, friends_count=len(user.friendships), profile_pic=user.profile_pic)
## workout plans page
def workout_plans():
    if not session.get('logged_in'):
        return redirect(url_for('routes.login'))
    user = Usernames.query.filter_by(username=session['username']).first()
    workout_plans = Workout.query.filter(
        Workout.user_id == user.id,
        Workout.completion == False
    ).all()
    return render_template('workout_plans.html', user=user, username=session['username'], workout_plans=workout_plans)


@login_required
def start_exercise():
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


def calorie_calculator(form):
        exercise_param = form.exercise.data
        sets = form.sets.data or 0
        reps = form.reps.data or 0
        completion_status = form.completion_status.data or False

        calories_per_rep = 0
        json_path = Path(__file__).resolve().parent / 'static' / 'data' / 'exercises.json'
        if json_path.exists():
            with open(json_path) as f:
                all_data = json.load(f)
            for group in all_data.values():
                for ex in group:
                    if exercise_param.lower() in ex["name"].lower():
                        calories_per_rep = ex.get("calories_burned_per_rep", 0)
                        break
        total_calories = calories_per_rep * sets * reps
        return total_calories

@login_required
def log_workout():
    form = WorkoutForm()
    plan_id = request.args.get('plan_id')
    workout = None
    message = ""

    # Check if editing an existing plan
    if plan_id:
        workout = Workout.query.get(int(plan_id))
        if workout and workout.user_id == Usernames.query.filter_by(username=session['username']).first().id:
            # Pre-fill form with existing data
            form.exercise.data = workout.exercise
            form.sets.data = workout.sets
            form.reps.data = workout.reps
            form.weights.data = workout.weights
            form.date.data = workout.date
            form.completion_status.data = workout.completion

    # Autofill if coming from quick-log link
    query_param = request.args.get('exercise')
    if query_param and not plan_id:
        form.exercise.data = query_param

    # Check if the form has been submitted
    if form.validate_on_submit():
        # Calculate calories
        total_calories = calorie_calculator(form)

        if plan_id:  # Updating an existing workout
            if workout:
                workout.exercise = form.exercise.data
                workout.sets = form.sets.data or 0
                workout.reps = form.reps.data or 0
                workout.date = form.date.data
                workout.calories_burned = total_calories
                workout.weights = form.weights.data
                workout.completion = form.completion_status.data or False
                db.session.commit()
                message = f"Workout {'updated' if workout.completion else 'plan updated'}!"
            else:
                flash("Workout not found.")
                return redirect(url_for('routes.index'))

        else:  # Creating a new workout
            # Check if the workout is completed and not set for a future date
            if form.completion_status.data and form.date.data > date.today():
                flash("Can't upload a completed workout later than today! Either select a date before today, or make this a workout plan.")
            else:
                workout = Workout(
                    user_id=Usernames.query.filter_by(username=session['username']).first().id,
                    exercise=form.exercise.data,
                    date=form.date.data,
                    sets=form.sets.data or 0,
                    reps=form.reps.data or 0,
                    calories_burned=total_calories,
                    weights=form.weights.data,
                    completion=form.completion_status.data or False
                )
                db.session.add(workout)
                db.session.commit()
                message = f"Workout logged! Calories burned: {total_calories}" if workout.completion else "Workout plan saved!"

        flash(message)
        return redirect(url_for('routes.index'))

    return render_template('log.html', form=form)


## calorie data chart
@login_required
def calories_data():

    user_id = current_user.id
    print("SESSION user_id:", user_id)

    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    # check if it's a friend comparison
    friend_username = request.args.get('friend')

    # if no friend param: just return your own data (for profile/home)
    if not friend_username:
        query = text("""
            SELECT date, SUM(calories_burned) AS calories
            FROM workout_history
            WHERE user_id = :user_id
            GROUP BY date
            ORDER BY date ASC
        """)
        result = db.session.execute(query, {"user_id": user_id}).fetchall()
        data = [{"date": str(row.date), "calories": row.calories} for row in result]
        return jsonify(data)

    # otherwise: comparison mode
    from app.models import Usernames  # adjust if needed based on where Usernames is defined
    friend = Usernames.query.filter_by(username=friend_username).first()
    if not friend:
        return jsonify({"error": "Friend not found"}), 404

    print(f"Comparing with friend: {friend.username} (ID: {friend.id})")

    user_query = text("""
        SELECT date, SUM(calories_burned) AS calories
        FROM workout_history
        WHERE user_id = :uid
        GROUP BY date
        ORDER BY date
    """)
    friend_query = text("""
        SELECT date, SUM(calories_burned) AS calories
        FROM workout_history
        WHERE user_id = :fid
        GROUP BY date
        ORDER BY date
    """)

    user_result = db.session.execute(user_query, {"uid": user_id}).fetchall()
    friend_result = db.session.execute(friend_query, {"fid": friend.id}).fetchall()

    return jsonify({
        "user": [{"date": str(row.date), "calories": row.calories} for row in user_result],
        "friend": [{"date": str(row.date), "calories": row.calories} for row in friend_result]
    })


@login_required
def view_friends():
    user_id = current_user.id

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

@login_required
def accept_friend(req_id):
    user_id = current_user.id
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


@login_required
def decline_friend(req_id):
    user_id = current_user.id
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

@login_required
def edit_profile():
    user = Usernames.query.filter_by(username=current_user.username).first()
    if not user:
        return redirect(url_for('routes.login'))

    form = EditProfileForm(obj=user)

    if form.validate_on_submit():
        user.username = form.username.data
        if form.password.data:
            user.password = user.set_password(form.password.data)
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
