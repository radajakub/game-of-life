""" Module for the toggle cell view. """

from kivy.uix.button import Button

from game_of_life.gui.consts import COLORS


class ToggleCellView(Button):
    """
    Widget for a single cell on the board that can be toggled alive or dead.
    It is used both to create a pattern and to set up a simulation.
    It can handle multiple players and reflect underlying model.
    """

    def __init__(self, row: int, col: int, value: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.row = row
        self.col = col
        self.background_normal = ''
        self.update(value)

    def update(self, value: int) -> None:
        """ Update the color of the cell based on the value. """

        self.background_color = COLORS[value]
