from game_of_life.config import DEFAULT_FREQUENCY, DEFAULT_STEPS
from game_of_life.engine.board import Board


class Game:
    def __init__(self, board: Board, frequency: int = DEFAULT_FREQUENCY, steps: int = DEFAULT_STEPS) -> None:
        self.board = board
        self.original_board = board.copy()
        self.boards = []

        self.frequency = frequency
        self.time_delay = 1 / frequency
        self.steps = steps
        self.i = 0

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"Game(board=({self.board.width}, {self.board.height}), frequency={self.frequency}, time_delay={self.time_delay})"

    def set_frequency(self, frequency: int) -> None:
        self.frequency = frequency
        self.time_delay = 1 / frequency

    def set_steps(self, steps: int) -> None:
        self.steps = steps

    def restart(self) -> None:
        self.board = self.original_board.copy()
        self.boards = []
        self.i = 0

    def next_step(self) -> None:
        self.boards.append(self.board.copy())
        self.board = self.board.evolve()
        self.i += 1

    def previous_step(self) -> None:
        self.board = self.boards[-1]
        self.boards.pop()
        self.i -= 1

    def can_go_previous(self) -> bool:
        return len(self.boards) > 0

    def can_go_next(self) -> bool:
        is_alive = self.board.count_alive_cells() > 0

        if len(self.boards) == 0:
            return is_alive

        return is_alive and not self.board.is_equal(self.boards[-1])

    def run_step(self) -> bool:
        if not self.can_go_next() or self.i >= self.steps:
            return False

        self.board = self.board.evolve()
        self.i += 1
        return True
