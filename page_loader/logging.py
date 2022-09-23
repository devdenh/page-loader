from logging import Formatter
import logging
import sys


def init_logging(logging_path):

    formatter = Formatter("[%(asctime)s:%(levelname)s] "
                          "[logger:%(name)s] %(message)s")

    file_handler = logging.FileHandler(filename=logging_path, mode='w')
    file_handler.setLevel(logging.WARNING)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    return formatter, file_handler, console_handler
