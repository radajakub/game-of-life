from __future__ import annotations
import pickle

import numpy as np
from scipy.signal import convolve2d

from config import GRID_DTYPE, DEFAULT_GRID_HEIGHT, DEFAULT_GRID_WIDTH
from entity import Entity
from visualization import stringify_grid


class Grid:
    @staticmethod
    def new(width: int = DEFAULT_GRID_WIDTH, height: int = DEFAULT_GRID_HEIGHT) -> Grid:
        return Grid(np.zeros((height, width), dtype=GRID_DTYPE))

    @staticmethod
    def load(path: str) -> Grid:
        with open(path, "rb") as f:
            return pickle.load(f)

    def __init__(self, data: np.ndarray) -> None:
        self.height, self.width = data.shape
        self.data = data

    def __repr__(self) -> str:
        return f"Grid(height={self.height}, width={self.width}, alive={np.sum(self.data != 0)})"

    def __str__(self) -> str:
        return stringify_grid(self.data)

    def save(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(self, f)

    def reset(self) -> None:
        self.data = np.zeros((self.height, self.width), dtype=GRID_DTYPE)

    def place_entity(self, entity: Entity, position: tuple[int, int]) -> None:
        # test if the entity fits in the grid
        assert 0 <= position[0] <= self.height - entity.height
        assert 0 <= position[1] <= self.width - entity.width

        self.data[position[0]:position[0] + entity.height, position[1]:position[1] + entity.width] = entity.data

    def evolve_naive(self) -> Grid:
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

        return Grid(new_data)

    def evolve(self) -> Grid:
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

        return Grid(new_data)


if __name__ == "__main__":
    grid = Grid.new(width=10, height=10)
    print(grid)
