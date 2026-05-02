# routes.py - All URL routes and logic for the Fitness Tracker

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Workout

# Blueprint groups all routes together; registered in app.py
main = Blueprint('main', __name__)


# ─── Helper ────────────────────────────────────────────────────────────────────

def get_current_user():
    """Return the logged-in User object, or None if not logged in."""
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None


# ─── Auth Routes ───────────────────────────────────────────────────────────────

@main.route('/')
def index():
    """Home page — redirect to dashboard if logged in, else to login."""
    if get_current_user():
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('main.login'))


@main.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user account."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        # Check if username already taken
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Try another.', 'error')
            return redirect(url_for('main.register'))

        # Hash the password before storing (never store plain text!)
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created! Please log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    """Log in an existing user."""
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        # Verify user exists and password matches
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id   # save user in session
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


@main.route('/logout')
def logout():
    """Log out the current user by clearing the session."""
    session.clear()
    return redirect(url_for('main.login'))


# ─── Dashboard ─────────────────────────────────────────────────────────────────

@main.route('/dashboard')
def dashboard():
    """Main dashboard: shows summary stats for the logged-in user."""
    user = get_current_user()
    if not user:
        return redirect(url_for('main.login'))

    workouts = Workout.query.filter_by(user_id=user.id).order_by(Workout.date_logged.desc()).all()

    # Calculate summary stats
    total_calories = sum(w.calories for w in workouts)
    total_workouts = len(workouts)
    total_minutes  = sum(w.duration for w in workouts)

    return render_template(
        'dashboard.html',
        user=user,
        workouts=workouts,
        total_calories=total_calories,
        total_workouts=total_workouts,
        total_minutes=total_minutes
    )


# ─── Workout Routes ────────────────────────────────────────────────────────────

@main.route('/add_workout', methods=['GET', 'POST'])
def add_workout():
    """Add a new workout entry."""
    user = get_current_user()
    if not user:
        return redirect(url_for('main.login'))

    if request.method == 'POST':
        workout_type = request.form['workout_type'].strip()
        duration     = int(request.form['duration'])
        calories     = int(request.form['calories'])

        new_workout = Workout(
            workout_type=workout_type,
            duration=duration,
            calories=calories,
            user_id=user.id
        )
        db.session.add(new_workout)
        db.session.commit()

        flash('Workout logged successfully!', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('add_workout.html', user=user)


@main.route('/workouts')
def workouts():
    """View all workouts for the logged-in user."""
    user = get_current_user()
    if not user:
        return redirect(url_for('main.login'))

    all_workouts = Workout.query.filter_by(user_id=user.id)\
                                .order_by(Workout.date_logged.desc()).all()
    return render_template('workouts.html', user=user, workouts=all_workouts)


@main.route('/delete_workout/<int:workout_id>')
def delete_workout(workout_id):
    """Delete a specific workout by ID (only if it belongs to the user)."""
    user = get_current_user()
    if not user:
        return redirect(url_for('main.login'))

    workout = Workout.query.get_or_404(workout_id)

    # Security check: make sure the workout belongs to this user
    if workout.user_id != user.id:
        flash('You cannot delete someone else\'s workout.', 'error')
        return redirect(url_for('main.dashboard'))

    db.session.delete(workout)
    db.session.commit()
    flash('Workout deleted.', 'success')
    return redirect(url_for('main.workouts'))
