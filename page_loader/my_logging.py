import logging
import sys
from logging import Formatter
from pathlib import Path


APP_LOG = Path(__file__).parent.parent / 'logs.log'

formatter = Formatter("[%(asctime)s:%(levelname)s] [logger:%(name)s] %(message)s")

file_handler = logging.FileHandler(filename=APP_LOG, mode='w')
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler(stream=sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
