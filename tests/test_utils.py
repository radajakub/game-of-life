import numpy as np

from game_of_life.utils.utils import crop_box, fill_nonzero, get_players, keep_only_number, safe_8_neighborhood
from game_of_life.config import BOARD_DTYPE


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


def test_fill_nonzero():
    input_box = np.array([
        [10, 0, 5, 0],
        [0, 3, 1, -1],
        [0, 0, 0, 0],
        [0, 4, 0, 0],
    ], dtype=BOARD_DTYPE)

    reference_box = np.array([
        [2, 0, 2, 0],
        [0, 2, 2, 2],
        [0, 0, 0, 0],
        [0, 2, 0, 0],
    ], dtype=BOARD_DTYPE)

    assert np.array_equal(fill_nonzero(input_box, fill_value=2), reference_box)


def test_keep_only_number():
    input_box = np.array([
        [1, 0, 2, 0],
        [0, 1, 0, 1],
        [0, 0, 0, 0],
        [3, 0, 3, 0],
    ], dtype=BOARD_DTYPE)

    reference_box = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 1],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ], dtype=BOARD_DTYPE)

    assert np.array_equal(keep_only_number(input_box, number=1), reference_box)


def test_get_players():
    input_box = np.array([
        [1, 0, 2, 0],
        [0, 1, 0, 1],
        [0, 0, 0, 0],
        [3, 0, 3, 0],
    ], dtype=BOARD_DTYPE)

    reference_players = np.array([1, 2, 3], dtype=BOARD_DTYPE)

    assert np.array_equal(get_players(input_box), reference_players)


def test_safe_8_neighborhood_in():
    input_box = np.array([
        [1, 0, 2, 0],
        [0, 1, 0, 1],
        [0, 0, 0, 0],
        [3, 0, 3, 0],
    ], dtype=BOARD_DTYPE)

    reference_box = np.array([
        [1, 0, 2],
        [0, 1, 0],
        [0, 0, 0],
    ], dtype=BOARD_DTYPE)

    assert np.array_equal(safe_8_neighborhood(input_box, r=1, c=1), reference_box)


def test_safe_8_neighborhood_out():
    input_box = np.array([
        [1, 0, 2, 0],
        [0, 1, 0, 1],
        [0, 0, 0, 0],
        [3, 0, 3, 0],
    ], dtype=BOARD_DTYPE)

    reference_box = np.array([
        [2, 0],
        [0, 1],
        [0, 0],
    ], dtype=BOARD_DTYPE)

    assert np.array_equal(safe_8_neighborhood(input_box, r=1, c=3), reference_box)
