import sys, os, logging

LOG_FORMAT = "%(levelname)s - %(message)s - %(asctime)s"
logging.basicConfig(filename = ".\\morgue-analyser.log",
    level= logging.DEBUG,
    format = LOG_FORMAT,
    filemode = 'w')
logger = logging.getLogger()

#TODO change the cwd to that given in the cl args. If that cannot be done put a
# meaningful message to output.
# (sys.argv[1:]))

#TODO read the files in cwd ending in .txt into some sorta buffer

#TODO parse the files and report

#TODO write to an output file in the morgue - write logs and program output.

output_variable = "This string is in a variable to be replaced by meaningful program output later."
results_file = open(".\\morgue-analysis.txt", 'w')
logger.info("Opened output for writing")
results_file.write(output_variable)
#TODO handle cannot male or write errors - permissions etc
results_file.close
logger.info("Closed output file")





logger.debug("This is a test debug level log message")
logger.info("This is a test info level log message")
logger.warning("This is a test warning level log message")
logger.error("This is a test error level log message")
logger.critical("This is a test critical level log message")
