import logging
import sys

# get logger
logger = logging.getLogger()

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# create strea handler
stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler("app.log")

# set formatter
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# add handler to logger
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

# set log level
logger.setLevel(logging.DEBUG)
