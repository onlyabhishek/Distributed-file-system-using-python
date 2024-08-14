from flask import Flask, request, send_file, jsonify
import os

app = Flask(__name__)
FILE_STORAGE_DIR = 'files'
REPLICA_COUNT = 3  # Number of replicas

# Ensure storage directories exist
for i in range(REPLICA_COUNT):
    replica_dir = os.path.join(FILE_STORAGE_DIR, f'replica_{i}')
    if not os.path.exists(replica_dir):
        os.makedirs(replica_dir)

def save_file(file, filename):
    for i in range(REPLICA_COUNT):
        replica_dir = os.path.join(FILE_STORAGE_DIR, f'replica_{i}')
        file_path = os.path.join(replica_dir, filename)
        file.save(file_path)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    filename = file.filename
    save_file(file, filename)
    return jsonify({'message': 'File uploaded and replicated successfully'}), 200

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    for i in range(REPLICA_COUNT):
        file_path = os.path.join(FILE_STORAGE_DIR, f'replica_{i}', filename)
        if os.path.exists(file_path):
            return send_file(file_path)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(port=5001)
