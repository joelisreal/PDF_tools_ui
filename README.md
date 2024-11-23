# PDF Tools UI

Welcome to the PDF Tools UI! This project aims to provide a user-friendly interface for performing various operations on PDF files, starting with compression.

## Compress PDF Files

Currently, the only functionality available is **PDF compression**. This compression is performed using **Ghostscript**, specifically its `pdfwrite` device. It's important to note that Ghostscript's `pdfwrite` device doesn't always 'compress' files in the traditional sense. While it often results in smaller file sizes, the process involves various settings that may trade quality for file size. 

### Understanding Compression Settings

Ghostscript provides a range of options, known as `PDFSETTINGS`, which control the compression process. These settings cover a multitude of different controls, including downsampling images to reduce quality and file size. It's crucial to understand the implications of these settings and how they affect the output PDF file.

Each control within the `PDFSETTINGS` groups is individually available for fine-tuning. These controls are documented [here](https://ghostscript.readthedocs.io/en/latest/VectorDevices.html). 



### Usage Instructions

To run the web application, follow these steps:

1. **Install Python 3**:
   If you don't have Python 3 installed, download and install it from the official Python website: [python.org](https://www.python.org/downloads/).

2. **Clone the repository**:
   Clone the project repository to your local machine.

3. **Navigate to the project directory**:
   Open a terminal or command prompt and go to the project folder.

4. **Install dependencies**:
   Install **Flask** and **Flask-SQLAlchemy** by running the following command in your terminal:
   ```bash
   pip3 install Flask Flask-SQLAlchemy
   ```
   This assumes that you already have **Python 3** and **pip3** (the Python package manager) installed. If you're unsure whether `pip3` is installed, you can check by running:
   ```bash
   pip3 --version
   ```

5. **Install Ghostscript**:
   Download and install **Ghostscript** from the official site.

   In the `static/assets/py/compress_pdf_ghostscript.py` file, you’ll find a variable `gs_command` that defines the Ghostscript executable. The default value for the first entry is set to `gswin64c` (for Windows). For Unix-based systems, you’ll need to update this to `gs`.

   Here are the recommended executable names for different operating systems:
   
   - **Unix**: `gs`
   - **VMS**: `gs`
   - **Windows**: 
     - `gswin32.exe`
     - `gswin32c.exe`
     - `gswin64.exe`
     - `gswin64c.exe`
   - **OS/2**: `gsos2`

6. **Set the Flask app**:
   Depending on your operating system and shell, you’ll need to set the `FLASK_APP` environment variable differently.

   - **For Bash (Unix-based systems)**, use:
     ```bash
     export FLASK_APP=pdf_calls.py
     ```

   - **For PowerShell (Windows)**, use:
     ```powershell
     $env:FLASK_APP="pdf_calls.py"
     ```

   - **For Command Prompt (Windows)**, use:
     ```cmd
     set FLASK_APP=pdf_calls.py
     ```

   - **Fish shell (Unix-based systems):
     ```fish
     set -x FLASK-APP=pdf_calls.py
     ```


7. **Run the Flask application**:
   Start the Flask server with the following command:
   ```bash
   flask run
   ```




## Disclaimer

Since the quality of the compressed PDF files depends on various factors such as content and chosen settings, it's recommended to experiment with different settings to find the balance between file size reduction and acceptable quality.
