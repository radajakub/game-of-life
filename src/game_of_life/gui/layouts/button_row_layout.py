""" Module for a layout putting buttons (and other widgets) in a row """

from kivy.uix.boxlayout import BoxLayout


class ButtonRowLayout(BoxLayout):
    """
    Layout for a row of buttons.
    """

    def __init__(self, **kwargs):
        """
        Initialize the button row layout.
        """

        self.orientation = 'horizontal'
        self.size_hint_y = 1
        self.spacing = 50
        self.padding = (10, 10)

        super().__init__(**kwargs)
