from flask import Flask, request, render_template_string
import os
import sqlite3
import subprocess

app = Flask(__name__)

# VULNERABILITY 1: Hardcoded Secret
app.config['SECRET_KEY'] = 'super-secret-key-12345'
DB_PASSWORD = "admin123"
API_KEY = "sk_live_1234567890abcdef"

@app.route('/')
def home():
    return '''
    <h1>Vulnerable Application</h1>
    <ul>
        <li><a href="/search?q=test">Search</a></li>
        <li><a href="/user/admin">User Profile</a></li>
        <li><a href="/execute?cmd=ls">Execute Command</a></li>
    </ul>
    '''

# VULNERABILITY 2: SQL Injection
@app.route('/user/<username>')
def get_user(username):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '" + username + "'"
    cursor.execute(query)
    return str(cursor.fetchall())

# VULNERABILITY 3: Command Injection
@app.route('/execute')
def execute_command():
    cmd = request.args.get('cmd', 'whoami')
    result = os.system(cmd)
    return f'Command executed: {result}'

# VULNERABILITY 4: Server-Side Template Injection
@app.route('/search')
def search():
    query = request.args.get('q', '')
    template = '<h2>Search results for: ' + query + '</h2>'
    return render_template_string(template)

# VULNERABILITY 5: Using shell=True
@app.route('/ping')
def ping():
    host = request.args.get('host', 'localhost')
    result = subprocess.call(f'ping -c 1 {host}', shell=True)
    return f'Ping result: {result}'

# VULNERABILITY 6: Debug mode in production
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)