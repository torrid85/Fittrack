"""Database models for the Offline Rural Health Management System."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Shared SQLAlchemy object
# It is initialized inside create_app() in app.py

db = SQLAlchemy()


class Patient(db.Model):
    """Stores basic patient registration details."""

    id = db.Column(db.Integer, primary_key=True)
    patient_code = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    village = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # A patient can have many visit records
    visits = db.relationship("Visit", backref="patient", lazy=True, cascade="all, delete-orphan")
    emergency_requests = db.relationship(
        "EmergencyRequest", backref="patient", lazy=True, cascade="all, delete-orphan"
    )


class Visit(db.Model):
    """Stores each patient visit with diagnosis information."""

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    visit_date = db.Column(db.String(20), nullable=False)
    symptoms = db.Column(db.Text, nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    medicines = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EmergencyRequest(db.Model):
    """Stores one emergency ambulance request event."""

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey("patient.id"), nullable=False)
    request_time = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(40), default="Sent Successfully")
    message = db.Column(db.Text, nullable=False)
