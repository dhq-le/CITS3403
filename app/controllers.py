import os
from flask import jsonify, render_template, session, redirect, url_for, request, flash, current_app
from sqlalchemy import text
from app.forms import *
from app.models import WorkoutPlan, Workout, Usernames, Friendship,FriendRequest
from app import db
from werkzeug.utils import secure_filename
import json
from pathlib import Path
from datetime import date, datetime
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse, urljoin


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


def calculate_age(dob_date: date) -> int:
    today = date.today()
    age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    return age


## index/dashboard page
@login_required
def index():

    user = current_user
    plans = []
    if user.dob:
        age = calculate_age(user.dob)
    else:
        age = "No age provided."
    workout_plans = Workout.query.filter(
        Workout.user_id == user.id,
        Workout.completion == False,
        Workout.date == date.today()
    ).all()

    for plan in workout_plans:
        plans.append(WorkoutPlan(exercise=plan.exercise, sets=plan.sets, reps=plan.reps, weights=plan.weights))
    return render_template('home.html', plans=plans, username=user.username, user=user, age=age)

## profile page
@login_required
def profile():
    user = current_user
    workout_history = Workout.query.filter(
	    Workout.user_id == user.id,
	    Workout.completion == True
    ).all()
    return render_template('profile.html', user=user, username=current_user.username, workout_history=workout_history,
                           height=user.height, dob=user.dob, friends_count=len(user.friendships), profile_pic=user.profile_pic)


## workout plans page
@login_required
def workout_plans():
    user = current_user
    workout_plans = Workout.query.filter(
        Workout.user_id == user.id,
        Workout.completion == False
    ).all()
    return render_template('workout_plans.html', user=user, username=session['username'], workout_plans=workout_plans)


@login_required
def delete_workout(workout_id):
    workout = Workout.query.filter_by(workout_id=workout_id, user_id=current_user.id).first()
    if workout:
        db.session.delete(workout)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Workout not found'}), 404

@login_required
def complete_workout(workout_id):
    workout = Workout.query.filter_by(workout_id=workout_id, user_id=current_user.id).first()
    if workout:
        workout.completion = True
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False, 'error': 'Workout not found'}), 404


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


def is_safe_url(target):
    # Prevent open redirect vulnerabilities
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@login_required
def log_workout():
    form = WorkoutForm()

    plan_id = request.values.get('plan_id')  # plan_id to identify updates
    next_url = request.args.get('next') or url_for('routes.index')

    if not is_safe_url(next_url):
        next_url = url_for('routes.index')

    # If updating, fetch the existing workout
    if plan_id:
        workout = Workout.query.filter_by(workout_id=plan_id, user_id=current_user.id).first()
        if workout:
            if request.method == 'GET':
                # Pre-fill form fields with existing workout data
                form.next.data = next_url  # Preserved into form
                form.exercise.data = workout.exercise
                form.date.data = workout.date
                form.sets.data = workout.sets
                form.reps.data = workout.reps
                form.weights.data = workout.weights
                form.completion_status.data = workout.completion

    # Handle pre-filling via ?exercise= query
    else:
        query_param = request.args.get('exercise')
        if query_param and not plan_id:
            form.exercise.data = query_param

    if form.validate_on_submit():
        if form.completion_status.data is True:
            if form.date.data > date.today():
                flash('Can\'t select a date in the future for a workout you\'ve completed!', 'error')
                return render_template('log.html', form=form)
        exercise_param = form.exercise.data
        sets = form.sets.data or 0
        reps = form.reps.data or 0
        calories_per_rep = 0

        # Load calories per rep from JSON
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

        if workout:
            # Update existing workout
            workout.exercise = exercise_param
            workout.date = form.date.data
            workout.sets = sets
            workout.reps = reps
            workout.weights = form.weights.data
            workout.calories_burned = total_calories
            workout.completion = form.completion_status.data
            flash(f'Workout updated!')
        else:
            # Create new workout
            workout = Workout(
                user_id=current_user.id,
                exercise=exercise_param,
                date=form.date.data,
                sets=sets,
                reps=reps,
                calories_burned=total_calories,
                weights=form.weights.data,
                completion=form.completion_status.data
            )
            db.session.add(workout)
            flash('Workout logged!')

        db.session.commit()
        next_url = form.next.data or url_for('routes.index')
        return redirect(next_url)

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
            AND completion = True
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
        AND completion = True
        GROUP BY date
        ORDER BY date
    """)
    friend_query = text("""
        SELECT date, SUM(calories_burned) AS calories
        FROM workout_history
        WHERE user_id = :fid
        AND completion = True
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

    # Accepted friends
    friendships = Friendship.query.filter_by(user_id=user_id).all()
    friends     = [fs.friend for fs in friendships]

    # Received friend requests
    requests    = FriendRequest.query.filter_by(to_user_id=user_id).all()

    form = AddFriendForm()
    if form.validate_on_submit():
        uname = form.friend_username.data.strip()
        target = Usernames.query.filter_by(username=uname).first()
        if not target:
            flash(f'Couldn\'t find a user by the name of {uname}!', 'error')
        elif target.id == user_id:
            flash('You can\'t add yourself!', 'error')
        else:
            already_frd = Friendship.query.filter_by(user_id=user_id, friend_id=target.id).first()
            already_req = FriendRequest.query.filter_by(from_user_id=user_id, to_user_id=target.id).first()
            if already_frd:
                flash(f'{uname} is already your friend.', 'error')
            elif already_req:
                flash(f'Already sent a request to {uname}.', 'error')
            else:
                fr = FriendRequest(from_user_id=user_id, to_user_id=target.id)
                db.session.add(fr)
                db.session.commit()
                flash(f'Successfully sent a friend request to {uname}!', 'success')
        return redirect(url_for('routes.view_friends'))

    return render_template('friends.html',
                           friends=friends,
                           requests=requests,
                           form=form
                           )

