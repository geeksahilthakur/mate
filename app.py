from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Use random secret key for session security

# Sample username and password (should ideally be stored securely)
USERNAME = 'matedev'
PASSWORD = '4117'

DATA_FILE = 'data.json'

# Load data from JSON file
def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data

# Save data to JSON file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return render_template('index.html', error=True)
    return render_template('index.html', error=False)

# Dashboard route - requires authentication
@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    data = load_data()
    return render_template('dashboard.html', data=data)

# Logout route
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))

# API endpoint to get all data
@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'GET':
        data = load_data()
        return jsonify(data)
    elif request.method == 'POST':
        if not session.get('logged_in'):
            return jsonify({'error': 'Authentication required'}), 401
        try:
            new_data = request.json
            current_data = load_data()
            current_data.update(new_data)
            save_data(current_data)
            return jsonify({'message': 'Data added successfully'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
