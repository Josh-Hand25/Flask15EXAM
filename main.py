from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = 'shh'

example_db = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root',
    password = '041510',
    database = "firstsql"
)

cursor = example_db.cursor()

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        sql = "SELECT Username, ThePassword FROM users WHERE Username = '"+username+"'"
        cursor.execute(sql)
        result = cursor.fetchall()

        if len(result) > 0 and result[0][1] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            message = 'Invalid username or password'
    return render_template('login.html', message=message)

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        sql = "SELECT Username, ThePassword FROM users WHERE Username = '"+username+"'"
        cursor.execute(sql)
        result = cursor.fetchall()
        
        if not username or not password:
            message = 'Please fill out all fields'
        elif password != confirm_password:
            message = 'Passwords do not match'
        elif len(result) > 0:
            message = 'Username already exists'
        else:
            sql = f"INSERT INTO users (Username, ThePassword) VALUES ('{username}', '{password}')"
            cursor.execute(sql)
            return redirect(url_for('login'))
            
    return render_template('register.html', message=message)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
