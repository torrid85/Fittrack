"""All routes/views for the Offline Rural Health Management System."""

from datetime import datetime
from flask import Blueprint, jsonify, redirect, render_template, request, url_for, flash

from models import db, Patient, Visit, EmergencyRequest

main = Blueprint("main", __name__)


def generate_patient_id() -> str:
    """Generate patient ID like P0001, P0002..."""
    last_patient = Patient.query.order_by(Patient.id.desc()).first()
    next_number = 1 if not last_patient else last_patient.id + 1
    return f"P{next_number:04d}"


@main.route("/")
def dashboard():
    """Main dashboard with patient list and optional search."""
    search_text = request.args.get("search", "").strip()

    query = Patient.query
    if search_text:
        query = query.filter(
            db.or_(Patient.name.ilike(f"%{search_text}%"), Patient.village.ilike(f"%{search_text}%"))
        )

    patients = query.order_by(Patient.created_at.desc()).all()
    return render_template("dashboard.html", patients=patients, search_text=search_text)


@main.route("/add-patient", methods=["GET", "POST"])
def add_patient():
    """Register a new patient."""
    if request.method == "POST":
        new_patient = Patient(
            patient_code=generate_patient_id(),
            name=request.form["name"].strip(),
            age=int(request.form["age"]),
            gender=request.form["gender"],
            village=request.form["village"].strip(),
            phone_number=request.form["phone_number"].strip(),
        )

        db.session.add(new_patient)
        db.session.commit()

        flash(f"Patient added successfully. ID: {new_patient.patient_code}", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("add_patient.html")


@main.route("/patient/<int:patient_id>")
def patient_history(patient_id):
    """Show all visit records for one patient."""
    patient = Patient.query.get_or_404(patient_id)
    visits = Visit.query.filter_by(patient_id=patient.id).order_by(Visit.created_at.desc()).all()
    emergencies = (
        EmergencyRequest.query.filter_by(patient_id=patient.id)
        .order_by(EmergencyRequest.request_time.desc())
        .all()
    )
    return render_template("patient_history.html", patient=patient, visits=visits, emergencies=emergencies)


@main.route("/patient/<int:patient_id>/add-visit", methods=["GET", "POST"])
def add_visit(patient_id):
    """Add a new visit record for a patient."""
    patient = Patient.query.get_or_404(patient_id)

    if request.method == "POST":
        visit = Visit(
            patient_id=patient.id,
            visit_date=request.form["visit_date"],
            symptoms=request.form["symptoms"].strip(),
            diagnosis=request.form["diagnosis"].strip(),
            medicines=request.form["medicines"].strip(),
        )
        db.session.add(visit)
        db.session.commit()

        flash("Visit record added successfully.", "success")
        return redirect(url_for("main.patient_history", patient_id=patient.id))

    return render_template(
        "add_visit.html", patient=patient, today=datetime.utcnow().strftime("%Y-%m-%d")
    )


@main.route("/patient/<int:patient_id>/request-ambulance", methods=["POST"])
def request_ambulance(patient_id):
    """Emergency endpoint: simulate sending SMS and store request."""
    patient = Patient.query.get_or_404(patient_id)

    sms_message = (
        f"EMERGENCY ALERT: Ambulance requested for {patient.name} "
        f"({patient.patient_code}) from {patient.village}. Contact: {patient.phone_number}."
    )

    # Simulated SMS send (offline-safe): print to server console/log.
    print("[SIMULATED SMS]", sms_message)

    emergency = EmergencyRequest(patient_id=patient.id, message=sms_message, status="Sent Successfully")
    db.session.add(emergency)
    db.session.commit()

    return jsonify({"status": "Sent Successfully", "message": "Ambulance request recorded and SMS simulated."})
