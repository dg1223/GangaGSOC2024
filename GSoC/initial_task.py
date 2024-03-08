#!/usr/bin/env python3
import os
import shutil
import sys
import time
from PyPDF2 import PdfReader
from tqdm import tqdm

# globals
call_script = 'run_initial_task.sh'
word_counting_script = 'count_it.py'
pdf_file = 'LHC.pdf'
current_dir = os.getcwd()


def create_call_script():
    if len(sys.argv) != 2:
        print(f"You must specify the Python file as an argument")
        sys.exit(1)

    python_script = sys.argv[1]    

    # Create a bash script that will run the specified Python script
    with open(call_script, 'w') as script:
        if python_script == word_counting_script:
            script.write(f"""#!/bin/bash
            python3 "{current_dir}/{python_script}" "$1" "$2" "$3" {pdf_file}
            """)
        else:
            script.write(f"""#!/bin/bash
            python3 "{current_dir}/{python_script}" "{current_dir}"
            """)

    # make it executable
    os.system(f"chmod +x {call_script}")

    return python_script

def check_file_existence(filepath):    
    if not os.path.exists(filepath):
        print(f"\nThe file '{filepath}' does not exist.")
        print("Please store the file in the current directory and rerun the job.\n")
        sys.exit(1)

def submit_ganga_job(python_script):
    job_name = os.path.splitext(python_script)[0]

    j = Job(name=job_name)
    j.application = Executable()
    j.application.exe = File(call_script)

    # Create splitter for the word count job
    if python_script == word_counting_script:
        input_pdf = os.path.join(current_dir, pdf_file)
        check_file_existence(input_pdf)
        reader = PdfReader(input_pdf)
        number_of_pages = len(reader.pages)
        word = 'it'

        # split using ArgSplitter
        splitter_args = [ [current_dir, page_num, word] for page_num in range(number_of_pages)]
        j.splitter = ArgSplitter(args=splitter_args)

        # merge using TextMerger
        j.postprocessors.append(TextMerger(files=['stdout']))

    j.submit()

    return j, job_name

def count_frequency(output_file):
    with open(output_file, 'r') as f:
        lines = f.readlines()

    word_count = 0
    for line in lines:
        # Check if the line does not start with '#'
        if not line.startswith('#'):
            try:
                word_count += int(line.strip())
            except ValueError:
                continue

    return word_count

def store_word_count(job, job_name):
    '''
    1. Wait (2 mins) until job finishes with 'completed' status.
    2. Extract the word counts from the merged file, calculate
    the total word count and store it to a file
    '''
    start_time = time.time()
    timeout = 120 # 2 minutes

    print("\nWaiting for job to finish. Maximum wait time: 2 minutes\n")

    with tqdm(total = timeout, \
        leave=False, \
        bar_format='{elapsed}') as progress_bar:
        while job.status != 'completed':
            # update progress bar
            elapsed_time = time.time() - start_time
            progress_bar.update(elapsed_time - progress_bar.n)

            # timeout if job is still running, there's probably an issue
            if elapsed_time > timeout:
                print("Timeout reached. Cannot print results. Exiting job...")
                return

            time.sleep(1)

    merged_output = job.outputdir + 'stdout'
    
    word_count = count_frequency(merged_output)

    result_file = current_dir + '/' + job_name + '.txt'
    with open(result_file, 'w') as f:
        f.write(str(word_count))

    print(f"Frequency of the word 'it' = {word_count}\n")
    print(f"The word count has been stored in the same directory as this script: {result_file}")
    print(f"\nRun this command to see the stored result: cat {result_file}")


# Run script
script = create_call_script()
job, job_name = submit_ganga_job(script)

if script == word_counting_script:
    store_word_count(job, job_name)
