#!/usr/bin/env python3

import sys
import os
import re
from PyPDF2 import PdfReader
from collections import Counter

def get_arguments():
    if len(sys.argv) != 4:
        print(f"You must specify all 3 parameters as arguments.\
            parameters are: current directory, page number, word")
        sys.exit(1)
    
    current_dir = sys.argv[1]
    page_num = sys.argv[2]
    word = sys.argv[3]

    return current_dir, page_num, word

def preprocess_text(text):
    # replace square brackets used for citations
    square_brackets = r'\[|\]'
    
    # replace other non-alphanumeric character
    non_alpha_numeric = r'[^\w\s]|_'

    # replace brackets first, then the rest
    clean_text = re.sub(square_brackets, ' ', text.lower())    
    clean_text = re.sub(non_alpha_numeric, '', clean_text)

    return clean_text

def count_word(file, page_num, word):
    # total_count = 0
    with open(file, 'rb') as pdf:
        reader = PdfReader(pdf)
        # for page in reader.pages:
        text = reader.pages[int(page_num)].extract_text()
        clean_text = preprocess_text(text)
        # total_count += Counter(clean_text.split())[word]
        return Counter(clean_text.split())[word]

    # return total_count


if __name__ == '__main__':
    current_dir, page_num, word = get_arguments()
    print(f"word count for '{word}' in page {page_num} of LHC.pdf: \
        {count_word(current_dir + '/LHC.pdf', page_num, word)}")
