import numpy as np

from game import Game
from board import Board
from entity import Entity

if __name__ == "__main__":
    board = Board.new(width=10, height=10)
    glider = Entity(np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]), name="Glider")
    board.place_entity(glider, (0, 0))

    reverse_glider = glider.clone()
    reverse_glider.reflect_horizontal()
    board.place_entity(reverse_glider, (7, 7))

    game = Game(board=board, frequency=10, steps=100)
    game.run()
