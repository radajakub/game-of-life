from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from game_of_life.engine.board import Board
from game_of_life.engine.pattern import Pattern
from game_of_life.gui.layouts.button_row_layout import ButtonRowLayout
from game_of_life.gui.widgets.centered_button import CenteredButton
from game_of_life.gui.widgets.integer_input import IntegerInput
from game_of_life.gui.layouts.preparation_layout import PreparationLayout
from game_of_life.gui.widgets.board_view import BoardView
from game_of_life.gui.consts import CREATE_PATTERN_SCREEN_LABEL, INTRO_SCREEN_LABEL, LABEL_FONT_SIZE, SIMULATION_SCREEN_LABEL, TITLE_FONT_SIZE
from game_of_life.utils.path_manager import PathManager


class CreatePatternScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.model = Board.new()
        self.layout = PreparationLayout()

        self.grid_view = BoardView(self.model)
        self.layout.grid_container.add_widget(self.grid_view)

        back_button = CenteredButton(
            text="Back",
            size_hint_y=1,
        )
        back_button.bind(on_press=self.go_to_intro_screen)
        self.layout.actions_container.add_widget(back_button)

        name_layout = ButtonRowLayout()
        self.name_input = TextInput(
            hint_text='Pattern Name',
            size_hint_x=0.5,
            size_hint_y=1,
            padding=(10, 5),
            multiline=False,
            font_size=LABEL_FONT_SIZE,
        )
        self.name_input.bind(text=self.check_save_button)
        self.save_button = CenteredButton(
            text='Save',
            size_hint_x=0.3,
            size_hint_y=1,
            disabled=True,
        )
        self.save_button.bind(on_press=self.save_pattern)
        name_layout.add_widget(self.name_input)
        name_layout.add_widget(self.save_button)
        self.layout.actions_container.add_widget(name_layout)

        size_layout = ButtonRowLayout()
        self.size_input = IntegerInput(
            hint_text='Size',
            text='10',
            size_hint_x=0.5,
            size_hint_y=1,
            padding=(10, 5),
            font_size=LABEL_FONT_SIZE,
        )
        size_layout.add_widget(self.size_input)
        self.resize_button = CenteredButton(
            text='Resize',
            size_hint_x=0.3,
            size_hint_y=1,
            disabled=True,
        )
        self.size_input.bind(text=self.check_resize_button)
        self.resize_button.bind(on_press=self.resize_board)
        size_layout.add_widget(self.resize_button)
        self.layout.actions_container.add_widget(size_layout)

        self.test_pattern_button = CenteredButton(
            text='Test Pattern',
            size_hint_y=1,
        )
        self.test_pattern_button.bind(on_press=self.go_to_simulation_screen)
        self.layout.actions_container.add_widget(self.test_pattern_button)

        self.clear_board_button = CenteredButton(
            text='Clear Board',
            size_hint_y=1,
        )
        self.clear_board_button.bind(on_press=self.clear_board)
        self.layout.actions_container.add_widget(self.clear_board_button)

        self.layout.patterns_container.add_widget(
            Label(
                text='Welcome to the Game of Life!',
                font_size=TITLE_FONT_SIZE,
                size_hint_y=0.7
            )
        )

        self.add_widget(self.layout)

    def go_to_intro_screen(self, instance):
        self.reset(instance)
        self.manager.current = INTRO_SCREEN_LABEL

    def resize_board(self, instance):
        dim = int(self.size_input.text)
        self.model.resize(dim, dim)
        self.grid_view = BoardView(self.model)
        self.grid_view.reflect_model()
        self.layout.grid_container.clear_widgets()
        self.layout.grid_container.add_widget(self.grid_view)

    def reset(self, instance):
        self.model = Board.new()
        self.grid_view = BoardView(self.model)
        self.grid_view.reflect_model()
        self.layout.grid_container.clear_widgets()
        self.layout.grid_container.add_widget(self.grid_view)
        self.name_input.text = ''
        self.size_input.text = str(self.model.height)

    def check_save_button(self, instance, value):
        self.save_button.disabled = not value

    def check_resize_button(self, instance, value):
        self.resize_button.disabled = (not value) or (int(value) == self.model.height)

    def save_pattern(self, instance):
        if not self.name_input.text or self.model.count_alive_cells() == 0:
            return

        path_manager = PathManager()
        pattern = Pattern(self.model.data, self.name_input.text)
        pattern.save(path_manager)

        self.reset(instance)

    def clear_board(self, instance):
        self.model.clear()
        self.grid_view.reflect_model()
        self.name_input.text = ''
        self.size_input.text = str(self.model.height)

    def go_to_simulation_screen(self, instance):
        # prepare data
        simulation_screen = self.manager.get_screen(SIMULATION_SCREEN_LABEL)
        simulation_screen.init_data(board=self.model.copy(), back_label=CREATE_PATTERN_SCREEN_LABEL)

        self.manager.current = SIMULATION_SCREEN_LABEL
