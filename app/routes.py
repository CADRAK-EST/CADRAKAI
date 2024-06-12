from flask import Blueprint, request, jsonify
import os
from app.dxf_parser import parse_dxf

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
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.dxf'):  # Check if the file is a .dxf file
        return jsonify({"error": "Invalid file type. Only .dxf files are allowed"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return jsonify({"message": "File uploaded successfully", "file_path": file_path}), 200

@main.route('/parse', methods=['POST'])
def parse_file():
    data = request.get_json()
    if not data or 'file_path' not in data:
        return jsonify({"error": "No file path provided"}), 400

    file_path = data['file_path']
    if not os.path.exists(file_path):
        return jsonify({"error": "File does not exist"}), 404

    parsed_data = parse_dxf(file_path)
    return jsonify({"message": f"File {file_path} parsed successfully", "parsed_data": parsed_data}), 200