# Imports
from flask import Flask, request, jsonify, send_file, render_template
import os

# Ensure Flask serves HTML from "templates"
app = Flask(__name__, template_folder="templates")

# Init upload folder
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Serve the Web UI - default route
@app.route('/')
def upload_page():
    return render_template('web_based_ui.html') # specify the html page where the file will be uploaded

# Upload API - upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # **Save file with its original name**
    # file_path = os.path.join(UPLOAD_FOLDER, "latest_file.xlsx") # you specify the file name and extn
    file_path = os.path.join(UPLOAD_FOLDER, file.filename) # upload any file as it is oth name and extn
    file.save(file_path)

    return jsonify({"message": "File uploaded successfully", "file_path": file_path})

# Download API - download route
@app.route('/download', methods=['GET'])
def download_file():
    filename = request.args.get("filename")  # Get filename from URL parameters
    
    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, filename)  # Correct file path generation

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)  # Send the file for download
    return jsonify({"error": "File not found"}), 404  # Handle missing file case

# if __name__ == '__main__':
    # port = int(os.environ.get('PORT', 10000))  # Render assigns a dynamic port
    # app.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Read port from environment variable
    app.run(host="0.0.0.0", port=port)
