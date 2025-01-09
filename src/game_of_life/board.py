from __future__ import annotations

import numpy as np
from scipy.signal import convolve2d

from config import BOARD_DTYPE, DEFAULT_BOARD_HEIGHT, DEFAULT_BOARD_WIDTH
from pattern import Pattern
from utils import fill_nonzero, safe_8_neighborhood
from visualization import stringify_board


NEIGHBOR_KERNEL = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])


def count_neighbors(board: np.ndarray) -> np.ndarray:
    return convolve2d(board, NEIGHBOR_KERNEL, mode="same", boundary="fill", fillvalue=0)


def get_majority_player(board: np.ndarray) -> int:
    # filter out dead cells
    vals = board.flatten()
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
    @staticmethod
    def new(width: int = DEFAULT_BOARD_WIDTH, height: int = DEFAULT_BOARD_HEIGHT) -> Board:
        return Board(np.zeros((height, width), dtype=BOARD_DTYPE))

    def __init__(self, data: np.ndarray) -> None:
        self.height, self.width = data.shape
        self.data = data

        # kernel for counting neighbors
        self.kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(height={self.height}, width={self.width}, alive={np.sum(self.data != 0)})"

    def __str__(self) -> str:
        return stringify_board(self.data)

    def reset(self) -> None:
        self.data = np.zeros((self.height, self.width), dtype=BOARD_DTYPE)

    def can_place_pattern(self, pattern: Pattern, x0: int, y0: int, player: int = 1) -> bool:
        dy, dx = pattern.height, pattern.width

        # does not go outside the bounds of the board
        fits_board = 0 <= y0 <= self.height - dy and 0 <= x0 <= self.width - dx

        # is not occupied by another player
        placement = self.data[y0:y0 + dy, x0:x0 + dx]
        foreign_mask = (placement != player) & (placement != 0)
        is_not_foreign = np.all(foreign_mask == 0)

        return fits_board and is_not_foreign

    def place_pattern(self, pattern: Pattern, x0: int, y0: int, player: int = 1) -> None:
        pattern = pattern.assign_to_player(player)

        # test if the pattern fits in the board
        if not self.can_place_pattern(pattern, x0, y0):
            raise ValueError(f"pattern {pattern} cannot be placed at position {x0, y0}")

        dy, dx = pattern.height, pattern.width
        # only place the alive cells, do not overwrite existing ones with dead cells
        alive_mask = pattern.data != 0
        self.data[y0:y0 + dy, x0:x0 + dx][alive_mask] = pattern.data[alive_mask]

    def evolve(self) -> Board:
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
