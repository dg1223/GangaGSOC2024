# Clone repository and activate ganga

## Clone repository

```bash
git clone https://github.com/dg1223/GangaGSoC2024.git
cd GangaGSoC2024
```

## Activate ganga prompt

- Go to the GSoC virtual environment:
    
    ```bash
    cd GSoC
    ```
    
- Activate ganga:
    
    ```bash
    ./bin/ganga
    ```
    

# Initial task

## Subtask 1

> Demonstrate that you can run a simple `Hello World` Ganga job that executes on a `Local` backend.
> 
- In the ganga prompt, execute the following commands:

```python
j = Job(name='hello')
j.submit()
```

The output should show:

```python
Hello World
[path_to_job_output_in_local_machine]/stdout (END)
```

Press `q` to get back to ganga prompt.

## Subtask 2

> Create a job in Ganga that demonstrates splitting a job into multiple pieces and then collates the results at the end.
> 
> - Use the included file `LHC.pdf`.
> - Create a job in Ganga that in python (or through using system calls) split the pdf file into individual pages.

- In the ganga prompt, execute:
    
    ```python
    runfile('initial_task.py').
    ```
    
- As soon as the job starts running you should be able to see a bash script `run_initial_task.sh` and a folder `extracted_pages` in the same directory.
- The `extracted_pages` folder is expected to contain 29 PDF files titled `LHC_page_[page_number].pdf`. Each file corresponds to a page from `LHC.pdf`.
- To check the `stdout` of the job:
    - execute:
        
        ```python
        jobs
        ```
        
    - It should show you the job IDs of all jobs that currently exist in your ganga repository. The last job ID is the one that we need to note. It should have a `completed` status.
    - Now execute:
        
        ```python
        jobs(job_ID).peek('stdout')
        ```
        
    - You should see several lines (29 lines to be precise) saying:
        
        ```python
        Extracted page 1 from LHC.pdf and saved as your_path_to_GSoC_virtual_environment/extracted_pages/LHC_page_1.pdf
        ...
        Extracted page 29 from LHC.pdf and saved as your_path_to_GSoC_virtual_environment/extracted_pages/LHC_page_29.pdf
        ```