from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3 

app = Flask(__name__)
app.secret_key = 'supersecretkey' #Secret key for session management
#Database connection function 
def get_db_connection(): 
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row #Access data by column name 
    return connection 

#route for the home page 
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

#route for the signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST': 
        username = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm-password']

        if password != confirm: 
            error = "Passwords don't match."
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

#route for the profile page
@app.route('/profile')
def profile():
    return render_template('profile.html')

#route for the event page
@app.route('/events')
def events():
    connection = get_db_connection()
    events = connection.execute('SELECT * FROM events').fetchall()
    connection.close()
    return render_template('events.html', events=events)

#route for the event details page
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
@app.route('/create-event')
def create_event():
    if request.method == 'POST':
        #Get data from form 
        title = request.form['title']
        description = request.form['description']
        date = request.form['date']
        location = request.form['location'] 

        #insert data into the events table
        connection = get_db_connection()
        connection.execute('INSERT INTO events (title, description, date, location) VALUES (?, ?, ?, ?)',
                           (title, description, date, location))
        connection.commit()
        connection.close()

        #redirect to events page to see the new event 
        return redirect(url_for('events'))
    
    return render_template('createevent.html')

if __name__ == '__main__':
    app.run(debug=True)
