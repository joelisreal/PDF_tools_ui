from flask import Flask, render_template, request, redirect, session, url_for, send_file, send_from_directory, after_this_request, flash, Response, jsonify
import sqlite3
import os
from flask_sqlalchemy import SQLAlchemy
import subprocess
import zipfile
from compress_pdf_ghostscript import compress_pdf_with_ghostscript

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
    file = request.files['file']
    print(file)
    # Save file on the server
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    session['filename'] = file.filename
    # Save file info in the database
    file_data = File(filename=file.filename, filepath=file_path, compressed_filepath='', status='uploaded')
    db.session.add(file_data)
    db.session.commit()
    # flash('File upload a success!', 'info')
    # return 'File uploaded successfully 456!'
    # return render_template('pdfcompress.html')
    return redirect('/')


@app.route('/compress')
def compress():
    # Get files to compress from the database
    
    filename = session['filename']
    file_data = File.query.filter_by(filename=filename).first()
    print(file_data.filepath)
    print(file_data.filename)
    # Compress files and update the database
    if not os.path.exists('compressed'):
        os.makedirs('compressed')
    
    # Append _gs to the filename
    output_file = os.path.join('compressed', file_data.filename.split('.')[0] + '_gs.pdf')
    print(output_file)
    compress_pdf_with_ghostscript(file_data.filepath, output_file)
    file_data.status = 'compressed'
    db.session.commit()
    # return 'Compression complete!'
    # return render_template('pdfdownload.html')
    return redirect(url_for('download'))


@app.route('/download')
def download():
    print(76)
    return render_template('pdfdownload.html')

@app.route('/download_all')
def download_all():
    # Path to the directory containing the compressed files
    compressed_dir = 'compressed'
    upload_dir = 'uploads'

    # Get the list of compressed files
    compressed_files = os.listdir(compressed_dir)
    
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

    # After this request, delete the zip file
    @after_this_request
    def remove_file(response):
        try:
            os.remove('AllFiles.zip')
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    # Send the zip file for download
    return send_file('AllFiles.zip', as_attachment=True)


if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)

