from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this to a more secure key

# Sample username and password
USERNAME = 'matedev'
PASSWORD = 'M11T3'

# Load data from JSON file
def load_data():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data

# Save data to JSON file
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
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
@app.route('/data', methods=['GET'])
def get_data():
    data = load_data()
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
