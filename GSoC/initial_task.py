#!/usr/bin/env python3
import os
import shutil
import sys
import time
from PyPDF2 import PdfReader

if len(sys.argv) != 2:
    print(f"You must specify the Python file as an argument")
    sys.exit(1)

python_script = sys.argv[1]
current_dir = os.getcwd()

# Create a bash script that will run the specified Python script
with open('run_initial_task.sh', 'w') as script:
    if python_script == 'count_it.py':
        script.write(f"""#!/bin/bash
        python3 "{current_dir}/{python_script}" "$1" "$2" "$3"
        """)
    else:
        script.write(f"""#!/bin/bash
        python3 "{current_dir}/{python_script}" "{current_dir}"
        """)

# make it executable
os.system('chmod +x run_initial_task.sh')

# run ganga job
job_name = os.path.splitext(python_script)[0]

j = Job(name=job_name)
j.application = Executable()
j.application.exe = File('run_initial_task.sh')

# Create splitter for the word count job
if job_name == 'count_it':
    reader = PdfReader('LHC.pdf')
    number_of_pages = len(reader.pages)
    word = 'it'

    # split using ArgSplitter
    splitter_args = [ [current_dir, page_num, word] for page_num in range(number_of_pages)]
    j.splitter = ArgSplitter(args=splitter_args)

    # merge using TextMerger
    j.postprocessors.append(TextMerger(files=['stdout']))

j.submit()



'''
Store result:
1. Wait (1 min) until job finishes with 'completed' status.
2. Extract the word counts from the merged file, calculate
the total word count and store it to a file
'''
if job_name == 'count_it':
    start_time = time.time()
    timeout = 60 # 1 minute

    while j.status != 'completed':
        # timeout if job is still running, probably an issue
        if time.time() - start_time > timeout:
            print("Timeout reached. Not waiting anymore for job completion")
            break

        continue

    output_file = j.outputdir + 'stdout'
    with open(output_file, 'r') as f:
        lines = f.readlines()
    
    result = 0
    for line in lines:
        # Check if the line does not start with '#'
        if not line.startswith('#'):
            try:
                result += int(line.strip())
            except ValueError:
                continue

    result_file = current_dir + '/' + job_name + '.txt'
    with open(result_file, 'w') as f:
        f.write(str(result))

    print(f"Word count has been stored in the same directory as this script: {result_file}")
    print(f"\nRun this command to see the result: cat {result_file}")
