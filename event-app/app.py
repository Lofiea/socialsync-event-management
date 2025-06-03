from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import sqlite3 
import re
from datetime import datetime, date  # added `date`

app = Flask(__name__)
app.secret_key = 'supersecretkey' #Secret key for session management

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.template_filter('datetimeformat')
def datetimeformat(value):
    try: 
        return datetime.strptime(value, '%Y-%m-%d').strftime('%m/%d/%Y')
    except: 
        return value
#Database connection function 
def get_db_connection(): 
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection 

# Home page 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST': 
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        user = connection.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        connection.close()

        if user and user['password'] == password: 
            session.permanent = True  # Make the session permanent
            session['logged_in'] = True
            session['username'] = user['username']
            flash('You have successfully logged in!')
            return redirect(url_for('index'))
        
        error = "Invalid email or password."
        return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You've been logged out.")
    return redirect(url_for('index'))

#route for the signup page
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
        elif not re.search(r"[A-Z]", password): 
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

        connection = get_db_connection()
        existing_user = connection.execute('SELECT * FROM users WHERE username = ? OR email = ?',
                                            (username, email)).fetchone()
        if existing_user: 
            error = "An account with this username or email already exists."
            connection.close()
            return render_template('signup.html', error=error)
        connection.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                           (username, email, password))
        connection.commit()
        connection.close()

        session['logged_in'] = True
        session['username'] = username
        flash('You have successfully signed up!')

        #redirect to login after successful sign-up
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/profile')
def profile():
    if not session.get('logged_in'):
        flash('You need to log in first.')
        return redirect(url_for('login'))
    return render_template('profile.html', username=session.get('username'))
#route for the event page
@app.route('/events')
def events():
    sort_by = request.args.get('sort', 'recommended')  # get sort param from URL

    query = 'SELECT * FROM events'
    if sort_by == 'date':
        query += ' ORDER BY start_date ASC, start_time ASC'
    elif sort_by == 'price':
        query += ' ORDER BY budget ASC'  # this depends on how you store "budget"
    elif sort_by == 'rating':
        query += ' ORDER BY rating DESC'  # only if you have a rating column
    elif sort_by == 'alphabetical':
        query += ' ORDER BY title COLLATE NOCASE ASC' 

    connection = get_db_connection()
    events = connection.execute(query).fetchall()
    connection.close()
    return render_template('events.html', events=events, current_sort=sort_by)

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

#route to create an event - with POST handling 
@app.route('/create-event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title       = request.form['title']
        description = request.form['description']
        startDate   = request.form['startDate']
        startTime   = request.form['startTime']
        endDate     = request.form['endDate']
        endTime     = request.form['endTime']
        location    = request.form['location']
        attendees = request.form.get('attendees', '0')

        image_file = request.files['image']
        if image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], image_filename))
        else:
            image_filename = None
        conn = get_db_connection()
        conn.execute(
        'INSERT INTO events (title, description, start_date, start_time, end_date, end_time, location, attendees, image) '
        'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (title, description, startDate, startTime, endDate, endTime, location, attendees, image_filename)
        )
        conn.commit()
        conn.close()
        return redirect(url_for('events'))

    return render_template('createevent.html')

@app.route('/delete-event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    con = get_db_connection()
    con.execute('DELETE FROM events WHERE id = ?', (event_id,))
    con.commit()
    con.close()
    flash("Event deleted.", "info")
    return redirect(url_for('events'))

if __name__ == '__main__':
    app.run(debug=True)
