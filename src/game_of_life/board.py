from __future__ import annotations

import numpy as np
from scipy.signal import convolve2d

from config import BOARD_DTYPE, DEFAULT_BOARD_HEIGHT, DEFAULT_BOARD_WIDTH
from entity import Entity
from visualization import stringify_board


class Board:
    @staticmethod
    def new(width: int = DEFAULT_BOARD_WIDTH, height: int = DEFAULT_BOARD_HEIGHT) -> Board:
        return Board(np.zeros((height, width), dtype=BOARD_DTYPE))

    def __init__(self, data: np.ndarray) -> None:
        self.height, self.width = data.shape
        self.data = data

    def __repr__(self) -> str:
        return f"board(height={self.height}, width={self.width}, alive={np.sum(self.data != 0)})"

    def __str__(self) -> str:
        return stringify_board(self.data)

    def reset(self) -> None:
        self.data = np.zeros((self.height, self.width), dtype=BOARD_DTYPE)

    def can_place_entity(self, entity: Entity, x0: int, y0: int) -> bool:
        fits_board = 0 <= y0 <= self.height - entity.height and 0 <= x0 <= self.width - entity.width
        is_unoccupied = np.all(self.data[y0:y0 + entity.height, x0:x0 + entity.width] == 0)
        return fits_board and is_unoccupied

    def place_entity(self, entity: Entity, x0: int, y0: int) -> None:
        # test if the entity fits in the board
        if not self.can_place_entity(entity, x0, y0):
            raise ValueError(f"Entity {entity} cannot be placed at position {x0, y0}")

        dy, dx = entity.height, entity.width
        self.data[y0:y0 + dy, x0:x0 + dx] = entity.data

    def evolve_naive(self) -> Board:
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        neighbor_counts = convolve2d(self.data, kernel, mode="same", boundary="fill", fillvalue=0)

        new_data = np.zeros_like(self.data)
        for r in range(self.height):
            for c in range(self.width):
                # is alive
                if self.data[r, c] != 0:
                    # (1) any live cell with fewer than two live neighbours dies
                    if neighbor_counts[r, c] < 2:
                        new_data[r, c] = 0
                    # (2) any live cell with two or three live neighbours lives on to the next generation
                    elif 2 <= neighbor_counts[r, c] <= 3:
                        new_data[r, c] = 1
                    # (3) any live cell with more than three live neighbours dies
                    elif neighbor_counts[r, c] > 3:
                        new_data[r, c] = 0
                # is dead
                else:
                    # (4) any dead cell with exactly three live neighbours becomes a live cell
                    if neighbor_counts[r, c] == 3:
                        new_data[r, c] = 1

        return Board(new_data)

    def evolve(self) -> Board:
        # compute counts of neighbors for each cell
        kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]])
        neighbor_counts = convolve2d(self.data, kernel, mode="same", boundary="fill", fillvalue=0)

        # apply the rules for counts

        new_data = np.zeros_like(self.data)

        # (1) any live cell with fewer than two live neighbours dies
        # (2) any live cell with two or three live neighbours lives on to the next generation
        # (3) any live cell with more than three live neighbours dies
        # (4) any dead cell with exactly three live neighbours becomes a live cell

        # TODO: consider majority for multiple players
        mask = (neighbor_counts == 3) | ((self.data != 0) & (neighbor_counts == 2))
        new_data[mask] = 1

        return Board(new_data)


if __name__ == "__main__":
    board = Board.new(width=10, height=10)
    print(board)
