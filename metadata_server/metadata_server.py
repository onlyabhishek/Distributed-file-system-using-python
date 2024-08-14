from flask import Flask, request, jsonify

app = Flask(__name__)
metadata = {}

@app.route('/register', methods=['POST'])
def register_file():
    data = request.json
    filename = data['filename']
    locations = data['locations']  # List of server URLs
    metadata[filename] = locations
    return jsonify({'message': 'File registered successfully'}), 200

@app.route('/get_locations/<filename>', methods=['GET'])
def get_locations(filename):
    locations = metadata.get(filename)
    if locations:
        return jsonify({'locations': locations}), 200
    else:
        return jsonify({'error': 'Metadata not found'}), 404

if __name__ == '__main__':
    app.run(port=5002)
