# models.py - Database models (tables) for the app

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# db is the SQLAlchemy instance shared across the app
db = SQLAlchemy()


# ─── User Table ───────────────────────────────────────────────────────────────

class User(db.Model):
    """Stores registered users."""
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # stored as a hash

    # One user can have many workouts
    workouts = db.relationship('Workout', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'


# ─── Workout Table ─────────────────────────────────────────────────────────────

class Workout(db.Model):
    """Stores individual workout entries."""
    id             = db.Column(db.Integer, primary_key=True)
    workout_type   = db.Column(db.String(100), nullable=False)   # e.g. "Running"
    duration       = db.Column(db.Integer, nullable=False)        # in minutes
    calories       = db.Column(db.Integer, nullable=False)        # calories burned
    date_logged    = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign key linking this workout to a user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Workout {self.workout_type} - {self.calories} cal>'
