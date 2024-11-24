import threading
from flask import Flask, render_template, request, redirect, session, url_for, send_file, send_from_directory, after_this_request, flash, Response, jsonify
import sqlite3
import time
import os
from flask_sqlalchemy import SQLAlchemy
import subprocess
import zipfile
from static.assets.py.compress_pdf_ghostscript import compress_pdf_with_ghostscript

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "hello"
db = SQLAlchemy(app)


class File(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    filename = db.Column(db.String(100))
    filepath = db.Column(db.String(100))
    compressed_filepath = db.Column(db.String(100))
    status = db.Column(db.String(100))

    def __init__(self, filename, filepath, compressed_filepath, status):
        self.filename = filename
        self.filepath = filepath
        self.compressed_filepath = compressed_filepath
        self.status = status

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    print('hello')
    return render_template('pdfhome.html')

@app.route('/pdfcompress')
def pdf_compress():
    return render_template('pdfcompress.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        files = request.files.getlist('files')
        print(files)
        print(5)
        if not files:
            return jsonify({"error": "No files uploaded"}), 400

        for file in files:
            existing_file = File.query.filter_by(filename=file.filename).first()
            if existing_file:
                return jsonify({"error": f"File {file.filename} already uploaded"}), 400

            if not os.path.exists('uploads'):
                os.makedirs('uploads')

            file_path = os.path.join('uploads', file.filename)
            file.save(file_path)

            file_data = File(filename=file.filename, filepath=file_path, compressed_filepath='', status='uploaded')
            db.session.add(file_data)

        db.session.commit()
        # Query all the entries in the File model
        files = File.query.all()
        
        # Print each file entry in the console
        for file in files:
            print(f"ID: {file.id}, Filename: {file.filename}, Status: {file.status}")

        return jsonify({"message": f"{len(files)} files uploaded successfully!"})

    except Exception as e:
        # Catch any unexpected errors
        return jsonify({"error": f"File upload failed: {str(e)}"}), 500


@app.route('/compress')
def compress():
    # Get all files to compress from the database
    files_to_compress = File.query.filter_by(status='uploaded').all()

    # Check if there are files to compress
    if not files_to_compress:
        return jsonify({"error": "No files to compress"}), 400
    
    # Compress files and update the database
    if not os.path.exists('compressed'):
        os.makedirs('compressed')

    # Compress each file
    for file_data in files_to_compress:
        # Original file path
        original_file = file_data.filepath

        # Append _gs to the filename for the compressed file path
        output_file = os.path.join('compressed', file_data.filename.split('.')[0] + '_gs.pdf')
        
        # Compress the file
        compress_pdf_with_ghostscript(original_file, output_file)

        # Get sizes of the original and compressed files
        original_size = os.path.getsize(original_file)
        compressed_size = os.path.getsize(output_file)

        # Compare sizes and proceed if the compressed file is smaller or equal
        if compressed_size <= original_size:
            # Update the database with the compressed file path and status
            file_data.compressed_filepath = output_file
            file_data.status = 'compressed'
        else:
            # If the compressed file is larger, don't update the file data and delete the compressed file
            os.remove(output_file)
            file_data.compressed_filepath = ''
            file_data.status = 'compression_failed'

        # Update the database with the compressed file path and status
        file_data.compressed_filepath = output_file
        file_data.status = 'compressed'
        db.session.commit()
    return jsonify({'redirect_to': url_for('download')})


@app.route('/download')
def download():
    return render_template('pdfdownload.html')

@app.route('/download_all')
def download_all():
    # Path to the directory containing the compressed files
    compressed_dir = 'compressed'
    upload_dir = 'uploads'

    # Get the list of compressed files
    compressed_files = os.listdir(compressed_dir)

    # Create a zip file
    zipf = zipfile.ZipFile('AllFiles.zip', 'w', zipfile.ZIP_DEFLATED)
    # for root, dirs, files in os.walk(compressed_dir):
    for file in compressed_files:
        # Add the file to the zip file
        # The arcname parameter is used to store the file under its filename only, not the full path
        zipf.write(os.path.join(compressed_dir, file), arcname=file)
    zipf.close()


    # Send the zip file for download
    return send_file('AllFiles.zip', as_attachment=True)

@app.after_request
def after_request(response):
    """Performs cleanup after each response, only if appropriate."""
    if request.endpoint in ['download_all']:
        clean_up_files_and_db()
    return response

def clean_up_files_and_db():
    """Deletes all files in the upload and compressed directories and clears the database."""
    try:
        # Remove files from the filesystem
        upload_dir = 'uploads'
        compressed_dir = 'compressed'

        # Delete uploaded files
        for file in os.listdir(upload_dir):
            os.remove(os.path.join(upload_dir, file))

        # Delete compressed files
        for file in os.listdir(compressed_dir):
            os.remove(os.path.join(compressed_dir, file))

        # Function to delete the zip file after the response is sent
        def delete_zip_file():
            time.sleep(3)  # Wait for a moment to ensure file is fully sent
            try:
                os.remove('AllFiles.zip')
            except Exception as error:
                app.logger.error(f"Error removing or closing downloaded file handle: {error}")

        # Start the background thread to delete the zip file
        threading.Thread(target=delete_zip_file).start()
        
        # Clear the database
        File.query.delete()
        db.session.commit()
        print("Files and database cleared successfully.")

    except Exception as error:
        print(f"Error clearing files and database: {error}")

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)

