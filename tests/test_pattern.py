import numpy as np
import pytest

from game_of_life.engine.pattern import Pattern


@pytest.fixture
def pattern():
    return Pattern(np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]), name="Glider")


def test_assign_to_player(pattern):
    assert np.array_equal(pattern.data, np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]))

    pattern = pattern.assign_to_player(player=3)

    assert np.array_equal(pattern.data, np.array([[0, 0, 3], [3, 0, 3], [0, 3, 3]]))


def test_rotate_clockwise(pattern):
    assert np.array_equal(pattern.data, np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]))

    pattern.rotate_clockwise(num=1)

    assert np.array_equal(pattern.data, np.array([[0, 1, 0], [1, 0, 0], [1, 1, 1]]))

    pattern.rotate_clockwise(num=2)

    assert np.array_equal(pattern.data, np.array([[1, 1, 1], [0, 0, 1], [0, 1, 0]]))


def test_rotate_counterclockwise(pattern):
    assert np.array_equal(pattern.data, np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]))

    pattern.rotate_counterclockwise(num=1)

    assert np.array_equal(pattern.data, np.array([[1, 1, 1], [0, 0, 1], [0, 1, 0]]))

    pattern.rotate_counterclockwise(num=2)

    assert np.array_equal(pattern.data, np.array([[0, 1, 0], [1, 0, 0], [1, 1, 1]]))


def test_reflect_diagonal(pattern):
    assert np.array_equal(pattern.data, np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]))

    pattern.reflect_diagonal()

    assert np.array_equal(pattern.data, np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]]))


def test_reflect_horizontal(pattern):
    assert np.array_equal(pattern.data, np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]))

    pattern.reflect_horizontal()

    assert np.array_equal(pattern.data, np.array([[1, 0, 0], [1, 0, 1], [1, 1, 0]]))


def test_reflect_vertical(pattern):
    assert np.array_equal(pattern.data, np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]))

    pattern.reflect_vertical()

    assert np.array_equal(pattern.data, np.array([[0, 1, 1], [1, 0, 1], [0, 0, 1]]))
