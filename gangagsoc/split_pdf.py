#!/usr/bin/env python3
import sys
import os
from pypdf import PdfReader, PdfWriter

def get_current_directory(cur_dir=None, pdf=None):
    if len(sys.argv) != 3:
        print(f"You must specify the current directory path and pdf file name as arguments.")
        sys.exit(1)

    current_dir = sys.argv[1] if not cur_dir else cur_dir
    pdf_file = sys.argv[2] if not pdf else pdf

    return current_dir, pdf_file

def split_pdf(file, cur_dir=None):
    if not cur_dir:
        current_dir, _ = get_current_directory()
    else:
        current_dir = cur_dir

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

        print(f"Extracted page {page_num+1} from {file} and saved as {filename}")

def execute_script():
    current_dir, pdf_file = get_current_directory()
    filepath = os.path.join(current_dir, pdf_file)
    split_pdf(filepath)


# Prevent autorun if script is being imported by test_InitialTask.py
if os.getenv("FROM_TEST_SCRIPT") == "true":
    RUN_INITIAL_TASK = False
else:
    RUN_INITIAL_TASK = True

if RUN_INITIAL_TASK or os.getenv("TEST_SCRIPT_OVERRIDE") == "true":
    execute_script()