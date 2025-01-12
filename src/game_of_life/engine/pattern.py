""" Module handling patterns, board entities, for the Game of Life """

from __future__ import annotations
import pickle

import numpy as np

from game_of_life.utils.path_manager import PathManager
from game_of_life.visualization.visualization import stringify_board
from game_of_life.utils.utils import crop_box, fill_nonzero


class Pattern:
    """
    Class handling patterns, board entities, for the Game of Life.
    """

    @staticmethod
    def new(box: np.ndarray, name: str) -> Pattern:
        """
        Create a new pattern from a box or board.
        The box is cropped to the smallest possible box that contains all the non-zero values.

        Args:
            box: box or board to create the pattern from
            name: name of the pattern

        Returns:
            new pattern
        """

        return Pattern(fill_nonzero(crop_box(box), fill_value=1), name)

    @staticmethod
    def load(path: str) -> Pattern:
        """
        Load a pattern from a file.

        Args:
            path: path to the file

        Returns:
            loaded pattern
        """

        with open(path, "rb") as f:
            return pickle.load(f)

    def __init__(self, data: np.ndarray, name: str) -> None:
        """
        Initialize the pattern with the given data and name.

        Args:
            data: data of the pattern
            name: name of the pattern
        """

        self.name = name
        self.data = data
        self.height, self.width = self.data.shape

    def __repr__(self) -> str:
        return f"pattern(name={self.name}, height={self.height}, width={self.width})"

    def __str__(self) -> str:
        return stringify_board(self.data)

    def _update_shape(self) -> None:
        """ Update the shape of the pattern from the data. """

        self.height, self.width = self.data.shape

    def rotate_clockwise(self, num: int = 1) -> None:
        """
        Rotate the pattern 90 degrees clockwise for the given number of times.

        Args:
            num: number of times to rotate
        """

        self.data = np.rot90(self.data, k=num, axes=(1, 0))
        self._update_shape()

    def rotate_counterclockwise(self, num: int = 1) -> None:
        """
        Rotate the pattern 90 degrees counterclockwise for the given number of times.

        Args:
            num: number of times to rotate
        """

        self.data = np.rot90(self.data, k=num, axes=(0, 1))
        self._update_shape()

    def reflect_diagonal(self) -> None:
        """ Reflect the pattern along the main diagonal. """

        self.data = np.transpose(self.data)
        self._update_shape()

    def reflect_horizontal(self) -> None:
        """ Reflect the pattern horizontally. """

        self.data = np.fliplr(self.data)
        self._update_shape()

    def reflect_vertical(self) -> None:
        """ Reflect the pattern vertically. """

        self.data = np.flipud(self.data)
        self._update_shape()

    def clone(self) -> Pattern:
        """ Create an exact copy of the pattern. """

        return Pattern(self.data, self.name)

    def rename(self, name: str) -> None:
        """
        Rename the pattern.

        Args:
            name: new name of the pattern
        """

        self.name = name

    def assign_to_player(self, player: int) -> Pattern:
        """
        Assign the pattern to a player.
        That means replacing all live cells with the index of given player.

        Args:
            player: player to assign the pattern to
        """

        return Pattern(fill_nonzero(self.data, fill_value=player), self.name)

    def save(self, path_manager: PathManager) -> None:
        """
        Save the pattern to a file.

        Args:
            path_manager: path manager to use
        """

        path = path_manager.get_pattern_path(self.name)
        with open(path, "wb") as f:
            pickle.dump(self, f)


def load_all_patterns(path_manager: PathManager) -> list[Pattern]:
    """
    Load all patterns from the given path manager.

    Args:
        path_manager: path manager to use
    """

    return [Pattern.load(path) for path in path_manager.get_all_patterns()]


if __name__ == "__main__":
    pattern = Pattern(np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]), name="Glider")
    print(pattern)
    pattern.rotate_clockwise(num=2)
    print(pattern)
    pattern.reflect_horizontal()
    print(pattern)
