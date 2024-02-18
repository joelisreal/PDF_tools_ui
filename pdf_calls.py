from flask import Flask, render_template, request, redirect, session, url_for, send_file, send_from_directory, after_this_request, flash, Response, jsonify
import sqlite3
import os
from flask_sqlalchemy import SQLAlchemy
import subprocess
import zipfile

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "hello"
db = SQLAlchemy(app)

# if __name__ == '__main__':
#     db.create_all()
    # app.debug = True

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
# UPLOAD_FOLDER = 'uploads'
# DOWNLOAD_FOLDER = 'downloads'
# ALLOWED_EXTENSIONS = {'pdf'}

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

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
    # session['file'] = file
    session['filename'] = file.filename
    # Save file info in the database
    # db.create_all()
    print(file.filename)
    print(file_path)
    file_data = File(filename=file.filename, filepath=file_path, compressed_filepath='', status='uploaded')
    db.session.add(file_data)
    db.session.commit()
    # flash('File upload a success!', 'info')
    # return 'File uploaded successfully 456!'
    # return render_template('pdfcompress.html')
    return redirect('/')

    # # Save file info in the database
    # conn = sqlite3.connect('files.db')
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO files (filename, filepath, status) VALUES (?, ?, ?)",
    #                (file.filename, file_path, 'uploaded'))
    # conn.commit()
    # conn.close()
    # flash('File upload a success!', 'info')
    # return 'File uploaded successfully 456!'
    # return redirect(url_for("download"))
    # return redirect("pdfdownload.html")
    
    # return redirect(url_for('static', filename='pdfdownload.html'))

    # return redirect("download")
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
    # compress_pdf_with_ghostscript(file_data.filepath, output_file)
    file_data.status = 'compressed'
    db.session.commit()
    # return 'Compression complete!'
    # return render_template('pdfdownload.html')
    return redirect(url_for('download'))

# @app.route('')
# @app.route('/compress', methods=['POST'])
# def compress():
#     conn = sqlite3.connect('files.db')
#     cursor = conn.cursor()

#     # Get files to compress from the database
#     cursor.execute("SELECT * FROM files WHERE status=?", ('uploaded',))
#     files_to_compress = cursor.fetchall()

#     # Compress files and update the database
#     for file_info in files_to_compress:
#         # ... Your compression logic here ...
#         # compressed_file_path = compress_file(file_info['filepath'])
#         # compressed_file_path = compress_pdf_with_ghostscript(file_info['filepath'], file_info['filename'])
#         compress_pdf_with_ghostscript(file_info['filepath'], compressed_file_path)
#         cursor.execute("UPDATE files SET compressed_filepath=?, status=? WHERE id=?",
#                        (compressed_file_path, 'compressed', file_info['id']))

#     conn.commit()
#     conn.close()

#     return 'Compression complete!'

# def compress_pdf_with_ghostscript(input_path, output_path):
#     gs_command = [
#         'gs',
#         '-sDEVICE=pdfwrite',
#         '-dCompatibilityLevel=1.4',
#         '-dPDFSETTINGS=/ebook',
#         '-dNOPAUSE',
#         '-dBATCH',
#         f'-sOutputFile={output_path}',
#         input_path
#     ]

#     try:
#         subprocess.run(gs_command, check=True)
#         print("PDF compression completed successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"Error occurred during PDF compression: {e}")

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





    # if "file" in session:
    #     file = session['file']
    # filename = session['filename']
    # file_data = File.query.filter_by(filename=filename).first()
    # print(file_data.filepath)
    # # return send_file(file_data.filepath)
    # return send_from_directory('uploads', filename, as_attachment=True)
    # response = send_from_directory('uploads', filename, as_attachment=True)
    # response.headers["Content-Disposition"] = "attachment; filename={}".format(filename)
    # response.headers["Content-Type"] = "application/pdf"
    # return response
    #     if file_data is None:
    #         abort(404)  # File not found
    #     return send_file(file_data.filepath, as_attachment=True)
    # if "file" in session:
    #     file = session['file']
    #     return send_file(file.filename, as_attachment=True)

#     conn = sqlite3.connect('files.db')
#     cursor = conn.cursor()

#     # Get compressed files from the database
#     cursor.execute("SELECT compressed_filepath FROM files WHERE status=?", ('compressed',))
#     compressed_files = cursor.fetchall()

#     conn.close()

#     # Package and send files for download (you'll need to implement this part)

    # return 'Download initiated!'


# @app.route('/upload', methods=['POST'])
# def upload():
#     file = request.files['file']
#     # Save file on the server
#     file_path = os.path.join('uploads', file.filename)
#     file.save(file_path)
#     # Save file info in the database
#     file_data = File(filename=file.filename, filepath=file_path, compressed_filepath='', status='uploaded')
#     db.session.add(file_data)
#     db.session.commit()
#     # Redirect to the download route for the uploaded file
#     return redirect(url_for('download', filename=file.filename))


