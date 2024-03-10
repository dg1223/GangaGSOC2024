#!/usr/bin/env python3
import sys
import re
import os
import shutil
from pypdf import PdfReader
from collections import Counter

def get_arguments():
    if len(sys.argv) != 5:
        print(f"You must specify all 4 parameters as arguments.\
            parameters are: current directory, page number, word, pdf file name")
        sys.exit(1)
    
    current_dir = sys.argv[1]
    page_num = sys.argv[2]
    word = sys.argv[3]
    pdf_file = sys.argv[4]

    return tuple(sys.argv[1:5])

def preprocess_text(text):
    # first, replace all square brackets used for citations
    square_brackets = r'\[|\]'
    
    # replace other non-alphanumeric character
    non_alpha_numeric = r'[^\w\s]|_'

    # replace brackets first, then the rest
    clean_text = re.sub(square_brackets, ' ', text.lower())    
    clean_text = re.sub(non_alpha_numeric, '', clean_text)

    return clean_text


def count_word(file, page_num, word):
    with open(file, 'rb') as pdf:
        reader = PdfReader(pdf)
        text = reader.pages[int(page_num)].extract_text()
        clean_text = preprocess_text(text)

        return Counter(clean_text.split())[word]

def execute_script():
    current_dir, page_num, word, pdf_file = get_arguments()
    input_pdf = os.path.join(current_dir, pdf_file)
    print((count_word(input_pdf, page_num, word)))


# Prevent autorun if script is being imported by test_InitialTask.py
if os.getenv("FROM_TEST_SCRIPT") == "true" or os.getenv("FROM_INIT") == "true":
    RUN_INITIAL_TASK = False
else:
    RUN_INITIAL_TASK = True

if RUN_INITIAL_TASK:
    execute_script()