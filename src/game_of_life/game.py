from time import sleep

from grid import Grid


class Game:
    def __init__(self, grid: Grid, frequency: int = 10, steps: int = 100) -> None:
        self.grid = grid
        self.frequency = frequency
        self.time_delay = 1 / frequency
        self.steps = steps

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return f"Game(grid=({self.grid.width}, {self.grid.height}), frequency={self.frequency}, time_delay={self.time_delay})"

    def set_frequency(self, frequency: int) -> None:
        self.frequency = frequency
        self.time_delay = 1 / frequency

    def set_steps(self, steps: int) -> None:
        self.steps = steps

    def reset(self) -> None:
        self.grid.reset()

    def run(self) -> None:
        print(self.grid)
        if self.steps < 0:
            self._run_infinite()
        else:
            self._run_finite()

    def _run_finite(self) -> None:
        for _ in range(self.steps):
            sleep(self.time_delay)
            self.grid = self.grid.evolve()
            print(self.grid)

    def _run_infinite(self) -> None:
        # TODO: implement asynchronous processing to stop this
        while True:
            sleep(self.time_delay)
            self.grid = self.grid.evolve()
            print(self.grid)
