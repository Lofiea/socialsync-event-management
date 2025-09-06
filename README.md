# Overview
SocialSync is a full-stack event management web app designed to help users discover, create, and manage local events in one place. It lets people browse upcoming events, search by keywords or tags, and sort by date, popularity, or relevance. Users can create their own events, add details like descriptions, dates, locations, capacity, and images, and manage everything through a personal dashboard.

# Getting Started
Getting Started
1) Prereqs
```
Python 3.11+

pip (or uv / pipx), git
```

2) Clone & install
```
git clone https://github.com/<you>/socialsync-event-management.git
cd socialsync-event-management
python -m venv .venv && source .venv/bin/activate   # (Windows) .venv\Scripts\activate
pip install -r requirements.txt
```
4) Environment variables

Create a .env (or copy .env.example):
```
FLASK_ENV=development
SECRET_KEY=dev-change-me
DATABASE_URL=sqlite:///socialsync.db
UPLOAD_FOLDER=./static/uploads
MAX_CONTENT_LENGTH=5_000_000   # 5 MB
JWT_SECRET_KEY=dev-jwt-change-me
```

4) Initialize database & seed
```
python scripts/create_db.py
python scripts/seed.py   # optional demo data
```
6) Run the app
   
# Project Structure
``` 
event-app/
├─ app.py # Main Flask app
├─ database.db # SQLite database
├─ schema.sql # SQL schema for creating tables
├─ templates/ # HTML templates
│ ├─ index.html # Homepage
│ ├─ events.html # Event listings
│ ├─ createevent.html# Create event form
│ ├─ favorite.html # Saved events
│ ├─ profile.html # User profile
│ ├─ login.html # User login
│ ├─ signup.html # User registration
│ ├─ verification.html # Email/code verification
│ ├─ aboutus.html # About page
│ └─ contact.html # Contact page
├─ static/ # CSS, JS, and uploaded images
├─ flask_helpers/ # Helper functions for queries, auth, etc.
├─ instance/ # Configs or local database instance
└─ myproject/ # (Optional / legacy folder)
```
# Tech Stack

Backend: Python 3.11+, Flask 3.x, Werkzeug

Database: SQLite 3 

Auth: Session cookies (Flask-Login); optional JWT (Flask-JWT-Extended)

Validation/Forms: WTForms or Flask-WTF (CSRF)

Testing: pytest, pytest-flask, coverage

CI/CD: GitHub Actions

# Contribution

Jenny Nguyen    ttn323@drexel.edu <br>
Dishita Singh   ds3864@drexel.edu <br>
Ansh Lad        al3788@drexel.edu <br>
Misha Busko     mb4558@drexel.edu (previous project owner) <br>
Gabe Duran      gd537@drexel.edu (previous developer)








