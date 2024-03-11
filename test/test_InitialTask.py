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
        from gangagsoc import hello
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

    def testCreateAndRemoveGangaJob(self):
        # simple test to see if ganga is working
        from ganga.ganga import ganga
        from ganga import Job
        

        j = Job()
        j.submit()
        self.assertTrue(sleep_until_completed(j, 60), 'Timeout on completing job')
        self.assertEqual(j.status, 'completed')
        j.remove()

    def testSubmitGangaJob(self):
        from ganga.ganga import ganga
        from ganga import Local
        from gangagsoc.initial_task import submit_ganga_job
        from ganga.GangaTest.Framework.utils import sleep_until_completed

        # get script into test directory for testing
        current_dir = os.getcwd()
        root_dir = os.path.dirname(current_dir)
        parent_dir = 'gangagsoc'
        filepath = os.path.join(root_dir, parent_dir, word_counting_script)

        src = '/home/runner/work/GangaGSoC2024/gangagsoc/count_it.py'
        current = '/home/runner/work/GangaGSoC2024/test'
        root = '/home/runner/work/GangaGSoC2024'
        parent = 'gangagsoc'

        shutil.copy(current_dir, root_dir)

        j, job_name = submit_ganga_job(word_counting_script)

        self.assertEqual(j.name, job_name)
        self.assertEqual(j.backend.__class__, Local)
        self.assertIsNotNone(j.application)
        self.assertIsNotNone(j.splitter)
        self.assertEqual(len(j.postprocessors), 1)
        self.assertEqual(len(j.subjobs), 29)

        sleep_until_completed(j)
        self.assertEqual(j.status, 'completed')
        
        j.remove()

        # remove main scripts after testing
        os.remove('run_initial_task.sh')
        os.remove(word_counting_script)

    def testCountFrequency(self):
        from gangagsoc.initial_task import count_frequency

        output_file = "test_output.txt"
        with open(output_file, "w") as f:
            f.write("1\n2\n3\n")

        self.assertEqual(count_frequency(output_file), 6)

        os.remove('test_output.txt')

    # def testStoreWordCount(self):
    #     from gangagsoc.initial_task import store_word_count

    #     job_name = "test_job"
    #     j = Job(name=job_name)
        
    #     store_word_count(j, job_name)

    #     self.assertTrue(os.path.exists(job_name + ".txt"))
    #     j.remove()
