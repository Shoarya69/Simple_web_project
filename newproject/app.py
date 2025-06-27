from flask import Flask as fk, render_template, request,redirect, url_for, session,flash
from flask_mysqldb import MySQL
app = fk(__name__)
app.secret_key = "super-secret"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Shoarya@123'
app.config['MYSQL_DB'] = 'flask_login_db'

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()   
        cur.close()
        if user:
            session['username'] = user[1]  # Assuming the second column is username
            flash('Login successful')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        existing_user = cur.fetchone()
        if existing_user:
            flash('Username already exists. Please choose another.')
            cur.close()
            return redirect(url_for('register'))
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cur.close()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('login_register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return flash('You need to log in first'), redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])
if __name__ == '__main__':
    app.run(debug=True)