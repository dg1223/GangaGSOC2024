# from ganga.GangaTest.Framework.utils import sleep_until_completed, file_contains
from ganga.ganga import ganga
from ganga import Job, Local
import os
import unittest
import shutil

os.environ["FROM_TEST_SCRIPT"] = "true"

# No need to do setUp and tearDown if you are
# inheriting from the GangaUnitTest class
class TestInitialTask(unittest.TestCase):
    # def setUp(self):
    #     # Create a directory to mimic the structure and avoid file conflicts
    #     os.mkdir("initial_task_test")
    #     os.chdir("initial_task_test")

    #     # Copy LHC.pdf into the dummy directory
    #     shutil.copyfile('../LHC.pdf', 'LHC.pdf')


    # def tearDown(self):
    #     os.remove('../run_initial_task.sh')

    def testCreateCallScript(self):
        from gangagsoc.initial_task import create_call_script        

        script = create_call_script()

        self.assertTrue(os.path.exists(script))
        self.assertTrue(os.access(script, os.X_OK))

    def testCreateAndRemoveGangaJob(self):
        # simple test to see if ganga is working
        j = Job()
        j.remove()

    def testSubmitGangaJob(self):
        from gangagsoc.initial_task import submit_ganga_job

        j, job_name = submit_ganga_job("count_it.py")

        self.assertEqual(j.name, job_name)
        self.assertEqual(j.backend.__class__, Local)
        self.assertIsNotNone(j.application)
        self.assertIsNotNone(j.splitter)
        self.assertEqual(len(j.postprocessors), 1)

        # remove the intermediate call script after testing
        os.remove('run_initial_task.sh')

    # def testCountFrequency(self):
    #     from initial_task import count_frequency

    #     output_file = "test_output.txt"
    #     with open(output_file, "w") as f:
    #         f.write("1\n2\n3\n")

    #     self.assertEqual(count_frequency(output_file), 6)

    # def testStoreWordCount(self):
    #     from initial_task import store_word_count
    #     from GangaCore.GPI import Job

    #     j = Job()
    #     j.outputdir = "test_output/"
    #     job_name = "test_job"
    #     store_word_count(j, job_name)

    #     self.assertTrue(os.path.exists(job_name + ".txt"))
