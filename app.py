from flask import Flask, render_template
from eventRoutes import events_bp

app = Flask(__name__)
app.register_blueprint(events_bp)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/events')
def events():
    return render_template('events.html')

if __name__ == '__main__':
    app.run(debug=True)
