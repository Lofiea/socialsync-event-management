from flask import Flask, render_template, request, redirect, url_for
import sqlite3 

app = Flask(__name__)
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
@app.route('/login')
def login():
    return render_template('login.html')

#route for the signup page
@app.route('/signup')
def signup():
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
