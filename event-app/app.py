from flask import Flask, make_response, render_template, request, redirect, url_for, session, flash
from datetime import datetime, date
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
JWTManager, create_access_token, jwt_required, get_jwt_identity,
set_access_cookies, unset_jwt_cookies
)
import os
import sqlite3 
import re

#Jenny's code 
app = Flask(__name__)
app.secret_key = 'supersecretkey' #Secret key for session management

app.config['JWT_SECRET_KEY'] = 'change-this-in-production'
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False # True if served over HTTPS
app.config['JWT_COOKIE_SAMESITE'] = 'Lax'
app.config['JWT_COOKIE_CSRF_PROTECT'] = False # enable True and add CSRF header in prod
jwt = JWTManager(app)

UPLOAD_FOLDER = 'static/uploads' # Folder to store uploaded images
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER # Ensure the upload folder exists

@app.template_filter('datetimeformat')
def datetimeformat(value):
    try: 
        return datetime.strptime(value, '%Y-%m-%d').strftime('%m/%d/%Y')
    except: 
        return value
    
#Database connection function 
DB_PATH = 'database.db' # Path to the SQLite database file
def get_db_connection(): 
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection 

# Initialize tables + indexes if missing
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    start_date TEXT,
    start_time TEXT,
    end_date TEXT,
    end_time TEXT,
    location TEXT,
    attendees INTEGER DEFAULT 0,
    image TEXT,
    budget REAL,
    rating REAL
);

