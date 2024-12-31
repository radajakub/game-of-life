import numpy as np

TOP_LEFT_CORNER = "┌"
TOP_RIGHT_CORNER = "┐"
BOTTOM_LEFT_CORNER = "└"
BOTTOM_RIGHT_CORNER = "┘"
HORIZONTAL_BORDER = "─"
VERTICAL_BORDER = "│"
HORIZONTAL_DOWN_BORDER = "┬"
HORIZONTAL_UP_BORDER = "┴"
VERTICAL_RIGHT_BORDER = "├"
VERTICAL_LEFT_BORDER = "┤"
CROSS_BORDER = "┼"

EMPTY_CELL = " "
PLAYER_CELL = "█"


def stringify_board(board: np.ndarray) -> str:
    char_board = np.zeros_like(board, dtype=str)
    char_board[board == 0] = EMPTY_CELL
    char_board[board != 0] = PLAYER_CELL

    height, width = board.shape
    res = []
    res.append(TOP_LEFT_CORNER + (HORIZONTAL_BORDER + HORIZONTAL_DOWN_BORDER)
               * (width - 1) + HORIZONTAL_BORDER + TOP_RIGHT_CORNER)
    for r in range(height):
        if r != 0:
            res.append(VERTICAL_RIGHT_BORDER + (HORIZONTAL_BORDER + CROSS_BORDER)
                       * (width - 1) + HORIZONTAL_BORDER + VERTICAL_LEFT_BORDER)
        res.append(VERTICAL_BORDER + VERTICAL_BORDER.join(char_board[r]) + VERTICAL_BORDER)
    res.append(BOTTOM_LEFT_CORNER + (HORIZONTAL_BORDER + HORIZONTAL_UP_BORDER)
               * (width - 1) + HORIZONTAL_BORDER + BOTTOM_RIGHT_CORNER)
    return "\n".join(res)
