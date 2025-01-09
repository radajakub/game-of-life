import numpy as np

from utils import get_players

TOP_LEFT = "┌"
TOP_RIGHT = "┐"
BOTTOM_LEFT = "└"
BOTTOM_RIGHT = "┘"
HORIZONTAL = "─"
VERTICAL = "│"
HORIZONTAL_DOWN = "┬"
HORIZONTAL_UP = "┴"
VERTICAL_RIGHT = "├"
VERTICAL_LEFT = "┤"
CROSS = "┼"

EMPTY_CELL = " "
# This is currently a limited to only 2 players
PLAYER_CELLS = ["◉", "▣"]


def stringify_board(board: np.ndarray) -> str:
    if len(get_players(board)) > 2:
        raise ValueError("This function is currently limited to only 2 players")

    # get the number of players on the board
    players = get_players(board)

    # turn game board into characters
    char_board = np.zeros_like(board, dtype=str)
    char_board[board == 0] = EMPTY_CELL
    for player, symbol in zip(players, PLAYER_CELLS):
        char_board[board == player] = symbol

    # create string representation of the board
    height, width = board.shape
    res = []
    res.append(TOP_LEFT + (HORIZONTAL + HORIZONTAL_DOWN) * (width - 1) + HORIZONTAL + TOP_RIGHT)
    for r in range(height):
        if r != 0:
            res.append(VERTICAL_RIGHT + (HORIZONTAL + CROSS) * (width - 1) + HORIZONTAL + VERTICAL_LEFT)
        res.append(VERTICAL + VERTICAL.join(char_board[r]) + VERTICAL)
    res.append(BOTTOM_LEFT + (HORIZONTAL + HORIZONTAL_UP) * (width - 1) + HORIZONTAL + BOTTOM_RIGHT)
    return "\n".join(res)
