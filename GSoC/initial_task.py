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
    # split
    splitter_args = [ [current_dir, page_num, word] for page_num in range(number_of_pages)]
    j.splitter = ArgSplitter(args=splitter_args)

j.submit()


'''
Failsafe:
Store the final count to a different file and 
remove the earlier file so that re-running the job
does not use the count from a previously run job
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

    output_file = current_dir + '/' + job_name + '.txt'
    copy_file = current_dir + '/' + job_name + '_final.txt'

    if os.path.isfile(output_file):
        shutil.copy(output_file, copy_file)
        os.remove(output_file)
    else:
        print(f"The original file '{output_file}' does not exist.")
