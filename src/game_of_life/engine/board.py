"""
This module implements the multi-player Game of Life board and related helper functions.
"""

from __future__ import annotations

import numpy as np
from scipy.signal import convolve2d

from game_of_life.config import BOARD_DTYPE, DEFAULT_BOARD_HEIGHT, DEFAULT_BOARD_WIDTH
from game_of_life.engine.pattern import Pattern
from game_of_life.utils.utils import fill_nonzero, safe_8_neighborhood
from game_of_life.visualization.visualization import stringify_board


NEIGHBOR_KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def count_neighbors(arr: np.ndarray) -> np.ndarray:
    """
    Compute 8 neighborhood matrix for the given board.
    This function considers all players as equal, i.e. all players contribute to the count with 1.

    Args:
        arr: 2D numpy array representing the board

    Returns:
        2D numpy array representing the 8 neighborhood matrix
    """

    return convolve2d(arr, NEIGHBOR_KERNEL, mode="same", boundary="fill", fillvalue=0)


def get_majority_player(arr: np.ndarray) -> int:
    """
    Get the majority player for the given board.
    This function finds the most frequent player in the given board.
    If the majority is a tie, it returns 0 (dead cell).

    Args:
        arr: 2D numpy array representing the board

    Returns:
        int index of the majority player
    """

    # filter out dead cells
    vals = arr.flatten()
    vals = vals[vals != 0]

    # count cells of each player and sort them in descending order
    counts = np.bincount(vals)
    sorted_counts = np.argsort(counts)[::-1]

    # if there is a tie, let the cell die (mutual annihilation)
    if counts[sorted_counts[0]] == counts[sorted_counts[1]]:
        return 0

    # return the player with the most neighbors
    return sorted_counts[0]


class Board:
    """
    This class represents the multi-player Game of Life board.
    """

    @staticmethod
    def new(width: int = DEFAULT_BOARD_WIDTH, height: int = DEFAULT_BOARD_HEIGHT) -> Board:
        """
        Create an empty board with the given width and height.

        Args:
            width: width of the board
            height: height of the board
        """

        return Board(np.zeros((height, width), dtype=BOARD_DTYPE))

    def __init__(self, data: np.ndarray) -> None:
        """
        Initialize the board with the given data and save the shape.
        Should not be used directly, used mainly for inner methods.

        Args:
            data: 2D numpy array representing the board
        """

        self.height, self.width = data.shape
        self.data = data

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(height={self.height}, width={self.width}, alive={self.count_alive_cells()})"

    def __str__(self) -> str:
        return stringify_board(self.data)

    def clear(self) -> None:
        """ Clears the board by setting all cells to 0. """

        self.data = np.zeros((self.height, self.width), dtype=BOARD_DTYPE)

    def copy(self) -> Board:
        """ Returns a copy of the board. """

        return Board(self.data.copy())

    def toggle_cell(self, r: int, c: int, value: int = 1) -> None:
        """
        Toggle the cell at the given position.
        If the cell is dead, it becomes alive and vice versa.

        Args:
            r: row index of the cell
            c: column index of the cell
            value: value to set the cell to (i.e. player index)
        """

        if self.data[r, c] == 0:
            self.data[r, c] = value
        else:
            self.data[r, c] = 0

    def count_alive_cells(self) -> int:
        """ Counts the number of alive cells on the board. """

        return np.sum(self.data != 0)

    def is_equal(self, other: Board) -> bool:
        """ Compare two boards for equality. """

        if self.height != other.height or self.width != other.width:
            return False

        return np.all(self.data == other.data)

    def resize(self, height: int, width: int) -> None:
        """
        Resize the board to the given height and width.
        If the new size is smaller, the board is cropped.
        If the new size is larger, the board is padded with dead cells.

        Args:
            height: new height of the board
            width: new width of the board
        """

        old_height, old_width = self.height, self.width
        new_height, new_width = height, width

        new_data = np.zeros((new_height, new_width), dtype=BOARD_DTYPE)

        dh = abs(old_height - new_height) // 2
        dw = abs(old_width - new_width) // 2

        if new_height < old_height and new_width < old_width:
            new_data[:, :] = self.data[dh:dh + new_height, dw:dw + new_width]
        elif new_height < old_height and new_width >= old_width:
            new_data[:, dw:dw + old_width] = self.data[dh:dh + new_height, :]
        elif new_height >= old_height and new_width < old_width:
            new_data[dh:dh + old_height, :] = self.data[:, dw:dw + new_width]
        elif new_height >= old_height and new_width >= old_width:
            new_data[dh:dh + old_height, dw:dw + old_width] = self.data

        self.data = new_data
        self.height, self.width = new_height, new_width

    def can_place_pattern(self, pattern: Pattern, x0: int, y0: int, player: int = 1) -> bool:
        """
        Check if the pattern can be placed on the board at the given position.

        Args:
            pattern: pattern to place
            x0: x-coordinate of the top-left corner of the pattern
            y0: y-coordinate of the top-left corner of the pattern
            player: player index to place the pattern for
        """

        dy, dx = pattern.height, pattern.width

        # does not go outside the bounds of the board
        fits_board = 0 <= y0 <= self.height - dy and 0 <= x0 <= self.width - dx

        # is not occupied by another player
        placement = self.data[y0:y0 + dy, x0:x0 + dx]
        foreign_mask = (placement != player) & (placement != 0)
        is_not_foreign = np.all(foreign_mask == 0)

        return fits_board and is_not_foreign

    def place_pattern(self, pattern: Pattern, x0: int, y0: int, player: int = 1) -> None:
        """
        Place the pattern on the board at the given position.

        Args:
            pattern: pattern to place
            x0: x-coordinate of the top-left corner of the pattern
            y0: y-coordinate of the top-left corner of the pattern
            player: player index to place the pattern for
        """

        pattern = pattern.assign_to_player(player)

        dy, dx = pattern.height, pattern.width
        # only place the alive cells, do not overwrite existing ones with dead cells
        alive_mask = pattern.data != 0
        self.data[y0:y0 + dy, x0:x0 + dx][alive_mask] = pattern.data[alive_mask]

    def evolve(self) -> Board:
        """
        Evolve the board to the next generation according to the extended rules of the Game of Life.
        """

        # (1) any live cell with fewer than two live neighbours dies
        # (2) any live cell with two or three live neighbours lives on to the next generation
        # (3) any live cell with more than three live neighbours dies
        # (4) any dead cell with exactly three live neighbours becomes a live cell
        # (5) when there are multiple players and cell should become alive, it becomes alive as the majority player
        # (6) in case of a tie, the cell dies (mutual annihilation)

        new_data = np.zeros_like(self.data)

        neighbor_counts = count_neighbors(fill_nonzero(self.data, fill_value=1))
        cells_to_check = np.where((neighbor_counts == 3) | ((self.data != 0) & (neighbor_counts == 2)))

        for r, c in zip(*cells_to_check):
            new_data[r, c] = get_majority_player(safe_8_neighborhood(self.data, r, c))

        return Board(new_data)


if __name__ == "__main__":
    board = Board.new(width=10, height=10)
    print(board)
