import os
import random
import shutil
import sys
import tempfile
from unittest import TestCase

import batchproc

class TestBatchProcessor(TestCase):

    # processing function which does nothing
    def fun(filename):
        return True

    def setUp(self):
        self.testdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.testdir)

    def test_log_filename(self):
        # test whether things are properly logged in file

        # process a random number of elements, and check log contents
        args = [str(i) for i in range(random.randint(5, 100))]
        log_filename = os.path.join(self.testdir, 'test.log')

        processor = batchproc.BatchProcessor(args, self.fun, log_filename=log_filename)
        processor.start()

        # read log
        with open(log_filename, 'r') as fd:
            lines = fd.readlines()

        os.unlink(log_filename)

        # count number of files processed, marked with a . at the start
        count = 0
        print (lines)
        for line in lines:
            if line.startswith('.'):
                count += 1

        self.assertEqual(len(args), count)

    def test_continue_on_error(self):
        # test both variations of the flag

        def always_fail(filename):
            return False

        args = ['a', 'b', 'c', 'd']
        log_filename = os.path.join(self.testdir, 'test.log')

        # make two runs, one continuing after errors, and the other stopping after the first
        # use the same logfile so that results are both in there
        processor = batchproc.BatchProcessor(args, always_fail, log_filename=log_filename, continue_on_error=True)
        processor.start()
        processor = batchproc.BatchProcessor(args, always_fail, log_filename=log_filename, continue_on_error=False)
        processor.start()

        # read log
        with open(log_filename, 'r') as fd:
            lines = fd.readlines()
        os.unlink(log_filename)

        # count number of files processed, marked with a . at the start
        count = 0
        print (lines)
        for line in lines:
            if line.startswith('.'):
                count += 1

        # log should contain 1 from the run that stopped after errors, and all from the other run
        self.assertEqual(len(args) + 1, count)

    def test_preprocessors(self):
        # test that the preprocessor filters get applied in the correct order

        # make some preprocessor functions where the order matters

        # filter files with a short filename
        def filter_short(files):
            return [f for f in files if len(f) >= 4]

        # make filenames longer
        def add_length(files):
            return [f + '1234' for f in files]

        args = ['a', 'bcde', 'f']
        log_filename = os.path.join(self.testdir, 'test.log')

        pre1 = (filter_short, add_length)
        pre2 = (add_length, filter_short)

        # make two runs, one for each order of preprocessors
        # use the same logfile so that results are both in there
        processor = batchproc.BatchProcessor(args, self.fun, pre1, log_filename=log_filename)
        processor.start()
        processor = batchproc.BatchProcessor(args, self.fun, pre2, log_filename=log_filename)
        processor.start()

        # read log
        with open(log_filename, 'r') as fd:
            lines = fd.readlines()
        os.unlink(log_filename)

        # count number of files processed, marked with a . at the start
        count = 0
        print (lines)
        for line in lines:
            if line.startswith('.'):
                count += 1

        # log should contain 1 from the run with pre1, and 3 from the other
        self.assertEqual(4, count)

    def test_basic_functionality(self):
        # test that the simplest use-case works

        # test function that adds some characters to the end of a file
        def append_zzz(filename):
            with open(filename, 'a') as fd:
                fd.write('zzz')

        # create some files to test it on, containing only their own filename
        filenames = [os.path.join(self.testdir, 'a.txt'), os.path.join(self.testdir, 'b.txt')]
        for file in filenames:
            with open(file, 'w') as fd:
                fd.write(file)

        processor = batchproc.BatchProcessor(filenames, append_zzz)
        processor.start()

        # read contents of files into result
        result = []
        for file in filenames:
            with open(file, 'r') as fd:
                result.append(fd.read())

        expected_result = [file + 'zzz' for file in filenames]

        for file in filenames:
            os.unlink(file)

        self.assertEqual(result, expected_result)

    def test_lambda(self):
        # test that it works when fun is a lambda
        args = ['test']
        lamfun = lambda filename: True
        processor = batchproc.BatchProcessor(args, lamfun)
        processor.start()

        # passes test if no errors are raised
        return

    def test_log_io_error(self):
        # make sure an exception occurs if the logfile can't be opened
        args = []

        # specify a directory as the logfile to deliberately cause an error
        self.assertRaises(Exception, batchproc.BatchProcessor, args, self.fun, log_filename='.')

        # specify an invalid filename - easy to do on windows, hard to do on linux
        if "win" in sys.platform:
            self.assertRaises(Exception, batchproc.BatchProcessor, args, self.fun, log_filename='"')


    def test_empty_list(self):
        # see what happens if the list of files is empty
        args = []

        processor = batchproc.BatchProcessor(args, self.fun)
        processor.start()

        # passes test if no errors are raised
        return

