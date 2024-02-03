from flask import Flask, request, jsonify
import json

app = Flask(__name__)
JSON_FILE = 'data.json'

# Helper function to read data from the JSON file
def read_data():
    try:
        with open(JSON_FILE, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []
    return data

# Helper function to write data to the JSON file
def write_data(data):
    with open(JSON_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Route to get all data
@app.route('/data', methods=['GET'])
def get_data():
    data = read_data()
    return jsonify(data)

# Route to add new data
@app.route('/data', methods=['POST'])
def add_data():
    new_data = request.json
    data = read_data()
    data.append(new_data)
    write_data(data)
    return jsonify(new_data), 201

# Route to update data by ID
@app.route('/data/<int:id>', methods=['PUT'])
def update_data(id):
    updated_data = request.json
    data = read_data()
    for item in data:
        if item.get('id') == id:
            item.update(updated_data)
            write_data(data)
            return jsonify(updated_data), 200
    return jsonify({'error': 'Data not found'}), 404

# Route to delete data by ID
@app.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    data = read_data()
    for index, item in enumerate(data):
        if item.get('id') == id:
            del data[index]
            write_data(data)
            return jsonify({'message': 'Data deleted'}), 200
    return jsonify({'error': 'Data not found'}), 404

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