@login_required
def accept_friend(req_id):
    user_id = current_user.id
    fr = FriendRequest.query.get(req_id)
    if fr and fr.to_user_id == user_id:
        # Establish a bidirectional friendship
        db.session.add(Friendship(user_id=user_id, friend_id=fr.from_user_id))
        db.session.add(Friendship(user_id=fr.from_user_id, friend_id=user_id))
        db.session.delete(fr)
        db.session.commit()
        flash('Request accepted!', 'info')
    else:
        flash('You\'ve run into an error! Please try again later.', 'error')
    return redirect(url_for('routes.view_friends'))


@login_required
def decline_friend(req_id):
    user_id = current_user.id
    fr = FriendRequest.query.get(req_id)
    if fr and fr.to_user_id == user_id:
        db.session.delete(fr)
        db.session.commit()
        flash('Request declined.', 'info')
    else:
        flash('You\'ve run into an error! Please try again later.', 'error')
    return redirect(url_for('routes.view_friends'))


UPLOAD_FOLDER = 'static/profile_pics'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_required
def edit_profile():
    user = current_user

    form = EditProfileForm(obj=user)

    if form.validate_on_submit():
        if Usernames.query.filter_by(username=form.username.data).first():
            if form.username.data != user.username:
                flash('That username is already taken.', 'error')
                return render_template('edit_profile.html', form=form, user=user)
        user.username = form.username.data
        if form.password.data is not None:
            print(form.password.data)
            user.set_password(form.password.data)
            print(user.password)
        user.height = form.height.data
        user.dob = form.dob.data

        file = request.files.get('profile_pic')
        if file and file.filename:
            if allowed_file(file.filename):
                upload_folder = os.path.join(current_app.root_path, 'static', 'profile_pics')
                os.makedirs(upload_folder, exist_ok=True)

                filename = secure_filename(file.filename)
                file_path = os.path.join(upload_folder, filename)
                file.save(file_path)

                user.profile_pic = filename
            else:
                flash('File not allowed. Please upload a valid image file (png, jpg, jpeg).', 'error')
                return render_template('edit_profile.html', form=form, user=user)

        db.session.commit()
        session['username'] = user.username
        flash('Successfully updated your information!', 'success')
        return redirect(url_for('routes.profile'))

    return render_template('edit_profile.html', form=form, user=user)
