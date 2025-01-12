from typing import Callable
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from game_of_life.engine.pattern import Pattern
from game_of_life.gui.widgets.cell_view import CellView


class PatternView(BoxLayout):
    def __init__(self, pattern: Pattern, **kwargs):
        super().__init__(**kwargs)
        self.pattern = pattern

        self.orientation = 'vertical'
        self.size_hint = (None, None)
        self.spacing = 1

        self.bind(on_touch_down=self._on_touch_down)

        self.grid = GridLayout(
            rows=pattern.height,
            cols=pattern.width,
            size_hint=(None, None),
            spacing=1,
        )

        for row in range(pattern.height):
            for col in range(pattern.width):
                self.grid.add_widget(CellView(row, col, self.pattern.data[row, col]))

        self.add_widget(self.grid)

        self.grid.bind(height=self._update_grid_size)

    def _on_touch_down(self, instance, touch):
        if self.collide_point(*touch.pos):
            if hasattr(self, 'on_select'):
                self.on_select(self.pattern)
            return True
        return super().on_touch_down(touch)

    def _update_grid_size(self, instance, value):
        if self.grid.parent:
            available_height = self.height - self.label.height
            size = min(available_height, self.width) * 0.8
            self.grid.height = size
            self.grid.width = size

    def bind_on_select(self, callback: Callable):
        self.on_select = callback
