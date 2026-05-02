"""Flask entry point for Offline Rural Health Management System."""

from flask import Flask

from models import db
from routes import main


def create_app():
    """App factory for local/offline usage."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "offline-rural-health-secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///health.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
