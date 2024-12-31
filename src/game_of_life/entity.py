import numpy as np

from visualization import stringify_grid
from utils import crop_box


class Entity:
    def __init__(self, box: np.ndarray, name: str) -> None:
        self.name = name
        self.data = crop_box(box)
        self.height, self.width = self.data.shape

    def __repr__(self) -> str:
        return f"Entity(name={self.name}, height={self.height}, width={self.width})"

    def __str__(self) -> str:
        return stringify_grid(self.data)

    def rotate_clockwise(self, num: int = 1) -> None:
        self.data = np.rot90(self.data, k=num, axes=(1, 0))
        self.height, self.width = self.data.shape

    def rotate_counterclockwise(self, num: int = 1) -> None:
        self.data = np.rot90(self.data, k=num, axes=(0, 1))
        self.height, self.width = self.data.shape


if __name__ == "__main__":
    entity = Entity(np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]), name="Glider")
    print(entity)
