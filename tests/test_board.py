import pytest

import numpy as np

from game_of_life.engine.board import Board, count_neighbors, get_majority_player
from game_of_life.engine.pattern import Pattern


def test_count_neighbors():
    board = np.array([
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ])

    neighbors = count_neighbors(board)

    assert np.array_equal(neighbors, np.array([
        [2, 4, 2],
        [2, 3, 1],
        [2, 3, 2],
    ]))


def test_get_majority_player_odd():
    board = np.array([
        [1, 2, 0],
        [1, 1, 1],
        [0, 2, 2],
    ])

    assert get_majority_player(board) == 1


def test_get_majority_player_even():
    board = np.array([
        [1, 2, 0],
        [1, 0, 1],
        [0, 2, 2],
    ])

    assert get_majority_player(board) == 0


@pytest.fixture
def board():
    return Board(data=np.array([
        [1, 2, 0, 0],
        [1, 1, 1, 0],
        [2, 2, 0, 2],
        [0, 0, 0, 0],
    ]))


def test_board_new(board: Board):
    assert board.height == 4
    assert board.width == 4
    assert board.count_alive_cells() == 8


def test_board_clear(board: Board):
    board.clear()

    assert board.height == 4
    assert board.width == 4
    assert board.count_alive_cells() == 0


def test_board_shrink(board: Board):
    assert board.height == 4
    assert board.width == 4

    board.resize(2, 2)

    assert board.height == 2
    assert board.width == 2
    assert np.array_equal(board.data, np.array([
        [1, 1],
        [2, 0],
    ]))


def test_board_grow(board: Board):
    assert board.height == 4
    assert board.width == 4

    board.resize(6, 6)

    assert board.height == 6
    assert board.width == 6
    assert np.array_equal(board.data, np.array([
        [0, 0, 0, 0, 0, 0],
        [0, 1, 2, 0, 0, 0],
        [0, 1, 1, 1, 0, 0],
        [0, 2, 2, 0, 2, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
    ]))


@pytest.fixture
def pattern():
    return Pattern(np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]), name="Glider")


def test_board_place_pattern(board: Board, pattern: Pattern):
    board.clear()

    assert board.can_place_pattern(pattern, 0, 0)

    board.place_pattern(pattern, 1, 1)

    assert np.array_equal(board.data, np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 1, 0, 1],
        [0, 0, 1, 1],
    ]))


def test_board_evolve(board: Board, pattern: Pattern):
    step0 = np.array([
        [0, 0, 1, 0],
        [1, 0, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ])

    step1 = np.array([
        [0, 1, 0, 0],
        [0, 0, 1, 1],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ])

    step2 = np.array([
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [0, 1, 1, 1],
        [0, 0, 0, 0],
    ])

    step3 = np.array([
        [0, 0, 0, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 0],
    ])

    step4 = np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 1, 0, 1],
        [0, 0, 1, 1],
    ])

    board.clear()
    board.place_pattern(pattern, 0, 0)

    assert np.array_equal(board.data, step0)
    board = board.evolve()
    assert np.array_equal(board.data, step1)
    board = board.evolve()
    assert np.array_equal(board.data, step2)
    board = board.evolve()
    assert np.array_equal(board.data, step3)
    board = board.evolve()
    assert np.array_equal(board.data, step4)
