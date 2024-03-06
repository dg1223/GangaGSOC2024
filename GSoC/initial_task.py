#!/usr/bin/env python3
import os
import sys
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

# Create splitter and merger for the word count job
if job_name == 'count_it':
    reader = PdfReader('LHC.pdf')
    number_of_pages = len(reader.pages)
    word = 'it'
    splitter_args = [ [current_dir, page_num, word] for page_num in range(number_of_pages)]
    j.splitter = ArgSplitter(args=splitter_args)

j.submit()