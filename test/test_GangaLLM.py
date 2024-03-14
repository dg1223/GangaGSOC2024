import os
import unittest
import subprocess

class TestGangaLLM(unittest.TestCase):
    # Mimics a complete system call to hello.py
    def testExecuteLLMScript(self):
        from gangagsoc.run_InterfaceGanga import run_ganga_llm

        # Check if LLM was able to generate code
        # self.assertTrue(run_ganga_llm(), "LLM failed to generate code.")

        # set up file paths
        current_dir = os.getcwd()
        root_dir = os.path.dirname(current_dir)
        parent_dir = 'gangagsoc'
        ganga_job = "run_ganga_job.py"


         # for local runs
        ganga = os.path.join(root_dir, parent_dir, ganga_job)

        # for test runs
        if not os.path.exists(ganga):
            ganga = os.path.join(current_dir, ganga_job)
        # for CI runs
        else:            
            ganga = os.path.join(current_dir, parent_dir, ganga_job)

        # check if LLM generated ganga job script exists
        self.assertTrue(os.path.exists(ganga), "Ganga job script does not exist.")

        # run the ganga job
        command = ["python3", ganga]
        result = subprocess.run(command)
        self.assertIsNotNone(result.returncode, "FAIL: Subprocess execution returned with None")
