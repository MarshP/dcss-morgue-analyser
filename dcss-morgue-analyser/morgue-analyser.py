import sys, os, logging, glob, fnmatch, re
from data_collection_functions import *

# TODO Learn to use a debugger. Begin to use it in the dev process.

# TODO Learn more on logging best practice. Decide how to log the application and whether to use separate modules.
# Logging module?
import logging

def start_logging():
    LOG_FORMAT = "%(levelname)s - %(message)s - %(asctime)s"
    logging.basicConfig(filename=".\\morgue-analyser.log",
                        level=logging.DEBUG,
                        format=LOG_FORMAT,
                        filemode='w')
    logger = logging.getLogger()

start_logging()

# TODO Learn to make and run tests, and do so once we have some functions

# TODO read the files in cwd ending in .txt into some sorta concatenated buffer or even a new, big, file

def read_morgue_files(directory_path):
    buffer = ''
    # may need a rethink if memory issues
    for filename in os.listdir(directory_path):
        if fnmatch.fnmatch(filename, '*.txt'):
            WorkingFile = open((directory_path+'\\'+filename),'r')
            buffer = WorkingFile.read()
            # calls to stat collection fns go here
            collect_data(buffer)
            # WOuld one big fn be better? Pass the buffer once? But not as modular.
            WorkingFile.close()



read_morgue_files('..\\tests\\test-data')
# change to '.' for cwd after testing



# TODO A fn for each regex so they can be modularly added




# ContentToParse = open(os.path.relpath(
#     file_path))
# print(ContentToParse.readlines())
# content_to_parse = open(os.path.relpath(,).\\.\\tests\\test-data\\morgue-Mash-20170822-155351.txt)


# TODO parse the files against searched terms and report

# TODO write to an output file in the morgue - write logs and program output.

#output_variable = "This string is in a variable to be replaced by meaningful program output later."
#results_file = open(".\\morgue-analysis.log", 'w')  # later.txt or .md
#logger.info("Opened output for writing")
#results_file.write(output_variable)
# TODO handle possible errors throughout. Cannot make file or write errors - permissions etc.
#results_file.close()
#logger.info("Closed output file")

#logger.debug("This is a test debug level log message y")
#logger.info("This is a test info level log message")
#logger.warning("This is a test warning level log message")
#logger.error("This is a test error level log message")
#logger.critical("This is a test critical level log message")