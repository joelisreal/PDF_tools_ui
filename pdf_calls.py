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
        file = request.files['file']
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Save the file on the server
        if not os.path.exists('uploads'):
            os.makedirs('uploads')

        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        session['filename'] = file.filename

        # Save file info in the database
        file_data = File(filename=file.filename, filepath=file_path, compressed_filepath='', status='uploaded')
        db.session.add(file_data)
        db.session.commit()

        return jsonify({"message": "File uploaded successfully!", "filename": file.filename})

    except Exception as e:
        # Catch any unexpected errors
        return jsonify({"error": f"File upload failed: {str(e)}"}), 500


@app.route('/compress')
def compress():
    # Get files to compress from the database
    filename = session['filename']
    file_data = File.query.filter_by(filename=filename).first()
    print(file_data.filepath)
    print(file_data.filename)
    print(file_data)
    # Compress files and update the database
    if not os.path.exists('compressed'):
        os.makedirs('compressed')
    
    # Append _gs to the filename
    output_file = os.path.join('compressed', file_data.filename.split('.')[0] + '_gs.pdf')
    print(output_file)
    print(file_data)
    compress_pdf_with_ghostscript(file_data.filepath, output_file)
    file_data.status = 'compressed'
    db.session.commit()
    # return 'Compression complete!'
    # return render_template('pdfdownload.html')
    # return redirect(url_for('download'))
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
    print(compressed_files)
    # Get the list of uploaded files
    upload_files = os.listdir(upload_dir)

    # Create a zip file
    zipf = zipfile.ZipFile('AllFiles.zip', 'w', zipfile.ZIP_DEFLATED)
    # for root, dirs, files in os.walk(compressed_dir):
    for file in compressed_files:
        # Add the file to the zip file
        # The arcname parameter is used to store the file under its filename only, not the full path
        zipf.write(os.path.join(compressed_dir, file), arcname=file)
        # for file in files:
            # zipf.write(os.path.join(root, file))
    zipf.close()

    # Delete the files in the upload and compressed directories
    for file in upload_files:
        os.remove(os.path.join(upload_dir, file))
    for file in compressed_files:
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

    # Send the zip file for download
    return send_file('AllFiles.zip', as_attachment=True)


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)

