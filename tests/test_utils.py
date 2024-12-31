import numpy as np

from src.game_of_life.utils import crop_box
from src.game_of_life.config import BOARD_DTYPE


def test_crop_box():
    input_box = np.array([
        [0, 0, 0, 0],
        [0, 1, 1, 1],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
    ], dtype=BOARD_DTYPE)

    reference_box = np.array([
        [1, 1, 1],
        [0, 1, 0],
    ], dtype=BOARD_DTYPE)

    assert np.array_equal(crop_box(input_box), reference_box)
