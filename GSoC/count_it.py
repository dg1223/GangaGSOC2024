#!/usr/bin/env python3

import sys
import re
import os
import shutil
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
    with open(file, 'rb') as pdf:
        reader = PdfReader(pdf)
        text = reader.pages[int(page_num)].extract_text()
        clean_text = preprocess_text(text)

        return Counter(clean_text.split())[word]


if __name__ == '__main__':
    current_dir, page_num, word = get_arguments()
    count = (count_word(current_dir + '/LHC.pdf', page_num, word))

    # store counts from each page to a file
    output_file = os.path.join(current_dir, 'count_it.txt')
    
    if not os.path.exists(output_file):
        with open(output_file, 'w') as f:
            f.write(str(count))
    else:
        # get the current word count
        with open(output_file, 'r') as f:
            line = f.readline()
            try:
                previous_count = int(line.strip())
            except ValueError:
                print("The file does not contain a valid number.")

        # update word count
        with open(output_file, 'w') as f:
            f.write(str(previous_count + count))
