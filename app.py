from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

USERNAME = 'm'
PASSWORD = 'M11T3'


def load_data():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    return data

def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)


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


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    data = load_data()
    return render_template('dashboard.html', data=data)


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('login'))


@app.route('/data', methods=['GET'])
def get_data():
    data = load_data()
    return jsonify(data)


@app.route('/add_data', methods=['POST'])
def add_data():
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
    app.run(debug=False, host='0.0.0.0')
