import requests

FILE_SERVER_URLS = ['http://localhost:5001']  # Add more URLs for each replica
METADATA_SERVER_URL = 'http://localhost:5002'

def upload_file(file_path):
    with open(file_path, 'rb') as file:
        for url in FILE_SERVER_URLS:
            response = requests.post(f'{url}/upload', files={'file': file})
            print(response.json())

def download_file(filename):
    for url in FILE_SERVER_URLS:
        response = requests.get(f'{url}/download/{filename}')
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                file.write(response.content)
            print('File downloaded successfully')
            return
    print('File not found')

def register_file(filename):
    data = {'filename': filename, 'locations': FILE_SERVER_URLS}
    response = requests.post(f'{METADATA_SERVER_URL}/register', json=data)
    print(response.json())

def get_file_locations(filename):
    response = requests.get(f'{METADATA_SERVER_URL}/get_locations/{filename}')
    print(response.json())

# Example usage
upload_file('example.txt')
register_file('example.txt')
get_file_locations('example.txt')
download_file('example.txt')
