import os
import sys
import unittest
import shutil
from fpdf import FPDF

os.environ["FROM_TEST_SCRIPT"] = "true"

wrapper_script = 'run_initial_task.sh'
split_pdf_script = 'split_pdf.py'


class TestSplitPDF(unittest.TestCase):
    def setUp(self):
        from gangagsoc import initial_task
        from gangagsoc import split_pdf

    def testGetCurrentDirectory(self):
        from gangagsoc.split_pdf import get_current_directory

        # simulate call to split_pdf.py through run_intial_task.sh from initial_task.py
        sys.argv = ["split_pdf.py", "current_dir", "pdf_file"]
        self.assertEqual(get_current_directory(), ("current_dir", "pdf_file"))

    def create_pdf_with_numbers(self):
        pdf_file = 'test_pdf.pdf'
        pdf_writer = FPDF()

        # Add blank pages and write their page numbers inside
        for i in range(3):
            pdf_writer.add_page()
            pdf_writer.set_xy(0, 0)
            pdf_writer.set_font('Times')
            pdf_writer.cell(ln=0, align='L', w=0, txt=str(i+1), border=0)
        
        pdf_writer.output(pdf_file, 'F')

        return pdf_file

    def testSplitPdf(self):
        from gangagsoc.split_pdf import split_pdf

        # create a dummy PDF file to test
        pdf_file = self.create_pdf_with_numbers()

        # test pdf splitting
        split_pdf(pdf_file, os.getcwd())
        self.assertTrue(os.path.exists("extracted_pages/LHC_page_1.pdf"))
        self.assertTrue(os.path.exists("extracted_pages/LHC_page_2.pdf"))
        self.assertTrue(os.path.exists("extracted_pages/LHC_page_3.pdf"))

        # remove dummy files
        os.remove(pdf_file)
        shutil.rmtree('extracted_pages')
