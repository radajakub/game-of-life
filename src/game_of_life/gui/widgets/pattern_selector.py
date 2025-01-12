""" Module for inspecting and modifying patterns. """

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

from game_of_life.engine.pattern import Pattern
from game_of_life.gui.consts import LABEL_FONT_SIZE
from game_of_life.gui.widgets.cell_view import CellView


class PatternSelector(BoxLayout):
    """
    Handles the detailed view of a pattern with a name and action buttons.
    The actions include rotations and reflections.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.player = 1

        self.label = Label(
            text='Selected Pattern',
            font_size=LABEL_FONT_SIZE,
            size_hint_y=0.1,
        )
        self.actions1_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1
        )
        self.left_button = Button(
            text='Rot. left',
            font_size='10sp',
            disabled=True,
        )
        self.left_button.bind(on_press=self.rotate_left)
        self.right_button = Button(
            text='Rot. right',
            font_size='10sp',
            disabled=True,
        )
        self.right_button.bind(on_press=self.rotate_right)
        self.clear_button = Button(
            text='Unselect',
            font_size='10sp',
            disabled=True,
        )
        self.clear_button.bind(on_press=self.reset)
        self.actions1_container.add_widget(self.left_button)
        self.actions1_container.add_widget(self.right_button)
        self.actions1_container.add_widget(self.clear_button)

        self.actions2_container = BoxLayout(
            orientation='horizontal',
            size_hint_y=0.1
        )
        self.flip_horizontal_button = Button(
            text='Flip horizontal',
            font_size='10sp',
            disabled=True,
        )
        self.flip_horizontal_button.bind(on_press=self.flip_horizontal)
        self.flip_vertical_button = Button(
            text='Flip vertical',
            font_size='10sp',
            disabled=True,
        )
        self.flip_vertical_button.bind(on_press=self.flip_vertical)
        self.flip_diagonal_button = Button(
            text='Flip diagonal',
            font_size='10sp',
            disabled=True,
        )
        self.flip_diagonal_button.bind(on_press=self.flip_diagonal)
        self.actions2_container.add_widget(self.flip_horizontal_button)
        self.actions2_container.add_widget(self.flip_vertical_button)
        self.actions2_container.add_widget(self.flip_diagonal_button)

        self.content_container = BoxLayout(
            size_hint_y=0.7,
            size_hint_x=0.8,
            padding=(20, 20),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )

        self.grid = GridLayout(
            rows=5,
            cols=5,
            size_hint=(1, 1),
            spacing=1,
        )
        for row in range(5):
            for col in range(5):
                self.grid.add_widget(CellView(row, col, 0))

        self.content_container.add_widget(self.grid)

        self.add_widget(self.label)
        self.add_widget(self.actions1_container)
        self.add_widget(self.actions2_container)
        self.add_widget(self.content_container)

        self.current_pattern = None

    def reset(self, _):
        """ Reset the pattern selector to the initial empty state. """
        self.current_pattern = None
        self.player = 1

        self.grid = GridLayout(
            rows=5,
            cols=5,
            size_hint=(1, 1),
            spacing=1,
        )
        for row in range(5):
            for col in range(5):
                self.grid.add_widget(CellView(row, col, 0))

        self.label.text = 'Selected Pattern'
        self.content_container.clear_widgets()
        self.content_container.add_widget(self.grid)
        self.update_buttons()

    def rotate_left(self, _):
        """ Rotate the pattern left action. """

        self.current_pattern.rotate_counterclockwise()
        self.set_pattern(self.current_pattern, self.player)

    def rotate_right(self, _):
        """ Rotate the pattern right action. """

        self.current_pattern.rotate_clockwise()
        self.set_pattern(self.current_pattern, self.player)

    def flip_horizontal(self, _):
        """ Flip the pattern horizontally action. """

        self.current_pattern.reflect_horizontal()
        self.set_pattern(self.current_pattern, self.player)

    def flip_vertical(self, _):
        """ Flip the pattern vertically action. """

        self.current_pattern.reflect_vertical()
        self.set_pattern(self.current_pattern, self.player)

    def flip_diagonal(self, _):
        """ Flip the pattern diagonally action. """

        self.current_pattern.reflect_diagonal()
        self.set_pattern(self.current_pattern, self.player)

    def set_player(self, player: int):
        """
        Set the player for the pattern.

        Args:
            player: the player to set the pattern for
        """

        if self.current_pattern is not None:
            self.set_pattern(self.current_pattern, player)

    def set_pattern(self, pattern: Pattern, player: int):
        """
        Set the pattern and update the widget to display it with the correct player.

        Args:
            pattern: the pattern to set
            player: the player to set the pattern for
        """

        self.player = player
        self.current_pattern = pattern

        self.grid = GridLayout(
            rows=pattern.height,
            cols=pattern.width,
            size_hint=(1, 1),
            spacing=1,
        )

        for row in range(pattern.height):
            for col in range(pattern.width):
                self.grid.add_widget(CellView(row, col, self.current_pattern.data[row, col] * player))

        self.label.text = pattern.name

        self.content_container.clear_widgets()
        self.content_container.add_widget(self.grid)
        self.update_buttons()

    def update_buttons(self):
        """
        Update the disabled state of the buttons based on the current pattern.
        The user should not be able to rotate or flip an empty pattern.
        """

        val = self.current_pattern is None
        self.left_button.disabled = val
        self.right_button.disabled = val
        self.clear_button.disabled = val
        self.flip_horizontal_button.disabled = val
        self.flip_vertical_button.disabled = val
        self.flip_diagonal_button.disabled = val
