""" Module for the cell view widget. """

from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color

from game_of_life.gui.consts import COLORS


class CellView(Widget):
    """
    CellView widget is non-interactive cell on a board.
    It is used to display the state of a cell either in a pattern or during a simulation.
    The user cannot toggle the state as in ToggleCellView.
    """

    def __init__(self, row: int, col: int, value: int, **kwargs):
        super().__init__(**kwargs)
        self.row = row
        self.col = col
        self.size_hint = (1, 1)

        self._change_color(value)
        self.rect = Rectangle(pos=self.pos, size=self.size)
        self.canvas.before.add(self.rect)

        self.bind(pos=self._update_rect, size=self._update_rect)

    def _change_color(self, value: int) -> None:
        """ Change the color of the cell based on the value. """

        self.canvas.before.add(Color(*COLORS[value]))

    def _update_rect(self, _, __):
        """ Update the underyling rectangle on the canvas. """
        self.rect.pos = self.pos
        self.rect.size = self.size

    def update(self, value: int) -> None:
        """ Update the color of the cell based on the value. """

        self.canvas.before.clear()
        self._change_color(value)
        self.canvas.before.add(self.rect)
