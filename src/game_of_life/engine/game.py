""" Module handling parameters and board for the Game of Life """

from game_of_life.config import DEFAULT_FREQUENCY, DEFAULT_STEPS
from game_of_life.engine.board import Board


class Game:
    """
    Class handling parameters and higer-level interface for the Game of Life.
    Separation of next/previous step logic and running logic.
    """

    def __init__(self, board: Board, frequency: int = DEFAULT_FREQUENCY, steps: int = DEFAULT_STEPS) -> None:
        """
        Initialize the Game of Life with the given board and parameters.

        Args:
            board: board to use for the Game of Life
            frequency: frequency of the game
            steps: number of steps to run
        """

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
        """
        Set the frequency of the game, i.e. how fast the board evolves per second.

        Args:
            frequency: frequency of the game
        """

        self.frequency = frequency
        self.time_delay = 1 / frequency

    def set_steps(self, steps: int) -> None:
        """
        Set the number of steps to run in the simulation.

        Args:
            steps: number of steps to run
        """

        self.steps = steps

    def restart(self) -> None:
        """ Restart the game, i.e. reset the board and step counter to the original state. """

        self.board = self.original_board.copy()
        self.boards = []
        self.i = 0

    def next_step(self) -> None:
        """ Evolve the board once to the next generation. """

        self.boards.append(self.board.copy())
        self.board = self.board.evolve()
        self.i += 1

    def previous_step(self) -> None:
        """ Go back to the previous step by looking at history. """

        self.board = self.boards[-1]
        self.boards.pop()
        self.i -= 1

    def can_go_previous(self) -> bool:
        """ Check if the game can go back to the previous step. """

        return len(self.boards) > 0

    def can_go_next(self) -> bool:
        """ Check if the game can evolve to the next step. """

        is_alive = self.board.count_alive_cells() > 0

        if len(self.boards) == 0:
            return is_alive

        return is_alive and not self.board.is_equal(self.boards[-1])

    def run_step(self) -> bool:
        """ Evolve the board once to the next generation as the game is running. """

        if not self.can_go_next() or self.i >= self.steps:
            return False

        self.board = self.board.evolve()
        self.i += 1
        return True
