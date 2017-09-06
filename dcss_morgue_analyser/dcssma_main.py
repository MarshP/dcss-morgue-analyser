import fnmatch
import logging
import os
from dcssma_data_processing import *


def main():

    log_format = "%(levelname)s - %(message)s - %(asctime)s - %(name)s"
    logging.basicConfig(filename=".\\morgue-analyser.log",
                        level=logging.INFO,
                        format=log_format,
                        filemode='w')
    logger = logging.getLogger(__name__)
    logger.info('Start logging in main(). Column delimiter is " - ".')
    logger.info('Set logging level ' + logging.getLevelName(logger.getEffectiveLevel()) + ' in this module.')
    # TODO centralise logger config some point for all modules

    working_dir = '..\\test\\test-data'
    logger.info('Set cwd to ' + working_dir)
    # TODO change to '.' for cwd after testing. Later write tests so this stays stable

    def join_morgue_files(directory_path):
        ConcatenatedMorgueFile = open((directory_path + '\\' + 'dcssma-temp-file.txt'), 'w')
        logger.info('Start concatenate the morgue files into dcssma-temp-file.txt')
        for filename in os.listdir(directory_path):
            if fnmatch.fnmatch(filename, 'morgue*[0123456789].txt'):
                WorkingFile = open((directory_path + '\\' + filename), 'r')
                ConcatenatedMorgueFile.write(WorkingFile.read())
        ConcatenatedMorgueFile.close()

    join_morgue_files(working_dir)

    def send_data_to_process(directory_path):
        SendingFileHandle = open((directory_path + '\\' + 'dcssma-temp-file.txt'), 'r')
        buffer = SendingFileHandle.read()
        process_data(buffer, directory_path)
        logger.info('Start parsing and analysing content of dcssma-temp-file.txt')
        SendingFileHandle.close()
        os.remove(directory_path + '\\' + 'dcssma-temp-file.txt')
        logger.info('Delete concatenated temporary file dcssma-temp-file.txt.')
    send_data_to_process(working_dir)

    # TODO handle and log errors throughout. try-except-logger.error


if __name__ == '__main__':
    main()

