# app.py - Main entry point for the Fitness Tracker Flask application

from flask import Flask
from models import db
from routes import main

# ─── App Setup ────────────────────────────────────────────────────────────────

def create_app():
    app = Flask(__name__)

    # Secret key for session management (change this to something random in production)
    app.config['SECRET_KEY'] = 'fitness_secret_key_2024'

    # SQLite database stored locally in the project folder
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database with the app
    db.init_app(app)

    # Register all routes from routes.py
    app.register_blueprint(main)

    # Create all database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    # debug=True means the server restarts automatically on code changes
    app.run(debug=True)
