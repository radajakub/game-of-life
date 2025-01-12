# game-of-life

Implementation and extension of Conway's Game of Life.
The package includees an engine that simulates the game for the traditional single player mode but also handles multi-player mode, where multiple players compete against each other.

## Installation

To install the package, first create a virtual environment to separate the dependencies from the rest of the system.
Personally, I use `pyenv` to create the virtual environment, but the traditional `venv` can also be used.

To continue with `pyenv`, run the following command to create the virtual environment.

```bash
pyenv virtualenv 3.13.1 game-of-life
```

Then, install the dependencies using `pip`.

```bash
pip install -r requirements.txt
```

To install the package so that it can be run easily, run the following command.

```bash
pip install -e .
```

The last two commands can be combined into a single command by running `make install`.

## Usage

### Starting the app

To run the application `GUI`, run the following command:

```bash
make run
```

This will start a Kivy GUI application with the Game of Life.

### Creating a new pattern

The first big functionality is creating a new pattern.
A pattern is a grid of cells that can be considered as a single entity and are placed on the board.
In this mode, thre is an interactive grid of cells that can be toggled on and off, or alive and dead.

In this way, the user can create a pattern that can be used in the game.
There is the option to save the pattern to a file, but only after we input the name of the pattern.
The file is saved to internal database under the inputed name.

User can also load and copy a pattern from the database, these patters are displayed in a row under the grid.
Another action is resizing the grid, for example, in a case that the user needs to use more or less space for the pattern.
Lastly, user can clear the grid and start over, or he can test the pattern.

### Testing the pattern

Testing the pattern takes the user to a new screen.
This time, there is a non-interactive grid that will only display the state of the pattern under the simulation rules.
On the right side there are simple actions the user can take.
He can adjust the simulation speed and the the number of steps, he can also evolve it one step at a time or let it run automatically.

After he is done, he can go back to the previous screen and save the pattern to the database or edit it again.

### Setting up the game for multi-player mode

From the introduction screen, the use can also choose to start a Simulation.
This button will take him to a new screen which looks very similar to the screen for creating new patterns.
The difference is that the user can now select a user under which the cell is toggled.
In this way, the user can create a pattern for a specific user and then let them evolve together.

The player is deteremined by the color of the cell, the color is selected by the arrow buttons next to the bigger colorful square.

User can also select a pattern. The pattern is enlarged on the right side and can be rotated and reflected using the action buttons.
That is for easier copying of the pattern on the board.

When the game is set up, the user can start the simulation by pressing the `Start` button.
It takes him to the exact same screen as the one for testing the pattern and which was described in the previous section.

## Tests

There are unit tests covering the engine functionality, the GUI is not covered by tests.
The tests are run by the `make test` command which displays the results in the terminal.
