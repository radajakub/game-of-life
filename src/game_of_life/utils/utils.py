""" Module containing utility functions for the Game of Life board and patterns. """

import numpy as np


def crop_box(arr: np.ndarray) -> np.ndarray:
    """
    Crop the arr to the smallest rectangle that contains all the non-zero elements.

    Args:
        arr: the array to crop
    """

    ys, xs = np.where(arr != 0)
    return arr[ys.min(): ys.max() + 1, xs.min(): xs.max() + 1]


def fill_nonzero(arr: np.ndarray, fill_value: int = 1) -> np.ndarray:
    """
    Fill all non-zero elements with the given fill value.

    Args:
        arr: the array to fill
    """

    return np.where(arr != 0, fill_value, 0)


def keep_only_number(arr: np.ndarray, number: int) -> np.ndarray:
    """
    Keep only the given number in the arr.

    Args:
        arr: the array to process
        number: the number to keep
    """

    return np.where(arr == number, number, 0)


def get_players(arr: np.ndarray) -> list[int]:
    """
    Get the players on the board.

    Args:
        arr: the array where players are counted
    """

    unique = np.unique(arr)
    return unique[unique != 0]


def safe_8_neighborhood(arr: np.ndarray, r: int, c: int) -> np.ndarray:
    """
    Get the 8-neighborhood of (r, c) in arr but check the bounds of the array

    Args:
        arr: the array to get the neighborhood from
        r: the row of the center cell
        c: the column of the center cell
    """

    rows, cols = arr.shape
    return arr[max(0, r - 1):min(rows, r + 2), max(0, c - 1):min(cols, c + 2)]
