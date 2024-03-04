#!/usr/bin/env python3

import sys
import os
from PyPDF2 import PdfReader, PdfWriter

def get_current_directory():
    if len(sys.argv) != 2:
        print(f"You must specify the current directory path as an argument")
        return

    current_dir = sys.argv[1]

    return current_dir

def split_pdf(file):
    current_dir = get_current_directory()
    output_folder = current_dir + '/extracted_pages'

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

        print(f"Extracted page {page_num+1} from LHC.pdf and saved as {filename}")


if __name__ == '__main__':
    current_dir = get_current_directory()
    split_pdf(current_dir + '/LHC.pdf')
