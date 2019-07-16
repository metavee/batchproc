import batchproc as bp

# test function that adds some characters to the end of a file
def append_zzz(filename):
    with open(filename, 'a') as fd:
        fd.write('zzz')

if __name__ == "__main__":
    # get list of files from user, either from command-line args or stdin
    args = bp.get_file_list()

    # write results to this file
    log_filename = 'batch_process.log'

    # optionally, a list of functions can be specified that are applied to the list of files before starting
    # append_zzz only works on files, so expand_folder is used, which recursively replaces folders with their contents
    file_filters = (bp.expand_folder,)

    processor = bp.BatchProcessor(args, append_zzz, file_filters, log_filename=log_filename)

    # apply our data-processing function, append_zzz to all files specified by user
    processor.start()