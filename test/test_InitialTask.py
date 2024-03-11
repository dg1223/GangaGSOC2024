import os
import unittest
import shutil
from ganga.GangaTest.Framework.utils import sleep_until_completed

os.environ["FROM_TEST_SCRIPT"] = "true"

wrapper_script = 'run_initial_task.sh'
word_counting_script = 'count_it.py'
split_pdf_script = 'split_pdf.py'

class TestInitialTask(unittest.TestCase):
    def setUp(self):
        from gangagsoc import initial_task
        from gangagsoc import count_it
        from gangagsoc import split_pdf

    def testCreateCallScript(self):
        from gangagsoc.initial_task import create_call_script

        script = create_call_script(word_counting_script)

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

        script = create_call_script(word_counting_script)
        j, job_name = submit_ganga_job(script)

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
        print(os.path.join(root_dir, parent_dir, split_pdf_script))
        print(os.path.join(current_dir, parent_dir, split_pdf_script))

        script = create_call_script(split_pdf_script)
        j, job_name = submit_ganga_job(script)

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

    # def testStoreWordCount(self):
    #     from ganga.ganga import ganga
    #     from ganga import Job
    #     from gangagsoc.initial_task import store_word_count

    #     job_name = "test_job"
    #     j = Job(name=job_name)
        
    #     store_word_count(j, job_name)

    #     self.assertTrue(os.path.exists(job_name + ".txt"))
    #     j.remove()
