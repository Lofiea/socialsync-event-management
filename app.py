from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)  
app.config['SECRET_KEY'] = '4653'
# SQLite database file will be created in the project root
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/dishitasingh/CI-03/the-party-website/instance/users.db'     
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ----------------------------------------
# Models
# ----------------------------------------
class User(db.Model):
    id       = db.Column(db.Integer, primary_key=True)
    name     = db.Column(db.String(100), nullable=False)
    email    = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # hashed

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }


# ----------------------------------------
# Routes
# ----------------------------------------
@app.before_request
with app.app_context():
    db.create_all()

'''def create_tables():
    db.create_all()'''


@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        email    = request.form.get('email', '').strip().lower()
        pw       = request.form.get('password', '')
        confirm  = request.form.get('confirm-password', '')

        if not name or not email or not pw:
            flash('Name, email, and password are required', 'error')
        elif pw != confirm:
            flash('Passwords do not match', 'error')
        elif User.query.filter_by(email=email).first():
            flash('Email already registered', 'error')
        else:
            hashed = generate_password_hash(pw)
            new_user = User(name=name, email=email, password=hashed)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created! Please log in.', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            flash(f'Welcome back, {user.name}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    return '<h1>🎉 You’re logged in! Welcome to your dashboard.</h1>'

@app.route('/users')
def list_users():
    """Returns JSON of all registered users (no passwords)."""
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


# Stub routes for the other navbar links
@app.route('/about')
def about():
    return '<h1>About Us – Coming Soon</h1>'

@app.route('/faq')
def faq():
    return '<h1>FAQ – Coming Soon</h1>'

@app.route('/contact')
def contact():
    return '<h1>Contact – Coming Soon</h1>'

@app.route('/host-event')
def host_event():
    return '<h1>Host Event – Coming Soon</h1>'


if __name__ == '__main__':
    # ensure the DB file exists
    if not os.path.exists('users.db'):
        open('users.db', 'a').close()
    app.run(debug=True)