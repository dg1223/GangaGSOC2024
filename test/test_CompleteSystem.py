import os
import unittest
import shutil
import subprocess
from ganga.GangaTest.Framework.utils import sleep_until_completed

os.environ["FROM_TEST_SCRIPT"] = "true"

wrapper_script = 'run_initial_task.sh'
word_counting_script = 'count_it.py'
split_pdf_script = 'split_pdf.py'

class TestInitialTask(unittest.TestCase):
    def testCreateCallScript(self):
        from gangagsoc.initial_task import create_call_script

        script, _ = create_call_script(word_counting_script)

        # check if wrapper bash script exists in current directory
        current_dir = os.getcwd()
        filepath = os.path.join(current_dir, word_counting_script)

        self.assertTrue(os.path.exists(wrapper_script))
        self.assertTrue(os.access(wrapper_script, os.X_OK))

    # simple test to see if ganga is working
    def testCreateAndRemoveGangaJob(self):
        from ganga.ganga import ganga
        from ganga import Job
        
        j = Job()
        j.submit()

        self.assertTrue(sleep_until_completed(j, 60), 'Timeout on completing job')
        self.assertEqual(j.status, 'completed')
        
        j.remove()

    def tryFileCopy(self, root, cur_dir, par_dir, script):
        try:
            # for local runs
            filepath = os.path.join(root, par_dir, script)
            shutil.copy(filepath, script)
        except:
            # for CI runs
            filepath = os.path.join(cur_dir, par_dir, script)
            shutil.copy(filepath, script)

    def testSubmitGangaJob_WordCounting(self):
        from ganga.ganga import ganga
        from ganga import Local
        from gangagsoc.initial_task import create_call_script
        from gangagsoc.initial_task import submit_ganga_job

        # get script into test directory for testing
        current_dir = os.getcwd()
        root_dir = os.path.dirname(current_dir)
        parent_dir = 'gangagsoc'

        self.tryFileCopy(root_dir, current_dir, parent_dir, word_counting_script)

        script, _ = create_call_script(word_counting_script)
        j, job_name = submit_ganga_job(script, current_dir)

        self.assertEqual(j.name, job_name)
        self.assertEqual(j.backend.__class__, Local)
        self.assertIsNotNone(j.application)
        self.assertIsNotNone(j.splitter)
        self.assertEqual(len(j.postprocessors), 1)

        # there should be a subjob for each page of LHC.pdf
        self.assertEqual(len(j.subjobs), 29)

        # wait for job completion
        sleep_until_completed(j)
        self.assertEqual(j.status, 'completed')
        
        j.remove()

        # remove main scripts after testing
        os.remove('run_initial_task.sh')
        os.remove(word_counting_script)

    def testSubmitGangaJob_SplitPDF(self):
        from ganga.ganga import ganga
        from ganga import Local
        from gangagsoc.initial_task import create_call_script
        from gangagsoc.initial_task import submit_ganga_job

        # get script into test directory for testing
        current_dir = os.getcwd()
        root_dir = os.path.dirname(current_dir)
        parent_dir = 'gangagsoc'

        self.tryFileCopy(root_dir, current_dir, parent_dir, split_pdf_script)

        script, _ = create_call_script(split_pdf_script)
        j, job_name = submit_ganga_job(script, current_dir)

        self.assertEqual(j.name, job_name)
        self.assertEqual(j.backend.__class__, Local)
        self.assertIsNotNone(j.application)

        # wait for job completion
        sleep_until_completed(j)
        self.assertEqual(j.status, 'completed')
        
        j.remove()

        # remove main scripts after testing
        os.remove('run_initial_task.sh')
        os.remove(split_pdf_script)

    def testCountFrequency(self):
        from gangagsoc.initial_task import count_frequency

        output_file = "test_output.txt"
        with open(output_file, "w") as f:
            f.write("1\n2\n3\n")

        self.assertEqual(count_frequency(output_file), 6)

        os.remove('test_output.txt')

    def testStoreWordCount(self):
        from ganga.ganga import ganga
        from ganga import Job, Local
        from gangagsoc.initial_task import store_word_count

        current_dir = os.getcwd()
        job_name = "test_store_word_count"
        j = Job(name=job_name, backend=Local())
        j.submit()
        sleep_until_completed(j)

        output_file = os.path.join(j.outputdir, 'stdout')

        # mimic merged output; overwrite default stdout
        with open(output_file, "w") as f:
            f.write("#sometext\n1\n2\n3\n#sometest\n")
        
        store_word_count(j, job_name, current_dir)

        result_file = job_name + '.txt'
        self.assertTrue(os.path.exists(result_file))

        with open(result_file, 'r') as f:
            count = f.read().strip(' \n')
        self.assertEqual(count, '6')

        j.remove()
        os.remove(result_file)

'''
These are complete system calls to count_it.py and split_pdf.py
through the calling script initial_task.py
'''
class TestSystem(unittest.TestCase):
    # set up file paths to make system calls
    def setupPath(self, main_script, output):
        current_dir = os.getcwd()
        root_dir = os.path.dirname(current_dir)
        parent_dir = 'gangagsoc'
        wrapper_script = "initial_task.py"

        # for local runs
        wrapper_path = os.path.join(root_dir, parent_dir, wrapper_script)
        main_path = os.path.join(root_dir, parent_dir, main_script)
        result = os.path.join(root_dir, parent_dir, output)

        # for CI runs
        if not os.path.exists(wrapper_path) and \
            not os.path.exists(main_path):
            wrapper_path = os.path.join(current_dir, parent_dir, wrapper_script)
            main_path = os.path.join(current_dir, parent_dir, main_script)
            result = os.path.join(current_dir, parent_dir, output)

        return wrapper_path, main_path, result

    # Mimic a complete system test of count_it.py
    def testCountIt(self):
        wrapper, main, result = self.setupPath(word_counting_script, 'count_it.txt')
        
        os.environ["TEST_SCRIPT_OVERRIDE"] = "true"
        command = ["python3", wrapper, main]
        subprocess.run(command)

        self.assertTrue(os.path.exists(result))

        with open(result, 'r') as f:
            count = f.read().strip(' \n')
        self.assertEqual(count, '30')

        os.remove(result)
        os.environ["TEST_SCRIPT_OVERRIDE"] = "true"

    # Mimic a complete system test of split_pdf.py
    def testSplitPDF(self):
        wrapper, main, result = self.setupPath(split_pdf_script, 'extracted_pages')
        
        os.environ["TEST_SCRIPT_OVERRIDE"] = "true"
        command = ["python3", wrapper, main]
        subprocess.run(command)

        self.assertTrue(os.path.exists(result))

        # check if directory has 29 files
        files = os.listdir(result)
        number_of_files = len(files)
        self.assertEqual(number_of_files, 29)

        # check if some filenames match with expected names
        self.assertTrue(os.path.exists(os.path.join(result, 'LHC_page_1.pdf')))
        self.assertTrue(os.path.exists(os.path.join(result, 'LHC_page_17.pdf')))
        self.assertTrue(os.path.exists(os.path.join(result, 'LHC_page_29.pdf')))

        shutil.rmtree(result)
        os.environ["TEST_SCRIPT_OVERRIDE"] = "false"
