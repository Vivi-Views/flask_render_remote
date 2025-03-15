# Imports
from flask import Flask, request, jsonify, send_file, render_template
import os
import sys  # Import sys to force immediate printing
import shutil

#-------------------------------XXX-------------------------------

# get flask api key from env vars
API_KEY = os.getenv("FLASK_API_KEY")  # Get API key from environment variables

# Chk api key
def check_api_key():
    """Checks if the correct API key is provided in request headers."""
    api_key = request.headers.get("x-api-key")  # Read API key from request headers
    
    if api_key != API_KEY:
        print("❌ Unauthorized access attempt!", flush=True)  # Ensure immediate printing
        sys.stdout.flush()  # Force terminal output
        return jsonify({"error": "Unauthorized"}), 403  # Deny access
    
    print("✅ Authorized API KEY", flush=True)  # Force immediate print on authorization
    sys.stdout.flush()  # Flush output to ensure it appears in the logs
    
    return None  # No response needed if authorized (continue execution)

#-------------------------------XXX-------------------------------

# Initialize Flask & set template folder
app = Flask(__name__, template_folder="templates")

#-------------------------------XXX-------------------------------

# Upload folder setup
UPLOAD_FOLDER = "uploaded_files"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#-------------------------------XXX-------------------------------

### Secure the Web UI - Default Route ###
@app.route('/')
def upload_page():
    auth = check_api_key()  # Verify API key before serving the page
    if auth:
        return auth  # Return 403 Unauthorized if API key is missing/invalid
    
    return render_template('Sanaatanam.html')  # Serve your HTML file

#-------------------------------XXX-------------------------------

### Secure the Web UI - Newpage Route ###
@app.route('/newpage')
def new_page():
    auth = check_api_key()  # Verify API key before serving the page
    if auth:
        return auth  # Return 403 Unauthorized if API key is missing/invalid
    
    return render_template('Vivi.html')  # Serve your HTML file


#-------------------------------XXX-------------------------------

### Upload API - Upload File ###
@app.route('/upload', methods=['POST'])
def upload_file():
    auth = check_api_key()  # Verify API key before serving the page
    if auth:
        return auth  # Return 403 Unauthorized if API key is missing/invalid

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Save file with its original name
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    return jsonify({"message": "File uploaded successfully", "file_path": file_path})

#-------------------------------XXX-------------------------------

### Download API - Download File ###
@app.route('/download', methods=['GET'])
def download_file():
    auth = check_api_key()  # Verify API key before serving the page
    filename = request.args.get("filename")  # Get filename from request

    if not filename:
        return jsonify({"error": "No filename provided"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)  # Serve file for download
    return jsonify({"error": "File not found"}), 404  # Handle file not found

#-------------------------------XXX-------------------------------

### List Uploaded Files ###
@app.route('/list-files', methods=['GET'])
def list_files():
    auth = check_api_key()  # Verify API key before serving the page
    files = os.listdir(UPLOAD_FOLDER)  # Get list of all uploaded files
    return jsonify({"files": files})  # Return the file list as JSON

#-------------------------------XXX-------------------------------

### Clear All Files from Render Server ###
@app.route('/clear-files', methods=['POST'])
def clear_files():
    auth = check_api_key()  # Verify API key before proceeding
    if auth:
        return auth  # If unauthorized, return 403 and stop execution

    try:
        if os.path.exists(UPLOAD_FOLDER):
            # Delete all files in the directory
            for filename in os.listdir(UPLOAD_FOLDER):
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"🗑️ Deleted: {file_path}")

            return jsonify({"message": "All files deleted successfully"}), 200
        else:
            return jsonify({"message": "Folder already empty"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#-------------------------------XXX-------------------------------

### Run the Flask Server ###
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Default to port 5000
    app.run(host="0.0.0.0", port=port, debug=True)  # Debug mode for easy error tracking
