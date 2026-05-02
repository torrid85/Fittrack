# Offline Rural Health Management System (Flask + SQLite)

A simple, fully offline MVP for rural clinic management.

## Features

1. Patient Registration (auto-generated Patient ID)
2. Patient Dashboard with search (name/village)
3. Add Visit Record linked to patient
4. Patient History page with all visits
5. Emergency Ambulance Request:
   - One-click red button
   - Confirmation popup
   - Status update: `Sending...` -> `Sent Successfully`
   - Simulated SMS in server console log
   - Emergency request saved in database

## Tech Stack

- Backend: Flask (Python)
- Database: SQLite (`health.db`)
- Frontend: HTML/CSS/JavaScript
- No internet APIs, no cloud dependency

## Project Structure

- `app.py` - Flask app entry point
- `models.py` - Database models
- `routes.py` - Routes and business logic
- `create_db.py` - Database creation script
- `templates/` - HTML templates
- `static/css/style.css` - Styling
- `static/js/main.js` - Frontend JS behavior
- `health.db` - Auto-created SQLite database file

## Setup and Run

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python create_db.py
python app.py
```

Open in browser:

`http://127.0.0.1:5000`

## Notes

- Works fully on localhost and offline.
- Database file is local SQLite.
- Code is intentionally beginner-friendly with comments.
