# redefine raw_input if using Python 2.x
try:
   input = raw_input
except NameError:
   pass

import os
import shlex
import sys

def expand_folder(files):
    """Return a clone of file list files where all directories are recursively replaced with their contents."""
    expfiles = []
    for file in files:
        if os.path.isdir(file):
            for dirpath, dirnames, filenames in os.walk(file):
                for filename in filenames:
                    expfiles.append(os.path.join(dirpath, filename))
        else:
            expfiles.append(file)

    for path in expfiles:
        if not os.path.exists(path):
            sys.stderr.write('%s: No such file or directory\n' % path)

    return expfiles


def get_file_list():
    """Return a list of strings corresponding to file names supplied by drag and drop or standard input."""

    if len(sys.argv) > 1:
        file_list = list(sys.argv[1:])  # make copy
    else:
        files_str = input('Select the files you want to process and drag and drop them onto this window, '
                          'or type their names separated by spaces. Paths containing spaces should be '
                          'surrounded by quotation marks.\nPress ENTER when you\'re done: ')

        if "win" in sys.platform:
            # the POSIX shlex.split uses backslashes for escape sequences, so Windows paths need to set posix=False
            file_list = shlex.split(files_str, posix=False)

            # the non-POSIX shlex.split does not automatically clean quotation marks from the final product
            file_list = [f.replace('"', '').replace("'", "") for f in file_list]
        else:
            file_list = shlex.split(files_str, posix=True)

    # substitute in shell variables and get absolute paths
    for i in range(len(file_list)):
        file_list[i] = os.path.abspath( os.path.expanduser(os.path.expandvars(file_list[i])) )

    return file_list