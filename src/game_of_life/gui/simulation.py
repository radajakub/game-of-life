""" Module for the simulation screen. """

from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from game_of_life.config import DEFAULT_FREQUENCY, DEFAULT_STEPS
from game_of_life.engine.board import Board
from game_of_life.engine.game import Game
from game_of_life.gui.consts import LABEL_FONT_SIZE, SIMULATION_FINISHED, SIMULATION_INITIALIZED, SIMULATION_PAUSED, SIMULATION_RUNNING
from game_of_life.gui.layouts.button_row_layout import ButtonRowLayout
from game_of_life.gui.layouts.split_layout import SplitLayout
from game_of_life.gui.widgets.board_game_view import BoardGameView
from game_of_life.gui.widgets.centered_button import CenteredButton
from game_of_life.gui.widgets.slider_input import SliderInput


class SimulationScreen(Screen):
    """
    Class handling the Game of Life simulation screen.
    In this case, the board is not interactive, it is controlled only by the action buttons.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.back_label = None
        self.board = None
        self.game_model = None
        self.board_view = None

        self.layout = SplitLayout()

        self.back_button = CenteredButton(
            text="Back",
            size_hint_y=1,
        )
        self.back_button.bind(on_press=self.go_back)
        self.layout.actions_container.add_widget(self.back_button)

        steps_layout = ButtonRowLayout()
        self.previous_step_button = CenteredButton(
            text="Prev step",
            size_hint_y=1,
            disabled=True,
        )
        self.previous_step_button.bind(on_press=self.previous_step)
        steps_layout.add_widget(self.previous_step_button)
        self.next_step_button = CenteredButton(
            text="Next step",
            size_hint_y=1,
        )
        self.next_step_button.bind(on_press=self.next_step)
        steps_layout.add_widget(self.next_step_button)
        self.layout.actions_container.add_widget(steps_layout)

        self.frequency_setter = SliderInput(
            label='Frequency',
            low=1,
            high=100,
            step=1,
            initial_value=DEFAULT_FREQUENCY,
            update_function=self.update_frequency,
        )
        self.layout.actions_container.add_widget(self.frequency_setter)

        self.steps_setter = SliderInput(
            label='Steps',
            low=10,
            high=1000,
            step=10,
            initial_value=DEFAULT_STEPS,
            update_function=self.update_steps,
        )
        self.layout.actions_container.add_widget(self.steps_setter)

        self.run_button = CenteredButton(
            text='Run',
            size_hint_y=1,
        )
        self.run_button.bind(on_press=self.run)
        self.layout.actions_container.add_widget(self.run_button)

        self.restart_button = CenteredButton(
            text='Restart',
            size_hint_y=1,
        )
        self.restart_button.bind(on_press=self.restart)
        self.layout.actions_container.add_widget(self.restart_button)

        self.status_label = Label(
            text=SIMULATION_INITIALIZED,
            font_size=LABEL_FONT_SIZE,
        )
        self.layout.actions_container.add_widget(self.status_label)

        self.add_widget(self.layout)

    def init_data(self, board: Board, back_label: str):
        """
        Method to initialize the data for the simulation when coming from another screen.

        Args:
            board: the board to use for the simulation
            back_label: the label of the screen to go back to
        """

        self.back_label = back_label
        self.board = board
        self.game_model = Game(board=self.board)
        self.board_view = BoardGameView(model=self.board)
        self.layout.grid_container.add_widget(self.board_view)
        self.status_label.text = SIMULATION_INITIALIZED

    def reset(self, _):
        """ Reset the simulation screen to not contain information from the last run. """

        self.previous_step_button.disabled = True
        self.layout.grid_container.clear_widgets()
        self.frequency_setter.slider.value = DEFAULT_FREQUENCY
        self.steps_setter.slider.value = DEFAULT_STEPS
        self.status_label.text = SIMULATION_INITIALIZED
        self.board = None
        self.game_model = None

    def restart(self, _):
        """ Restart the simulation to be in the initial state. """

        self.game_model.restart()
        self.board_view.reflect_model(self.game_model.board)
        self.toggle_buttons(disabled=False)
        self.check_step_buttons()
        self.status_label.text = SIMULATION_INITIALIZED

    def toggle_buttons(self, disabled: bool):
        """ Toggle the buttons to be disabled or enabled during the simulation. """

        self.back_button.disabled = disabled
        self.previous_step_button.disabled = disabled
        self.next_step_button.disabled = disabled
        self.run_button.disabled = disabled
        self.restart_button.disabled = disabled
        self.frequency_setter.slider.disabled = disabled
        self.steps_setter.slider.disabled = disabled

    def format_status(self, status: str):
        """ Format the status label to display the current step and total steps. """

        return f'{status} ({self.game_model.i}/{self.game_model.steps})'

    def run(self, _):
        """ Run the simulation using the Kivy Clock. """

        self.status_label.text = self.format_status(SIMULATION_RUNNING)
        self.toggle_buttons(disabled=True)

        Clock.schedule_interval(self._run_step, self.game_model.time_delay)

    def _run_step(self, _):
        """ Run a single step inside the Clock schedule function. """
        output = self.game_model.run_step()
        self.board_view.reflect_model(self.game_model.board)
        self.status_label.text = self.format_status(SIMULATION_RUNNING)

        if not output:
            self.restart_button.disabled = False
            self.status_label.text = self.format_status(SIMULATION_FINISHED)

        return output

    def _update_left_column_width(self, instance, value):
        """ Update the width of the left column to be the same as its height. """
        instance.width = value

    def go_back(self, instance):
        """ Go back to the previous screen set in the init_data method. """

        if self.back_label:
            self.reset(instance)
            self.manager.current = self.back_label

    def check_step_buttons(self):
        """ Check if the prev/next step buttons should be disabled. """

        self.previous_step_button.disabled = not self.game_model.can_go_previous()
        self.next_step_button.disabled = not self.game_model.can_go_next()

        if self.next_step_button.disabled:
            self.status_label.text = self.format_status(SIMULATION_FINISHED)
        else:
            self.status_label.text = self.format_status(SIMULATION_PAUSED)

    def previous_step(self, _):
        """ Go to the previous step of the simulation. """

        if not self.game_model.can_go_previous():
            return
        self.game_model.previous_step()
        self.board_view.reflect_model(self.game_model.board)

        self.status_label.text = self.format_status(SIMULATION_PAUSED)
        self.check_step_buttons()

    def next_step(self, _):
        """ Go to the next step of the simulation (evolve board once). """

        if not self.game_model.can_go_next():
            return
        self.game_model.next_step()
        self.board_view.reflect_model(self.game_model.board)
        self.status_label.text = self.format_status(SIMULATION_PAUSED)

        self.check_step_buttons()

    def update_frequency(self, _, value):
        """ Update the frequency of the simulation. """

        self.game_model.set_frequency(value)

    def update_steps(self, _, value):
        """ Update the number of steps to run the simulation for. """

        self.game_model.set_steps(value)
