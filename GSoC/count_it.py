#!/usr/bin/env python3

import sys
import os
import re
from PyPDF2 import PdfReader
from collections import Counter

def get_current_directory():
    if len(sys.argv) != 2:
        print(f"You must specify the current directory path as an argument")
        sys.exit(1)

    current_dir = sys.argv[1]

    return current_dir

def preprocess_text(text):
    # replace square brackets used for citations
    square_brackets = r'\[|\]'
    
    # replace other non-alphanumeric character
    non_alpha_numeric = r'[^\w\s]|_'

    # replace brackets first, then the rest
    clean_text = re.sub(square_brackets, ' ', text.lower())    
    clean_text = re.sub(non_alpha_numeric, '', clean_text)

    return clean_text

'''
Perform lazy iteration on PDF file so that 
it doesn't load the entire file in memory
'''
def count_word(file, word):
    total_count = 0
    with open(file, 'rb') as pdf:
        reader = PdfReader(pdf)
        for page in reader.pages:
            text = page.extract_text()
            clean_text = preprocess_text(text)
            total_count += Counter(clean_text.split())[word]

    return total_count


if __name__ == '__main__':
    current_dir = get_current_directory()
    print("word count for 'it' in LHC.pdf: ", count_word(current_dir + '/LHC.pdf', "it"))
