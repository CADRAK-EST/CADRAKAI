from flask import Blueprint, request, jsonify
import os
import requests
import logging
from app.logging_config import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

main = Blueprint('main', __name__)

UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@main.route('/')
def index():
    return jsonify({"message": "DXF Parser API"})

@main.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logger.error("No file part in request")
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        logger.error("No selected file")
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.dxf'):  # Check if the file is a .dxf file
        logger.error("Invalid file type. Only .dxf files are allowed")
        return jsonify({"error": "Invalid file type. Only .dxf files are allowed"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    logger.info(f"File uploaded successfully: {file_path}")
    return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200

@main.route('/parse', methods=['POST'])
def parse_file():
    data = request.get_json()
    if not data or 'file_path' not in data:
        logger.error("No file path provided")
        return jsonify({"error": "No file path provided"}), 400

    file_path = data['file_path']
    if not os.path.exists(file_path):
        logger.error(f"File does not exist: {file_path}")
        return jsonify({"error": "File does not exist"}), 404

    try:
        with open(file_path, 'rb') as f:
            response = requests.post('http://localhost:5001/parse', files={'file': f})
        response_data = response.json()
        if response.status_code == 200:
            logger.info(f"File {file_path} parsed successfully")
        else:
            logger.error(f"Failed to parse file {file_path}: {response_data}")
        return jsonify(response_data), response.status_code
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to communicate with CADRAK Engine: {str(e)}")
        return jsonify({"error": "Failed to communicate with CADRAK Engine"}), 500
