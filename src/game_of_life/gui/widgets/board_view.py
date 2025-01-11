from kivy.uix.gridlayout import GridLayout

from game_of_life.engine.board import Board
from game_of_life.gui.widgets.toggle_cell_view import ToggleCellView


class BoardView(GridLayout):
    def __init__(self, model: Board, **kwargs):
        super().__init__(**kwargs)

        self.model = model
        self.rows = model.height
        self.cols = model.width
        self.spacing = 1

        self.buttons = []

        self.bind(size=self._update_size)

        for r in range(self.rows):
            for c in range(self.cols):
                cell = ToggleCellView(row=r, col=c)
                cell.bind(on_press=self.update_model)
                self.buttons.append(cell)
                self.add_widget(cell)

    def update_model(self, instance):
        self.model.toggle_cell(instance.row, instance.col)
        instance.update(self.model.data[instance.row, instance.col])

    def reflect_model(self, *args):
        for button in self.buttons:
            button.update(self.model.data[button.row, button.col])

    def _update_size(self, instance, value):
        # Make cells square
        side = min(self.width / self.cols, self.height / self.rows)
        for child in self.children:
            child.size_hint = (None, None)
            child.width = side
            child.height = side
