import re
import sys
import time
import torch
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM

class InterfaceGanga:
    def __init__(self, llm_model="deepseek-ai/deepseek-coder-1.3b-instruct",\
                       llm_input="Find approximation of Pi using Monte Carlo",\
                       return_tensor_format='pt'):

        self.llm_model = llm_model
        self.llm_input = llm_input
        self.return_tensor_format = return_tensor_format

    def run_llm(self):
        tokenizer = AutoTokenizer.from_pretrained(self.llm_model,\
            trust_remote_code=True)

        model = AutoModelForCausalLM.from_pretrained(self.llm_model,\
            trust_remote_code=True, torch_dtype=torch.bfloat16)

        # Run on GPU if available
        if torch.cuda.is_available():
            print("\nFound CUDA compatible GPU. Utilizing GPU...\n\
Esimated runtime: < 1 minute\n")
            model = model.cuda()
        else:
            print("\nNo CUDA compatible GPU found. Running on CPU only...\n\
Esimated runtime: < 13-25 minutes\n")

        if not tokenizer.pad_token:
            tokenizer.pad_token = tokenizer.eos_token

        input_text = self.llm_input
        inputs = tokenizer(input_text,\
                return_tensors=self.return_tensor_format).to(model.device)

        start_time = time.time()

        # testing: Assert max_length >= input length
        outputs = model.generate(**inputs, max_length=1024)

        end_time = time.time()

        print("\nTime taken:", round((end_time - start_time) / 60.0, 2), "minutes\n")

        return tokenizer.decode(outputs[0], skip_special_tokens=True)

    ### THIS FUNCTION BLOCK IS AUXILLARY TO THE PROBLEM STATEMENT ###

    def store_llm_output(self, output):
        output_file = 'llm_output.txt'
        with open(output_file, 'w') as f:
            f.write(output)

        return output_file

    def read_llm_output(self, output_file): 
        with open(output_file, 'r') as f:
            llm_output = f.read()

        return llm_output

    def print_llm_output(self, llm_output):
        print(llm_output)

    ### THIS FUNCTION BLOCK IS AUXILLARY TO THE PROBLEM STATEMENT ###


    def extract_code_snippet(self, pattern_type, pattern_1, pattern_2, llm_output):
        total_tries_left = 2
        while total_tries_left > 0:
            if total_tries_left == 2:
                snippets = re.findall(pattern_1, llm_output, re.DOTALL)
            else:
                snippets = re.findall(pattern_2, llm_output, re.DOTALL)
                    
            snippet = self.helper_extract_code_snippet(snippets)

            if not snippet:
                total_tries_left -= 1
                if total_tries_left == 1:
                    print(f"\nWARNING: No code snippet for '{pattern_type}' was parsed \
using coding marker #1.\nLLM probably generated a different pattern of text.")
                    print("Trying a different coding marker to match pattern...")            
                    continue
                # No point running a Ganga job when there's no code to run
                elif pattern_type == 'Pi approximation' or pattern_type == 'Ganga job':
                    print("\nERROR: Unable to parse code from LLM's output. Exiting...\n")
                    sys.exit(1)
                else:
                    print("LLM generated incomplete code. Continuing...")
            else:
                print(f"\n'SUCCESS!! {pattern_type}' code found in LLM's output.")

            return snippet

    def helper_extract_code_snippet(self, snippets):
        snippet_size = np.shape(snippets)
        dimensions = len(snippet_size)
        # no dimension
        if not snippet_size or snippet_size[0] == 0:
            return None
        # one-dimensional
        elif dimensions == 1 and snippet_size[0] > 0:
            snippet = snippets[0]
        # two-dimensional
        else:
            snippet = snippets[0][0]

        return snippet

    def write_code_snippet_to_file(self, llm_output):
        '''
        These hardcoded patterns were developer after doing multiple simulation runs
        with the same prompt on the deepseeker model. However, the LLM's consistency
        cannot be guaranteed.
        '''
        pi_pattern_1 = r'python code snippet #1:(.*?)((?=\npython code snippet #2)|$)'
        ganga_pattern_1 = r'python code snippet #2:(.*?)((?=\nbash code snippet)|$)'
        bash_pattern_1 = r'bash code snippet:(.*?)((?=\npython code snippet)|$)'
        pi_pattern_2 = r"```python(.*?)```"
        ganga_pattern_2 = r"```python(\n[^`]*?from.*?)```"
        bash_pattern_2 = r"```bash(.*?)```"

        python_snippet = self.extract_code_snippet(\
            'Pi approximation', pi_pattern_1, pi_pattern_2, llm_output)
        print(python_snippet)
        ganga_snippet = self.extract_code_snippet(\
            'Ganga job', ganga_pattern_1, ganga_pattern_2, llm_output)
        print(ganga_snippet)
        bash_snippet = self.extract_code_snippet(\
            'Bash', bash_pattern_1, bash_pattern_2, llm_output)
        print(bash_snippet)

        # all code snippets should be ready by this point. #
        
        # Generate file names
        pi_function_name = re.findall(r'def\s+(\w+)\(', python_snippet, re.DOTALL)
        if pi_function_name:
            if len(pi_function_name) > 1:
                pi_filename = f"{pi_function_name[0]}.py"        
            else:
                pi_filename = f"{pi_function_name}.py"
        else:
            pi_filename = "pi_estimation.py"

        ganga_filename = "run_ganga_job.py"
        bash_filename = "run_ganga.sh"

        # Write code snippets to respective files
        self.helper_write_to_file(pi_filename, python_snippet)
        self.helper_write_to_file(ganga_filename, ganga_snippet)
        self.helper_write_to_file(bash_filename, bash_snippet)

    def helper_write_to_file(self, filename, snippet):
        with open(filename, 'w') as file:
            file.write(snippet.lstrip())


if __name__ == '__main__':
    prompt = "I want to use Ganga to calculate an approximation to the number \
    pi using an accept-reject simulation method with one million simulations. I \
    would like to perform this calculation through a Ganga job. The job should be \
    split into a number of subjobs that each do thousand simulations.The code \
    should be written in Python. \
    Here are some instructions that you can follow. \
    1. Write code to calculate the approximation of pi using the above-mentioned \
    method. \
    2. Write a bash script that will execute the code above. \
    3. Run a ganga job using local backend: j = Job(name=job_name, backend=Local()) \
    4. Run the Bash script as an Executable application: \
    j.application = Executable() \
    j.application.exe = File(the_script_to_run) \
    5. Use ArgSplitter to split the job: j.splitter = ArgSplitter(args=splitter_args) \
    It should split the job into a number of subjobs that each do thousand simulations. \
    6. Merge output from the splitter using TextMerger: \
    j.postprocessors.append(TextMerger(files=['stdout'])) \
    7. Run the ganga job: j.submit() \
    Do not give me code as IPython or Jupyter prompts. Give me the python script."

    llm = InterfaceGanga(llm_input=prompt)
    output = llm.run_llm()
    llm.write_code_snippet_to_file(output)
