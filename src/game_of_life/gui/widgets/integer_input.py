""" Module for the integer input widget. """

import re
from kivy.uix.textinput import TextInput


class IntegerInput(TextInput):
    """ Integer input widget is used to enforce only integer input in a text field. """

    def __init__(self, max_digits: int = 4, **kwargs):
        super().__init__(**kwargs)

        self.max_digits = max_digits

        self.pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        """ Insert text into the text input if it compiles with the pattern. """

        s = re.sub(self.pat, '', substring)
        if len(self.text) + len(s) <= self.max_digits:
            return super().insert_text(s, from_undo=from_undo)
        return ''
