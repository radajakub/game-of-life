"""
This is the configuration file for the game of life engine part.
Specifically default values and strings for simple file db.
"""

import numpy as np

BOARD_DTYPE = np.int32
DEFAULT_BOARD_WIDTH = 10
DEFAULT_BOARD_HEIGHT = 10

DEFAULT_FREQUENCY = 10
DEFAULT_STEPS = 100

DB_ROOT = "db"
DB_BOARD_DIR = "boards"
DB_PATTERN_DIR = "entities"
