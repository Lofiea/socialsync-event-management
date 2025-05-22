from flask import Flask, render_template, request, redirect
from eventRoutes import events_bp
import sqlite3

app = Flask(__name__)
app.register_blueprint(events_bp)

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect('socialsync.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/createevent', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        data = request.form
        image_urls = request.form.get('images', '')

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO events 
            (name, start_date, start_time, end_date, end_time, location, is_offline, capacity, is_unlimited,
             visibility, host, age_tag, event_type, budget, notes, image_urls)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'], data['startDate'], data['startTime'], data['endDate'], data['endTime'],
            data['location'], data.get('isOffline') == 'on', data.get('capacity') or None,
            data.get('isUnlimited') == 'on', data['visibility'], data['host'], data['ageTag'],
            data['eventType'], data['budget'], data['notes'], image_urls
        ))
        conn.commit()
        conn.close()
        return redirect('/events')

    return render_template('createevent.html')

@app.route('/events')
def events():
    conn = get_db_connection()
    events = conn.execute('SELECT * FROM events').fetchall()
    conn.close()
    return render_template('events.html', events=events)

if __name__ == '__main__':
    app.run(debug=True)