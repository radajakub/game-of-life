from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from game_of_life.engine.board import Board
from game_of_life.engine.pattern import Pattern, load_all_patterns
from game_of_life.gui.layouts.button_row_layout import ButtonRowLayout
from game_of_life.gui.widgets.centered_button import CenteredButton
from game_of_life.gui.widgets.integer_input import IntegerInput
from game_of_life.gui.layouts.preparation_layout import PreparationLayout
from game_of_life.gui.widgets.board_view import BoardView
from game_of_life.gui.consts import CREATE_PATTERN_SCREEN_LABEL, INTRO_SCREEN_LABEL, LABEL_FONT_SIZE, SIMULATION_SCREEN_LABEL
from game_of_life.gui.widgets.pattern_view import PatternView
from game_of_life.utils.path_manager import PathManager


class CreatePatternScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.path_manager = PathManager()

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
        self.resize_button.bind(on_press=self.resize_board_from_input)
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

        self.update_pattern_lib()

        self.add_widget(self.layout)

    def update_pattern_lib(self):
        self.layout.patterns_container.clear_widgets()
        self.patterns = load_all_patterns(self.path_manager)
        for pattern in self.patterns:
            pattern_view = PatternView(pattern)
            pattern_view.bind_on_select(self.on_pattern_view_click)
            self.layout.patterns_container.add_widget(pattern_view)

    def on_pattern_view_click(self, pattern: Pattern):
        self.model.clear()

        if pattern.height > self.model.height or pattern.width > self.model.width:
            larger_size = max(pattern.height, pattern.width)
            self.resize_board(larger_size)

        y0 = (self.model.height - pattern.height) // 2
        x0 = (self.model.width - pattern.width) // 2
        self.model.place_pattern(pattern, x0, y0)
        self.grid_view.reflect_model()

    def go_to_intro_screen(self, instance):
        self.reset(instance)
        self.manager.current = INTRO_SCREEN_LABEL

    def resize_board(self, new_size: int):
        self.model.resize(new_size, new_size)
        self.grid_view = BoardView(self.model)
        self.grid_view.reflect_model()
        self.layout.grid_container.clear_widgets()
        self.layout.grid_container.add_widget(self.grid_view)

    def resize_board_from_input(self, instance):
        dim = int(self.size_input.text)
        self.resize_board(dim)

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
        pattern = Pattern.new(self.model.data, self.name_input.text)
        pattern.save(path_manager)

        self.reset(instance)
        self.update_pattern_lib()

    def clear_board(self, instance):
        self.model.clear()
        self.grid_view.reflect_model()
        self.name_input.text = ''
        self.size_input.text = str(self.model.height)

    def go_to_simulation_screen(self, instance):
        if self.model.count_alive_cells() == 0:
            return

        # prepare data
        simulation_screen = self.manager.get_screen(SIMULATION_SCREEN_LABEL)
        simulation_screen.init_data(board=self.model.copy(), back_label=CREATE_PATTERN_SCREEN_LABEL)

        self.manager.current = SIMULATION_SCREEN_LABEL
