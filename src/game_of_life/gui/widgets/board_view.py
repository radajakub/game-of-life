""" Module for the board view widget. """

from kivy.uix.gridlayout import GridLayout

from game_of_life.engine.board import Board
from game_of_life.gui.widgets.toggle_cell_view import ToggleCellView


class BoardView(GridLayout):
    """ Display a square board as a grid of toggleable cells. """

    def __init__(self, model: Board, **kwargs):
        super().__init__(**kwargs)

        self.model = model

        self.player = 1

        self.rows = model.height
        self.cols = model.width
        self.spacing = 1

        self.buttons = []

        self.bind(size=self._update_size)

        for r in range(self.rows):
            for c in range(self.cols):
                cell = ToggleCellView(row=r, col=c, value=0)
                cell.bind(on_press=self.update_model)
                self.buttons.append(cell)
                self.add_widget(cell)

    def update_model(self, instance):
        """ Update the underlying model when a cell is toggled. """

        self.model.toggle_cell(instance.row, instance.col, value=self.player)
        instance.update(self.model.data[instance.row, instance.col])

    def update_player(self, player):
        """ Update the player for the board as which the cells are toggled. """

        self.player = player

    def reflect_model(self, *_):
        """ Update the display of the board based on the underlying model. """

        for button in self.buttons:
            button.update(self.model.data[button.row, button.col])

    def _update_size(self, _, __):
        """ Update the size so that the cells are square. """
        # Make cells square
        side = min(self.width / self.cols, self.height / self.rows)
        for child in self.children:
            child.size_hint = (None, None)
            child.width = side
            child.height = side
