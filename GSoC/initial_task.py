#!/usr/bin/env python3
import os
import sys

if len(sys.argv) != 2:
    print(f"You must specify the Python file to run as an argument")
    sys.exit(1)

python_script = sys.argv[1]
current_dir = os.getcwd()

# Create a bash script that will run the specified Python script
with open('run_initial_task.sh', 'w') as script:
    script.write(f"""#!/bin/bash
current_dir="$1"
python3 "${{current_dir}}/{python_script}" "$current_dir"
""")

# make it executable
os.system('chmod +x run_initial_task.sh')

# run ganga job
job_name = os.path.splitext(python_script)[0]
j = Job(name=job_name)
j.application = Executable()
j.application.exe = File('run_initial_task.sh')
j.application.args = [current_dir]

j.submit()