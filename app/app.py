
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, g, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
DATABASE = '/home/mcipks/Desktop/New Folder 1/help_desk_system/database/help_desk.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('../database/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')

@app.route('/')
def index():
    db = get_db()
    tickets = db.execute('SELECT * FROM tickets').fetchall()
    return render_template('index.html', tickets=tickets)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), role),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("login"))
        flash(error)

    return render_template('register.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        urgency = request.form['urgency']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO tickets (title, description, urgency, user_id) VALUES (?, ?, ?, ?)',
                (title, description, urgency, 1) # Replace 1 with the actual user_id
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('create_ticket.html')

def get_open_tickets_by_technician(technician_id):
    db = get_db()
    tickets = db.execute(
        'SELECT * FROM tickets WHERE user_id = ? AND status != "Closed"',
        (technician_id,)
    ).fetchall()
    return tickets

def calculate_average_resolution_time():
    db = get_db()
    avg_time = db.execute(
        'SELECT AVG(julianday(resolved_at) - julianday(created_at)) FROM tickets WHERE status = "Resolved"'
    ).fetchone()[0]
    return avg_time

def get_tickets_by_urgency_report():
    db = get_db()
    report = db.execute(
        'SELECT urgency, COUNT(*) as count FROM tickets GROUP BY urgency'
    ).fetchall()
    return report

@app.route('/reports')
def reports():
    open_tickets = get_open_tickets_by_technician(1) # Example technician_id
    avg_resolution_time = calculate_average_resolution_time()
    urgency_report = get_tickets_by_urgency_report()
    return render_template('reports.html',
                           open_tickets=open_tickets,
                           avg_resolution_time=avg_resolution_time,
                           urgency_report=urgency_report)

if __name__ == '__main__':
    app.run(debug=True)
