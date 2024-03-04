#!/usr/bin/env python3
import os

current_dir = os.getcwd()

# Create a bash script that will run the split_pdf script
open('run_initial_task.sh', 'w').write("""#!/bin/bash
current_dir="$1"
python3 "${current_dir}/split_pdf.py" "$current_dir"
""")

# make it executable
os.system('chmod +x run_initial_task.sh')

# run ganga job to split pdf
j = Job(name='split_pdf')
j.application = Executable()
j.application.exe = File('run_initial_task.sh')
j.application.args = [current_dir]

j.submit()