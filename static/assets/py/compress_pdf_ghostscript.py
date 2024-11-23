import subprocess
import sys

def compress_pdf_with_ghostscript(input_path, output_path):
    
    gs_command = [
        'gswin64c',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dPDFSETTINGS=/ebook',
        '-dNOPAUSE',
        '-dBATCH',
        f'-sOutputFile={output_path}',
        input_path
    ]

    try:
        subprocess.run(gs_command, check=True)
        print("PDF compression completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during PDF compression: {e}")

