from time import sleep

from board import Board


class Game:
    def __init__(self, board: Board, frequency: int = 10, steps: int = 100, players: int = 1) -> None:
        self.board = board
        self.frequency = frequency
        self.time_delay = 1 / frequency
        self.steps = steps
        self.players = players

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"Game(board=({self.board.width}, {self.board.height}), frequency={self.frequency}, time_delay={self.time_delay}, players={self.players})"

    def set_frequency(self, frequency: int) -> None:
        self.frequency = frequency
        self.time_delay = 1 / frequency

    def set_steps(self, steps: int) -> None:
        self.steps = steps

    def reset(self) -> None:
        self.board.reset()

    def run(self) -> None:
        print(self.board)
        if self.steps < 0:
            self._run_infinite()
        else:
            self._run_finite()

    def _run_finite(self) -> None:
        for _ in range(self.steps):
            sleep(self.time_delay)
            self.board = self.board.evolve()
            print(self.board)

    def _run_infinite(self) -> None:
        # TODO: implement asynchronous processing to stop this
        while True:
            sleep(self.time_delay)
            self.board = self.board.evolve()
            print(self.board)
