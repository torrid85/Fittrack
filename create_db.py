"""Creates all SQLite tables for the health management system."""

from app import create_app
from models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database created successfully: health.db")
