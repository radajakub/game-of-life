from kivy.uix.button import Button


class ToggleCellView(Button):
    def __init__(self, row: int, col: int, value: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.row = row
        self.col = col
        self.background_normal = ''
        self.update(value)

    def update(self, value: int) -> None:
        self.background_color = (0.2, 0.6, 1, 1) if value else (0.2, 0.2, 0.2, 1)
