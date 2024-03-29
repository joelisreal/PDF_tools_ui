import subprocess
import sys
from pdf import input_paths

def compress_pdf_with_ghostscript(input_paths, output_paths):
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

# if __name__ == "__main__":
    # input_paths = sys.argv[1:]
print(input_paths)
output_paths = [f"output_{i}.pdf" for i in range(len(input_paths))]

for (input_path, output_path) in zip(input_paths, output_paths):
    compress_pdf_with_ghostscript(input_path, output_path)

# Example usage
# input_file = 'PSET 2.pdf'
# output_file = 'output_compressed_gs.pdf'
# compress_pdf_with_ghostscript(input_file, output_file)
