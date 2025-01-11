from kivy.uix.gridlayout import GridLayout

from game_of_life.engine.pattern import Pattern


class PatternView(GridLayout):
    def __init__(self, pattern: Pattern, **kwargs):
        super().__init__(**kwargs)
        self.pattern = pattern
        self.rows = pattern.height
        self.cols = pattern.width
        self.buttons = []
        self.spacing = 1
