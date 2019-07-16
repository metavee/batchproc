import io
import os
import shutil
import sys
import tempfile
from unittest import TestCase

import batchproc

class TestUtil(TestCase):

    def setUp(self):
        self.testdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.testdir)

    def test_expand_folder(self):
        '''Test that the basic functionality of expand_folder works.'''

        f1_path = os.path.join(self.testdir, 'f1')
        d1_path = os.path.join(self.testdir, 'd1')
        f2_path = os.path.join(d1_path, 'f2')
        d2_path = os.path.join(d1_path, 'd2')
        f3_path = os.path.join(d2_path, 'f3')
        d3_path = os.path.join(d2_path, 'd3')

        # make a nested directory structure
        os.makedirs(d3_path)

        # make some files
        with open(f1_path, 'w') as f1, open(f2_path, 'w') as f2, open(f3_path, 'w') as f3:
            pass

        file_list = [self.testdir]
        original_file_list = file_list[:]
        result = batchproc.expand_folder(file_list)
        expected_result = [f1_path, f2_path, f3_path]

        # cleanup
        shutil.rmtree(d1_path)
        os.remove(f1_path)

        # check that we get the right answer
        self.assertEqual(result, expected_result)

        # check that our original list isn't modified
        self.assertEqual(file_list, original_file_list)

    def test_expand_folder_symlink(self):
        # test that symlinks pointing to their own parent directory do not cause infinite loops

        if "win" in sys.platform:
            self.skipTest('Symbolic links cannot be tested on Windows, since making them requires admin rights.')

        d1_path = os.path.join(self.testdir, 'd1')
        f1_path = os.path.join(self.testdir, 'f1')

        os.makedirs(d1_path)

        # make symlink pointing to parent of d1, inside d1
        os.symlink(self.testdir, os.path.join(d1_path, 'link'))

        # make a file
        with open(f1_path, 'w') as f1:
            pass

        file_list = [self.testdir]
        result = batchproc.expand_folder(file_list)
        expected_result = [f1_path]

        shutil.rmtree(d1_path)
        os.remove(f1_path)

        self.assertEqual(result, expected_result)

    def test_get_file_list_stdin(self):
        # test that stdin parsing works, particularly that it handles filenames with spaces properly

        # make up some fake filenames
        f1 = os.path.join(self.testdir, 'a filename with spaces')
        f2 = os.path.join(self.testdir, 'another filename with spaces')
        f3 = os.path.join(self.testdir, 'a_filename_without_spaces')
        files = [
            "'%s'" % f1,
            '"%s"' % f2,
            f3
        ]

        # make virtual stdin stream
        old_stdin = sys.stdin
        sys.stdin = io.StringIO(u' '.join(files))

        # make sure sys.argv only has one item so that get_file_list reads from stdin
        old_args = sys.argv
        sys.argv = sys.argv[0:1]

        result = batchproc.get_file_list()
        expected_result = list(map(os.path.abspath, [f1,f2,f3]))

        # restore stdin stream and sys.argv
        sys.stdin = old_stdin
        sys.argv = old_args

        self.assertEqual(result, expected_result)

    def test_get_file_list_args(self):
        # test that it correctly returns a slice from sys.argv

        # temporarily replace sys.argv with our own bogus list
        old_args = sys.argv

        sys.argv = [sys.argv[0], '1', '2', '3']
        result = batchproc.get_file_list()
        expected_result = ['1', '2', '3']

        sys.argv = old_args

        for r, e in zip(result, expected_result):
            self.assertEqual(os.path.abspath(r), os.path.abspath(e))