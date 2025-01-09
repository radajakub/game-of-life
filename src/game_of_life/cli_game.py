import numpy as np

from game_of_life.engine.game import Game
from game_of_life.engine.board import Board
from game_of_life.engine.pattern import Pattern
from game_of_life.utils.path_manager import PathManager

if __name__ == "__main__":
    path_manager = PathManager()

    board = Board.new(width=10, height=10)
    glider = Pattern.new(np.array([[0, 0, 1], [1, 0, 1], [0, 1, 1]]), name="Glider")
    glider.save(path_manager)
    board.place_pattern(glider, x0=0, y0=0, player=1)

    reverse_glider = glider.clone()
    reverse_glider.rotate_clockwise(num=2)
    board.place_pattern(reverse_glider, x0=7, y0=7, player=2)

    game = Game(board=board, frequency=10, steps=100, players=1)
    game.run()
