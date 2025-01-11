from kivy.uix.boxlayout import BoxLayout

from game_of_life.gui.consts import BASE_PADDING


class SplitLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'horizontal'
        self.padding = BASE_PADDING
        self.spacing = 1

        self.grid_container = BoxLayout(
            orientation='vertical',
            size_hint_x=None,
            size_hint_y=1,
        )

        self.grid_container.bind(height=self._update_grid_container_width)
        self.add_widget(self.grid_container)

        self.actions_container = BoxLayout(
            orientation='vertical',
            padding=BASE_PADDING,
            size_hint_x=0.2,
            size_hint_y=1,
            spacing=50,
        )
        self.add_widget(self.actions_container)

    def _update_grid_container_width(self, instance, value):
        # Make left column width equal to its height to maintain square shape
        instance.width = value
