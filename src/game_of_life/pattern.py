from __future__ import annotations
import pickle

import numpy as np

from path_manager import PathManager
from visualization import stringify_board
from utils import crop_box, fill_nonzero


class Pattern:
    @staticmethod
    def new(box: np.ndarray, name: str) -> Pattern:
        return Pattern(fill_nonzero(crop_box(box), fill_value=1), name)

    @staticmethod
    def load(path: str) -> Pattern:
        with open(path, "rb") as f:
            return pickle.load(f)

    def __init__(self, data: np.ndarray, name: str) -> None:
        self.name = name
        self.data = data
        self.height, self.width = self.data.shape

    def __repr__(self) -> str:
        return f"pattern(name={self.name}, height={self.height}, width={self.width})"

    def __str__(self) -> str:
        return stringify_board(self.data)

    def _update_shape(self) -> None:
        self.height, self.width = self.data.shape

    def rotate_clockwise(self, num: int = 1) -> None:
        self.data = np.rot90(self.data, k=num, axes=(1, 0))
        self._update_shape()

    def rotate_counterclockwise(self, num: int = 1) -> None:
        self.data = np.rot90(self.data, k=num, axes=(0, 1))
        self._update_shape()

    def reflect_diagonal(self) -> None:
        self.data = np.transpose(self.data)
        self._update_shape()

    def reflect_horizontal(self) -> None:
        self.data = np.fliplr(self.data)
        self._update_shape()

    def reflect_vertical(self) -> None:
        self.data = np.flipud(self.data)
        self._update_shape()

    def clone(self) -> Pattern:
        return Pattern(self.data, self.name)

    def rename(self, name: str) -> None:
        self.name = name

    def assign_to_player(self, player: int) -> Pattern:
        return Pattern(fill_nonzero(self.data, fill_value=player), self.name)

    def save(self, path_manager: PathManager) -> None:
        path = path_manager.get_pattern_path(self.name)
        with open(path, "wb") as f:
            pickle.dump(self, f)


if __name__ == "__main__":
    pattern = Pattern(np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]), name="Glider")
    print(pattern)
    pattern.rotate_clockwise(num=2)
    print(pattern)
    pattern.reflect_horizontal()
    print(pattern)
