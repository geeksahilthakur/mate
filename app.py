from flask import Flask, request, session, redirect, url_for, render_template, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import os
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # replace with your secret key

users = {
    'matedev': generate_password_hash('4117')
}

DATA_FILE = 'data.json'

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/index', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in users and check_password_hash(users[username], password):
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password.'
    return render_template('index.html', error=error)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    data = load_data()
    return render_template('dashboard.html', data=data.items())

@app.route('/data', methods=['GET', 'POST', 'PUT', 'DELETE'])
def handle_data():
    if not session.get('logged_in'):
        return jsonify({'error': 'Authentication required'}), 401
    data = load_data()
    if request.method == 'GET':
        return jsonify(data)
    elif request.method == 'POST':
        new_data = request.json
        data.update(new_data)
        save_data(data)
        return jsonify({'message': 'Data added successfully'}), 200
    elif request.method == 'PUT':
        updated_data = request.json
        data.update(updated_data)
        save_data(data)
        return jsonify({'message': 'Data updated successfully'}), 200
    elif request.method == 'DELETE':
        for key in request.json.keys():
            data.pop(key, None)
        save_data(data)
        return jsonify({'message': 'Data deleted successfully'}), 200

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
