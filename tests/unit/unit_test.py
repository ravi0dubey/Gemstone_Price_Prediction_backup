import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from source.logger.logger import logging

logging.info("testing from unit_test")