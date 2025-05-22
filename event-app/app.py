from flask import Flask, render_template, request, redirect, url_for
import sqlite3 

app = Flask(__name__)

# Database connection function 
def get_db_connection(): 
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection 

# Home page 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
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