CREATE INDEX IF NOT EXISTS idx_events_title ON events(title);
CREATE INDEX IF NOT EXISTS idx_events_start ON events(start_date, start_time);
"""

def init_db():
    """Initialize database schema + indexes if missing."""
    con = get_db_connection()
    con.executescript(SCHEMA_SQL)
    con.commit()
    con.close()

init_db() 

# Home page 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST']) #shows the login page when visited (GET) and handles login form data when submitted (POST)
def login():
    if request.method == 'POST': 
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        user = connection.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone() # Fetch user by email
        connection.close()

        if user and check_password_hash(user['password'], password):
            session.permanent = True  # Make the session permanent
            session['logged_in'] = True
            session['username'] = user['username']
            access_token = create_access_token(identity=user['username'])
            resp = make_response(redirect(url_for('index')))
            set_access_cookies(resp, access_token)
            
            flash('You have successfully logged in!')
            return resp
        
        error = "Invalid email or password."
        return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You've been logged out.")
    resp = make_response(redirect(url_for('index')))
    unset_jwt_cookies(resp)
    return resp

#route for the signup page
@app.route('/signup', methods=['GET', 'POST']) #handle both viewing the page (GET) and submitting form data (POST)
def signup():
    if request.method == 'POST': 
        username = request.form['name'] 
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm-password']

        #Validate the input, check password strength and match
        if password != confirm: 
            error = "Passwords don't match."
            return render_template('signup.html', error=error)
        # Check password strength
        if len(password) < 8: 
            error = "Password must be at least 8 characters long." 
            return render_template('signup.html', error=error)
        # Check for at least one uppercase letter
        elif not re.search(r"[A-Z]", password): 
            error = "Password must contain at least one uppercase letter."
            return render_template('signup.html', error=error)
        # Check for at least one lowercase letter
        elif not re.search(r"[a-z]", password):
            error = "Password must contain at least one lowercase letter."
            return render_template('signup.html', error=error)
        # Check for at least one number and one special character
        elif not re.search(r'[0-9]', password):
            error = "Password must contain at least one number."
            return render_template('signup.html', error=error)
        # Check for at least one special character
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            error = "Password must contain at least one special character."
            return render_template('signup.html', error=error)
        
        # Check if username or email already exists
        connection = get_db_connection()
        existing_user = connection.execute('SELECT * FROM users WHERE username = ? OR email = ?',
                                            (username, email)).fetchone()
        if existing_user: 
            error = "An account with this username or email already exists."
            connection.close()
            return render_template('signup.html', error=error)
        
        hashed_password = generate_password_hash(password)  
        connection.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                           (username, email, password))
        
        connection.commit()
        connection.close()

        # Set session variables
        session['logged_in'] = True
        session['username'] = username
        access_token = create_access_token(identity=username)

        resp = make_response(redirect(url_for('login')))
        set_access_cookies(resp, access_token)

        flash('You have successfully signed up!')

        #redirect to login after successful sign-up
        return resp
    return render_template('signup.html')

#jenny's part
#route for the profile page
@app.route('/profile')
@jwt_required()
def profile():
    username = get_jwt_identity() or session.get('username')
    if not username:
        flash('You need to log in first.')
        return redirect(url_for('login'))
    return render_template('profile.html', username=username)

#jenny's part
#route for the event page
@app.route('/events')
def events():
    # Get the sort parameter from the request, default to 'recommended'
    sort_by = request.args.get('sort', 'recommended') 
    page = max(int(request.args.get('page', 1) or 1), 1)
    per_page = 10
    offset = (page - 1) * per_page

    query = 'SELECT * FROM events'
    if sort_by == 'date':
        query += ' ORDER BY start_date ASC, start_time ASC'
    elif sort_by == 'price':
        query += ' ORDER BY budget ASC'  
    elif sort_by == 'rating':
        query += ' ORDER BY rating DESC'  
    elif sort_by == 'alphabetical':
        query += ' ORDER BY title COLLATE NOCASE ASC' 
    elif sort_by == 'id': 
        query += ' ORDER BY id ASC'
    else: 
        query += ' ORDER BY start_date ASC, start_time ASC, id ASC'


    connection = get_db_connection()
    total = connection.execute('SELECT COUNT(*) FROM events').fetchone()[0]
    events = connection.execute(f"{query} LIMIT ? OFFSET ?", (per_page, offset)).fetchall()
    connection.close()

    total_pages = max((total + per_page - 1) // per_page, 1)

    return render_template('events.html', events=events, current_sort=sort_by, page=page, total_pages=total_pages, per_page=per_page)

@app.route('/host-events')
def host_events():
    return render_template('hostevents.html')

@app.route('/favorite')
def favorite():
    return render_template('favorite.html')

@app.route('/verification')
def verification():
    return render_template('verification.html')

@app.route('/about-us')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/terms-and-conditions')
def termsandconditions():
    return render_template('termsandconditions.html')

@app.route('/privacy-policy')
def privacypolicy():
    return render_template('privacypolicy.html')

@app.route('/faq')
def faq():
    return render_template('FAQ.html')

#jenny's code
#route to create an event - with POST handling 
@app.route('/create-event', methods=['GET', 'POST'])
@jwt_required()
def create_event():
    # Check if the user is logged in
    if request.method == 'POST':
        title       = request.form['title'] # Get the title from the form
        description = request.form['description'] # Get the description from the form
        startDate   = request.form['startDate']
        startTime   = request.form['startTime']
        endDate     = request.form['endDate']
        endTime     = request.form['endTime']
        location    = request.form['location']
        attendees = request.form.get('attendees', '0')
        budget = request.form.get('budget', 'Free') #default to 'Free' if not provided
        event_type = request.form['eventType']


        image_file = request.files['image'] # Get the uploaded image file
        # Check if the image file is provided and save it
        if image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename)) # Save the file to the upload folder
        else:
            image_filename = None # No image provided
        conn = get_db_connection()
        #insrt the event data into the database
        conn.execute( 
            'INSERT INTO events (title, description, start_date, start_time, end_date, end_time, location, attendees, image, budget, event_type) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (title, description, startDate, startTime, endDate, endTime, location, attendees, image_filename, budget, event_type)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('events'))

    return render_template('createevent.html')

#Dishita's code for deleting an event
@app.route('/delete-event/<int:event_id>', methods=['POST'])
@jwt_required()
def delete_event(event_id):
    con = get_db_connection()
    con.execute('DELETE FROM events WHERE id = ?', (event_id,))
    con.commit()
    con.close()
    flash("Event deleted.", "info")
    return redirect(url_for('events'))

if __name__ == '__main__':
    app.run(debug=True)