# @app.route('/download/<filename>')
# def download(filename):
#     file_data = File.query.filter_by(filename=filename).first()
#     if file_data:
#         return send_from_directory('uploads', filename, as_attachment=True)
#     else:
#         # Handle case where file does not exist
#         return 'File not found'
        
# # @app.route('/download/<filename>', methods=['GET'])
# # def download_file(filename):
# #     return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

# @app.route('/remove/<int:file_id>', methods=['DELETE'])
# def remove(file_id):
#     conn = sqlite3.connect('files.db')
#     cursor = conn.cursor()

#     # Get file info from the database
#     cursor.execute("SELECT * FROM files WHERE id=?", (file_id,))
#     file_info = cursor.fetchone()

#     # Remove file from storage
#     os.remove(file_info['filepath'])

#     # Remove file info from the database
#     cursor.execute("DELETE FROM files WHERE id=?", (file_id,))
#     conn.commit()
#     conn.close()

#     return 'File removed successfully!'

if __name__ == '__main__':
    # db.create_all()
    app.run(debug=True)

# # from flask import Flask, render_template, request

# # app = Flask(__name__)

# # @app.route('/compress', methods=['POST'])
# # def compress():
# #     # Call your Python script here
# #     os.system('python compress_pdf_ghostscript.py')
# #     return 'Compression complete!'

# from flask import Flask, render_template, request, jsonify
# import os
# import subprocess
# import sys

# app = Flask(__name__)

# @app.route('/')
# def index():
#     print('hello')
#     return render_template('pdfcompress.html')

# @app.route('/compress', methods=['POST'])
# def compress():
#     # Get the objectUrls from the POST request data
#     # object_urls = request.form.getlist('objectUrls')
#     # object_urls = request.get_json()
#     # object_urls = request.json['objectUrls']
#     # object_urls = request.form['objectUrls']
#     # Get the JSON data from the POST request
#     data = request.get_json()

#     # Extract the objectUrls from the JSON data
#     object_urls = data.get('objectUrls', [])

#     # Now you can do something with the list of object URLs
#     print(object_urls)
    
#     # Set input_paths to object_urls
#     # input_paths = ' '.join(object_urls)
#     # global input_paths
#     input_paths = object_urls
#     input_file = 'PSET 2.pdf'

#     # output_paths = [f"output_{i}.pdf" for i in range(len(input_paths))]
#     output_file = 'output_compressed_gs.pdf'
#     # for (input_path, output_path) in zip(input_paths, output_paths):
#     compress_pdf_with_ghostscript(input_path, output_path)

#     # Now you can do something with the inputpath
#     # print(input_paths)
    
#     # Call your Python script here
#     # os.system(f'python3 static/assets/py/compress_pdf_ghostscript.py {input_paths}')

#     # Call your Python script here
#     # os.system('python3 compress_pdf_ghostscript.py')
#     # os.system('python3 static/assets/py/compress_pdf_ghostscript.py')
#     return 'Compression complete!'


# # import subprocess
# # import sys

# def compress_pdf_with_ghostscript(input_path, output_path):
#     gs_command = [
#         'gswin64c',
#         '-sDEVICE=pdfwrite',
#         '-dCompatibilityLevel=1.4',
#         '-dPDFSETTINGS=/ebook',
#         '-dNOPAUSE',
#         '-dBATCH',
#         f'-sOutputFile={output_path}',
#         input_path
#     ]

#     try:
#         subprocess.run(gs_command, check=True)
#         print("PDF compression completed successfully.")
#     except subprocess.CalledProcessError as e:
#         print(f"Error occurred during PDF compression: {e}")


# if __name__ == '__main__':
#     app.run(debug=True)

# # from flask import Flask, render_template, request, jsonify
# # import os
# # import compress_pdf_ghostscript

# # app = Flask(__name__)

# # @app.route('/')
# # def index():
# #     print('hello')
# #     return render_template('pdfcompress.html')

# # @app.route('/compress', methods=['POST'])
# # def compress():
# #     # Get the JSON data from the POST request
# #     data = request.get_json()

# #     # Extract the objectUrls from the JSON data
# #     object_urls = data.get('objectUrls', [])

# #     # Now you can do something with the list of object URLs
# #     print(object_urls)

# #     # Call your Python script here using the object URLs
# #     input_paths = object_urls  # Assuming object_urls is a list of file paths
# #     output_paths = []  # You need to define how you want to handle output paths

# #     compress_pdf_with_ghostscript(input_paths, output_paths)

# #     return 'Compression complete!'

# # if __name__ == '__main__':
# #     app.run()
