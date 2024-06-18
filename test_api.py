import requests
import os
import json

UPLOAD_URL = 'http://localhost:5000/upload'
PARSE_URL = 'http://localhost:5000/parse'
TEST_ZIP_FILE = 'Kaur2_only2D.dxf'  # Path to your test ZIP file
OUTPUT_FOLDER = 'output_jsons'

if not os.path.exists(OUTPUT_FOLDER):
    os.makedirs(OUTPUT_FOLDER)

# Step 1: Upload the ZIP file
def upload_file(file_path):
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(UPLOAD_URL, files=files)
        response.raise_for_status()
        return response.json()['file_path']

# Step 2: Parse the uploaded file and save JSONs
def parse_file(file_path):
    response = requests.post(PARSE_URL, json={'file_path': file_path}, stream=True)
    response.raise_for_status()

    for index, chunk in enumerate(response.iter_content(chunk_size=None)):
        if chunk:
            json_data = json.loads(chunk.decode('utf-8'))
            output_file = os.path.join(OUTPUT_FOLDER, f'page_{index + 1}.json')
            with open(output_file, 'w') as json_file:
                json.dump(json_data, json_file, indent=4)
            print(f'Saved: {output_file}')

if __name__ == '__main__':
    try:
        # Upload the file
        uploaded_file_path = upload_file(TEST_ZIP_FILE)
        print(f'Uploaded file path: {uploaded_file_path}')

        # Parse the file and save JSON responses
        parse_file(uploaded_file_path)
        print('All JSON files have been saved successfully.')

    except requests.RequestException as e:
        print(f'Error: {e}')
