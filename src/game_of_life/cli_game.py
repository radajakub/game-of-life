import numpy as np

from game import Game
from grid import Grid
from entity import Entity

if __name__ == "__main__":
    grid = Grid.new(width=10, height=10)
    glider = Entity(np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]), name="Glider")
    grid.place_entity(glider, (0, 0))

    game = Game(grid=grid, frequency=10, steps=100)
    game.run()
