# PDF Tools UI

Welcome to the PDF Tools UI! This project aims to provide a user-friendly interface for performing various operations on PDF files, starting with compression.

## Compress PDF Files

Currently, the only functionality available is PDF compression. This compression is performed using Ghostscript, specifically its pdfwrite device. It's important to note that Ghostscript's pdfwrite device doesn't always 'compress' files in the traditional sense. While it often results in smaller file sizes, the process involves various settings that may trade quality for file size. 

### Understanding Compression Settings

Ghostscript provides a range of options, known as `PDFSETTINGS`, which control the compression process. These settings cover a multitude of different controls, including downsampling images to reduce quality and file size. It's crucial to understand the implications of these settings and how they affect the output PDF file.

Each control within the `PDFSETTINGS` groups is individually available for fine-tuning. These controls are documented [here](ghostscript.com/doc/9.54.0/VectorDevices.htm#PDFWRITE). 

### Usage

To run the web application, follow these steps:

1. Clone the repository.
2. Navigate to the project directory.
3. Open a terminal window.
4. Set the Flask app:
    ```
    export FLASK_APP=pdf_calls.py
    ```
5. Run the Flask application:
    ```
    flask run
    ```

## Disclaimer

Since the quality of the compressed PDF files depends on various factors such as content and chosen settings, it's recommended to experiment with different settings to find the balance between file size reduction and acceptable quality.
