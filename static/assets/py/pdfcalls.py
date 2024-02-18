# # from flask import Flask, render_template, request

# # app = Flask(__name__)

# # @app.route('/compress', methods=['POST'])
# # def compress():
# #     # Call your Python script here
# #     os.system('python compress_pdf_ghostscript.py')
# #     return 'Compression complete!'

# from flask import Flask, render_template, request
# import os

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('pdf.html')

# @app.route('/compress', methods=['POST'])
# def compress():
#     # Call your Python script here
#     os.system('python assets/py/compress_pdf_ghostscript.py')
#     return 'Compression complete!'

# if __name__ == '__main__':
#     app.run()
