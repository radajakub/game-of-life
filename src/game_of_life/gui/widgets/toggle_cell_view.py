from kivy.uix.button import Button

from game_of_life.gui.consts import COLORS


class ToggleCellView(Button):
    def __init__(self, row: int, col: int, value: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.row = row
        self.col = col
        self.background_normal = ''
        self.update(value)

    def update(self, value: int) -> None:
        self.background_color = COLORS[value]
