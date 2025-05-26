from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3 
import re #regex pattern matching 

app = Flask(__name__)

# Database connection function 
app.secret_key = 'supersecretkey'
def get_db_connection(): 
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection 

# Home page 
@app.route('/')
def index():
    return render_template('index.html')


#route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        user = connection.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        connection.close()

        if user and user['password'] == password: 
            session['logged_in'] = True
            session['username'] = user['username']
            flash('You have successfully logged in!')
            return redirect(url_for('index'))
        
        error = "Invalid email or password."
        return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
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
       
        if len(password) < 8: 
            error = "Password must be at least 8 characters long." 
            return render_template('signup.html', error=error)
        
        elif not re.research(r"[A-Z]", password): 
            error = "Password must contain at least one uppercase letter."
            return render_template('signup.html', error=error)
        
        elif not re.search(r"[a-z]", password):
            error = "Password must contain at least one lowercase letter."
            return render_template('signup.html', error=error)
        
        elif not re.search(r'[0-9]', password):
            error = "Password must contain at least one number."
            return render_template('signup.html', error=error)
        
        elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            error = "Password must contain at least one special character."
            return render_template('signup.html', error=error)
        else: 
            error = None 

        if error: 
            return render_template('signup.html', error=error)
        
        #check if username or email already exists
        connection = get_db_connection()
        existing_user = connection.execute('SELECT * FROM users WHERE username = ? OR email = ?',
                                            (username, email)).fetchone()
        if existing_user: 
            error = "An account with this username or email already exists."
            connection.close()
            return render_template('signup.html', error=error)
        #insert user into database
        connection = get_db_connection()
        connection.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                           (username, email, password))
        connection.commit()
        print("New user created:", username, email)
        connection.close()

        session['logged_in'] = True
        session['username'] = username
        flash('You have successfully signed up!')

        #redirect to login after successful sign-up
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/events')
def events():
    connection = get_db_connection()
    events = connection.execute('SELECT * FROM events').fetchall()
    connection.close()
    return render_template('events.html', events=events)

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

# creating events
@app.route('/create-event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        data = request.form
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO events (
                name, description, start_date, start_time, end_date, end_time,
                location, is_offline, capacity, visibility, host,
                age_tag, event_type, budget, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('name'),
            data.get('notes'),
            data.get('startDate'),
            data.get('startTime'),
            data.get('endDate'),
            data.get('endTime'),
            data.get('location'),
            1 if data.get('isOffline') == 'on' else 0,
            data.get('capacity'),
            data.get('visibility', 'Public'),
            data.get('host', 'Anonymous'),
            data.get('age_tag', 'All Ages'),
            data.get('event_type'),
            data.get('budget'),
            data.get('notes')
        ))
        conn.commit()
        conn.close()
        return redirect(url_for('events'))
    return render_template('createevent.html')

if __name__ == '__main__':
    app.run(debug=True)