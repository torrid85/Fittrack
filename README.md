# ⚡ FitTrack — Fitness Tracker Web App

A simple, beginner-friendly fitness tracker built with **Flask + SQLite**.  
Track your workouts, view a dashboard, and manage your fitness history.

---

## 📁 Folder Structure

```
fitness_tracker/
├── app.py               ← Entry point; creates Flask app
├── models.py            ← Database models (User, Workout)
├── routes.py            ← All URL routes and logic
├── requirements.txt     ← Python dependencies
├── static/
│   ├── css/
│   │   └── style.css    ← Styling
│   └── js/
│       └── main.js      ← Small JS enhancements
└── templates/
    ├── base.html        ← Shared layout (navbar, flash messages)
    ├── login.html       ← Login page
    ├── register.html    ← Register page
    ├── dashboard.html   ← Dashboard with stats
    ├── add_workout.html ← Add workout form
    └── workouts.html    ← Full workout history
```

> **Note:** `fitness.db` (the SQLite database) is created automatically when you first run the app. You don't need to create it manually.

---

## 🚀 How to Run (Step-by-Step)

### Step 1 — Make sure Python is installed
```bash
python --version   # should be 3.8 or higher
```

### Step 2 — Navigate to the project folder
```bash
cd fitness_tracker
```

### Step 3 — Create a virtual environment (recommended)
```bash
python -m venv venv
```

Activate it:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### Step 4 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 5 — Run the app
```bash
python app.py
```

### Step 6 — Open in browser
Visit: **http://127.0.0.1:5000**

---

## ✅ Features

| Feature              | Status |
|----------------------|--------|
| User Registration    | ✅     |
| User Login/Logout    | ✅     |
| Add Workout          | ✅     |
| View All Workouts    | ✅     |
| Delete Workout       | ✅     |
| Dashboard Stats      | ✅     |
| Password Hashing     | ✅     |
| Session Management   | ✅     |

---

## 🛠️ Tech Stack

- **Backend:** Python 3, Flask
- **Database:** SQLite (via Flask-SQLAlchemy)
- **Frontend:** HTML5, CSS3, Vanilla JS
- **Security:** Werkzeug password hashing

---

## 💡 Notes for Beginners

- The database (`fitness.db`) is created automatically — no setup needed.
- Passwords are **hashed** using Werkzeug; they are never stored as plain text.
- Sessions are used to keep users logged in between page visits.
- `debug=True` in `app.py` means the server auto-restarts on code changes. Turn it off in production.
