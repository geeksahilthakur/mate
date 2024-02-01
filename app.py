from flask import Flask, request, jsonify, render_template
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import os
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '4117'  # Secret key set to '4117'

users = {
    'matedev': generate_password_hash('4117')
}

tokens = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and check_password_hash(users[username], password):
            s = Serializer(app.config['SECRET_KEY'], expires_in=3600)
            token = s.dumps({'username': username}).decode('utf-8')
            tokens[token] = username
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password.'
    return render_template('index.html', error=error)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    data = load_data()
    return render_template('dashboard.html', data=data)

@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    token = request.headers.get('Authorization')
    if token not in tokens:
        return jsonify({'error': 'Authentication required'}), 401
    # rest of your code here

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
