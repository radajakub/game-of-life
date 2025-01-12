""" Module for the centered button widget. """

from kivy.uix.button import Button

from game_of_life.gui.consts import LABEL_FONT_SIZE


class CenteredButton(Button):
    """ Centered button widget is used to display a button in the center of the parent widget. """

    def __init__(self, **kwargs):
        self.font_size = LABEL_FONT_SIZE
        self.pos_hint = {'center_x': 0.5}
        self.size_hint_x = 0.5
        self.size_hint_y = 0.1

        self.bind(texture_size=self.setter('size'))

        super().__init__(**kwargs)
