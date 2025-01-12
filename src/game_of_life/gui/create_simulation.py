""" Module for the create simulation screen. """

from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from game_of_life.engine.board import Board
from game_of_life.engine.pattern import Pattern, load_all_patterns
from game_of_life.gui.layouts.button_row_layout import ButtonRowLayout
from game_of_life.gui.widgets.cell_view import CellView
from game_of_life.gui.widgets.centered_button import CenteredButton
from game_of_life.gui.widgets.integer_input import IntegerInput
from game_of_life.gui.layouts.preparation_layout import PreparationLayout
from game_of_life.gui.widgets.board_view import BoardView
from game_of_life.gui.consts import COLORS, CREATE_SIMULATION_SCREEN_LABEL, INTRO_SCREEN_LABEL, LABEL_FONT_SIZE, SIMULATION_SCREEN_LABEL
from game_of_life.gui.widgets.pattern_selector import PatternSelector
from game_of_life.gui.widgets.pattern_view import PatternView
from game_of_life.utils.path_manager import PathManager


class CreateSimulationScreen(Screen):
    """
    Screen for setting up and creating a new simulation even for multiple players.
    The board is interactive, the user can click and set alive cells for arbitrary player.
    The user can also select a pattern to display and reuse in the simulation.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.path_manager = PathManager()

        self.model = Board.new()
        self.player = 1

        self.layout = PreparationLayout()

        self.grid_view = BoardView(self.model)
        self.layout.grid_container.add_widget(self.grid_view)

        run_button_row = ButtonRowLayout(size_hint_y=0.1)
        back_button = CenteredButton(
            text="Back",
            size_hint_y=1,
            size_hint_x=0.3
        )
        back_button.bind(on_press=self.go_to_intro_screen)
        run_button_row.add_widget(back_button)
        self.start_simulation_button = CenteredButton(
            text='Start Simulation',
            size_hint_y=1,
            size_hint_x=0.4
        )
        self.start_simulation_button.bind(on_press=self.go_to_simulation_screen)
        run_button_row.add_widget(self.start_simulation_button)
        self.clear_board_button = CenteredButton(
            text='Clear Board',
            size_hint_y=1,
            size_hint_x=0.3
        )
        self.clear_board_button.bind(on_press=self.clear_board)
        run_button_row.add_widget(self.clear_board_button)
        self.layout.actions_container.add_widget(run_button_row)

        player_layout = ButtonRowLayout(size_hint_y=0.1)
        player_label = Label(
            text='Player: ',
            font_size=LABEL_FONT_SIZE,
        )
        prev_player_button = CenteredButton(
            text='<',
            size_hint_x=0.1,
            size_hint_y=1,
        )
        prev_player_button.bind(on_press=self.get_prev_player)
        next_player_button = CenteredButton(
            text='>',
            size_hint_x=0.1,
            size_hint_y=1,
        )
        next_player_button.bind(on_press=self.get_next_player)
        self.player_indicator = CellView(0, 0, self.player)
        self.player_indicator.size_hint = (0.4, 1)

        player_layout.add_widget(player_label)
        player_layout.add_widget(prev_player_button)
        player_layout.add_widget(self.player_indicator)
        player_layout.add_widget(next_player_button)
        self.layout.actions_container.add_widget(player_layout)

        size_layout = ButtonRowLayout(size_hint_y=0.1)
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

        self.pattern_selector = PatternSelector(size_hint_y=0.7)
        self.layout.actions_container.add_widget(self.pattern_selector)

        self.update_pattern_lib()

        self.add_widget(self.layout)

    def get_next_player(self, _):
        """ In player switcher, select the next player in the sequence. """

        self.player += 1

        if self.player >= len(COLORS):
            self.player = 1
        self.player_indicator.update(self.player)
        self.grid_view.update_player(self.player)
        self.pattern_selector.set_player(self.player)

    def get_prev_player(self, _):
        """ In player switcher, select the previous player in the sequence. """

        self.player -= 1

        if self.player < 1:
            self.player = len(COLORS) - 1
        self.player_indicator.update(self.player)
        self.grid_view.update_player(self.player)
        self.pattern_selector.set_player(self.player)

    def update_pattern_lib(self):
        """ Load all patterns from the patterns folder and display them. """
        self.layout.patterns_container.clear_widgets()
        self.patterns = load_all_patterns(self.path_manager)
        for pattern in self.patterns:
            pattern_view = PatternView(pattern)
            pattern_view.bind_on_select(self.on_pattern_view_click)
            self.layout.patterns_container.add_widget(pattern_view)

    def on_pattern_view_click(self, pattern: Pattern):
        """
        Select pattern for a detailed view.

        Args:
            pattern: the pattern to show detail of
        """

        self.pattern_selector.set_pattern(pattern, self.player)

    def go_to_intro_screen(self, instance):
        """ Go back to the intro screen. """

        self.reset(instance)
        self.manager.current = INTRO_SCREEN_LABEL

    def resize_board(self, new_size: int):
        """
        Resize the board to the new size

        Args:
            new_size: the new size of the board
        """

        self.model.resize(new_size, new_size)
        self.grid_view = BoardView(self.model)
        self.grid_view.reflect_model()
        self.layout.grid_container.clear_widgets()
        self.layout.grid_container.add_widget(self.grid_view)

    def resize_board_from_input(self, _):
        """ Resize the board to the new size from the input field. """

        dim = int(self.size_input.text)
        self.resize_board(dim)

    def reset(self, _):
        """ Reset the grid and all the fields so that they do not contain information from the last run. """

        self.model = Board.new()
        self.grid_view = BoardView(self.model)
        self.grid_view.reflect_model()
        self.layout.grid_container.clear_widgets()
        self.layout.grid_container.add_widget(self.grid_view)
        self.size_input.text = str(self.model.height)
        self.player = 1
        self.player_indicator.update(self.player)

    def check_resize_button(self, _, value):
        """ Check if the resize button should be disabled. """

        self.resize_button.disabled = (not value) or (int(value) == self.model.height)

    def clear_board(self, _):
        """ Clear the board so that the user can start from scratch. """

        self.model.clear()
        self.grid_view.reflect_model()
        self.size_input.text = str(self.model.height)

    def go_to_simulation_screen(self, _):
        """
        Go to the simulation screen if there are alive cells on the board.
        Function also prepares and sends data for the simulation screen.
        """

        if self.model.count_alive_cells() == 0:
            return

        # prepare data
        simulation_screen = self.manager.get_screen(SIMULATION_SCREEN_LABEL)
        simulation_screen.init_data(board=self.model.copy(), back_label=CREATE_SIMULATION_SCREEN_LABEL)

        self.manager.current = SIMULATION_SCREEN_LABEL
