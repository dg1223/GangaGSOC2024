import re
import time
import torch
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

    def parse_llm_output(self, llm_output):
        python_code_matches = re.findall(r'```python\s+(.*?)\s+```', llm_output, re.DOTALL)
        bash_code_matches = re.findall(r'```bash\s+(.*?)\s+```', llm_output, re.DOTALL)

        if len(python_code_matches) > 0:
            for idx, python_code in enumerate(python_code_matches):
                print(f"python code snippet #{idx+1}:\n{python_code}\n\n")
        else:
            print("\nNo Python code snippet could be parsed from LLM's output.\n")

        if len(bash_code_matches) > 0:
            for idx, bash_code in enumerate(bash_code_matches):
                print(f"bash code snippet:\n{bash_code}\n\n")
        else:
            print("\nNo Bash code snippet could be parsed from LLM's output.\n")


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
    output_file = llm.store_llm_output(output)
    content = llm.read_llm_output(output_file)
    llm.print_llm_output(content)
    print("\n\n")
    llm.parse_llm_output(content)
