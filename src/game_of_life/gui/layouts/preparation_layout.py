from kivy.uix.boxlayout import BoxLayout

from game_of_life.gui.config import BASE_PADDING


class PreparationLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.padding = BASE_PADDING
        self.spacing = 1

        top_row = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.9,
            size_hint_x=1,
        )
        self.add_widget(top_row)

        self.grid_container = BoxLayout(
            orientation='vertical',
            size_hint_x=None,
        )
        self.grid_container.bind(height=self._update_grid_container_width)
        top_row.add_widget(self.grid_container)

        self.actions_container = BoxLayout(
            orientation='vertical',
            padding=BASE_PADDING,
            size_hint_y=1,
            size_hint_x=0.2,
            spacing=50,
        )
        top_row.add_widget(self.actions_container)

        self.patterns_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1,
            size_hint_x=1,
            spacing=1,
        )
        self.add_widget(self.patterns_container)

    def _update_grid_container_width(self, instance, value):
        # Make left column width equal to its height to maintain square shape
        instance.width = value
