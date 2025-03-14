# Imports
from flask import Flask, request, jsonify, send_file, render_template
import os

# Initialize Flask & set template folder
app = Flask(__name__, template_folder="templates")

# Upload folder setup
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

### Serve the Web UI - Default Route ###
@app.route('/')
def upload_page():
    return render_template('Sanaatanam.html')  # Serves your HTML file

@app.route('/newpage')
def new_page():
    return render_template('Vivi.html')

### Upload API - Upload File ###
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save file with its original name
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({"message": "File uploaded successfully", "file_path": file_path})

### Download API - Download File ###
@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get("filename")  # Get filename from request

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)  # Serve file for download
    return jsonify({"error": "File not found"}), 404  # Handle file not found

### List Uploaded Files ###
@app.route('/list-files', methods=['GET'])
def list_files():
    files = os.listdir(UPLOAD_FOLDER)  # Get list of all uploaded files
    return jsonify({"files": files})  # Return the file list as JSON

### Run the Flask Server ###
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000
    app.run(host="0.0.0.0", port=port, debug=True)  # Debug mode for easy error tracking
