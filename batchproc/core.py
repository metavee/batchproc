# adapted from http://blog.schettino72.net/posts/power-up-your-tools.html

import base64
import sys
import os.path
import tempfile
import time

from doit.loader import generate_tasks
from doit.doit_cmd import DoitMain
from doit.cmd_base import TaskLoader

class BatchProcessor(TaskLoader):
    """provide simple interface for programmatically creating pydoit tasks"""

    def __init__(self, args, fun, preprocessors=(), continue_on_error=True, log_filename='',
                 timestamp_fmt='%Y-%m-%d %H:%M:%S'):
        """set list of files to be processed
        @param args (list - str) file/folder path to apply fun
        @param fun (function) function to run on each file
        @param preprocessors (list - function) sequence of functions to modify args before tasks are generated
        @param continue_on_error (bool) if False, will quit after first error
        @param logfile (_io.TextIOWrapper) output stream or file handle where info is logged
        """

        if log_filename:
            log_file = open(log_filename, 'a')
        else:
            log_file = sys.stdout

        # get base64 string derived from processing function as filename
        # surprisingly inconvenient to get something python 3 compatible
        dep_filename = base64.b16encode(fun.__name__.encode()).decode()

        self.DOIT_CONFIG = {
            'verbosity': 2,  # 0 to capture stdout and stderr, 1 to only capture stdout, and 2 to not capture
            'continue': continue_on_error,
            # 'reporter': 'zero',  # 'zero', 'json', or don't define for the default
            'outfile': log_file,
            'dep_file': os.path.join(tempfile.gettempdir(), dep_filename),
            # 'num_process': 2
        }


        self.args = list(args)   # make a copy

        self.fun = fun

        for pp in preprocessors:
            self.args = pp(self.args)

        self.log_filename = log_filename
        self.log_file = log_file
        self.timestamp_fmt = timestamp_fmt

    def _gen_tasks(self):
        """generate doit tasks for each file"""
        for filename in self.args:
            path = os.path.abspath(filename)
            yield {
                'name': path,
                # 'file_dep': [path],
                'actions': [(self.fun, (filename,))],
            }

    def start(self):
        """Begin executing tasks."""

        if self.log_filename:
            print('Output will be logged to `%s`.' % self.log_filename)

        start_time = time.strftime(self.timestamp_fmt)
        print('Started %s' % start_time)

        if self.log_filename:
            orig_stdout = sys.stdout
            orig_stderr = sys.stderr

            sys.stdout = self.log_file
            sys.stderr = self.log_file

            print('Started %s' % start_time)

        doit_main = DoitMain(self)
        doit_main.run(['run'])

        stop_time = time.strftime(self.timestamp_fmt)

        if self.log_filename:
            print('Stopped %s' % stop_time)
            print()

            sys.stdout = orig_stdout
            sys.stderr = orig_stderr
            self.log_file.close()

        print('Stopped %s' % stop_time)


    def load_tasks(self, cmd, params, args):
        """implements loader interface, return (tasks, config)"""
        return generate_tasks('taskname that shows up in log', self._gen_tasks()), self.DOIT_CONFIG
