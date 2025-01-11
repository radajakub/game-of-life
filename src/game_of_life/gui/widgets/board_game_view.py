from kivy.uix.gridlayout import GridLayout

from game_of_life.engine.board import Board
from game_of_life.gui.widgets.cell_view import CellView


class BoardGameView(GridLayout):
    def __init__(self, model: Board, **kwargs):
        super().__init__(**kwargs)

        self.rows = model.height
        self.cols = model.width

        self.size_hint = (1, 1)
        self.spacing = 1
        self.cells = []

        for r in range(model.height):
            for c in range(model.width):
                cell = CellView(row=r, col=c, value=model.data[r, c])
                self.cells.append(cell)
                self.add_widget(cell)

    def reflect_model(self, model: Board):
        for cell in self.cells:
            cell.update(model.data[cell.row, cell.col])
