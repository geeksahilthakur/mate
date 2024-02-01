from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # replace with your secret key

users = {
    'matedev': generate_password_hash('4117')
}

tokens = {}

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    if username in users and check_password_hash(users[username], password):
        s = Serializer(app.config['SECRET_KEY'], expires_in=3600)
        token = s.dumps({'username': username}).decode('utf-8')
        tokens[token] = username
        return jsonify({'token': token}), 200
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/data', methods=['GET', 'POST'])
def handle_data():
    token = request.headers.get('Authorization')
    if token not in tokens:
        return jsonify({'error': 'Authentication required'}), 401
    # rest of your code here

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
