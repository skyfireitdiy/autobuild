import logging

logging.basicConfig(format='[%(levelname)6s %(asctime)s %(module)20s:%(lineno)5d] --> %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


file_formatter = logging.Formatter('[%(levelname)6s %(asctime)s %(module)20s:%(lineno)5d] --> %(message)s')
file = logging.FileHandler("build_error.log")
file.setLevel(logging.WARN)
file.setFormatter(file_formatter)
logger.addHandler(file)

