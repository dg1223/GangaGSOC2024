#!/usr/bin/env python3
import sys
import os
from pypdf import PdfReader, PdfWriter

def get_current_directory():
    if len(sys.argv) != 3:
        print(f"You must specify the current directory path and pdf file name as arguments.")
        sys.exit(1)

    current_dir = sys.argv[1]
    pdf_file = sys.argv[2]

    return current_dir, pdf_file

def split_pdf(file):
    current_dir, _ = get_current_directory()
    output_folder = os.path.join(current_dir, 'extracted_pages')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    reader = PdfReader(file)
    pages = reader.pages

    for page_num, page in enumerate(pages):
        filename = os.path.join(output_folder, f"LHC_page_{page_num+1}.pdf")

        with open(filename, 'wb') as output_file:
            writer = PdfWriter()
            writer.add_page(page)
            writer.write(output_file)

        print(f"Extracted page {page_num+1} from {pdf_file} and saved as {filename}")


if __name__ == '__main__':
    current_dir, pdf_file = get_current_directory()
    filepath = os.path.join(current_dir, pdf_file)
    split_pdf(filepath)
