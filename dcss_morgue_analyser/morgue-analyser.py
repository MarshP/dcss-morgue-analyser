import fnmatch
import logging
import os
from data_collection_functions import *


def main():
    log_format = "%(levelname)s - %(message)s - %(asctime)s - %(name)s"
    logging.basicConfig(filename=".\\morgue-analyser.log",
                        level=logging.DEBUG,
                        format=log_format,
                        filemode='w')
    logger = logging.getLogger(__name__)
    logger.info('Begin logging. Item delimiter is en-dash/subtract symbol')

    # TODO Learn to make and run tests, and do so once we have some functions

    def join_morgue_files(directory_path):
        ConcatenatedMorgueFile = open((directory_path + '\\' + 'dcssma-temp-file.txt'), 'w')
        for filename in os.listdir(directory_path):
            if fnmatch.fnmatch(filename, '*.txt'):
                WorkingFile = open((directory_path + '\\' + filename), 'r')
                ConcatenatedMorgueFile.write(WorkingFile.read())
        ConcatenatedMorgueFile.close()

    join_morgue_files('..\\test\\test-data')
    # TODO change to '.' for cwd after testing

    def send_data_to_process(directory_path):
        SendingFileHandle = open((directory_path + '\\' + 'dcssma-temp-file.txt'), 'r')
        buffer = SendingFileHandle.read()
        collect_data(buffer, directory_path)
        SendingFileHandle.close()
        os.remove(directory_path + '\\' + 'dcssma-temp-file.txt')

    send_data_to_process('..\\test\\test-data')
    # TODO change to '.' for cwd after testing

    # TODO handle errors throughout. try-except-logger.error


if __name__ == '__main__':
    main()
