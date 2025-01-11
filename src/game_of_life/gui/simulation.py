from kivy.clock import Clock
from kivy.uix.screenmanager import Screen

from game_of_life.config import DEFAULT_FREQUENCY, DEFAULT_STEPS
from game_of_life.engine.board import Board
from game_of_life.engine.game import Game
from game_of_life.gui.layouts.button_row_layout import ButtonRowLayout
from game_of_life.gui.layouts.split_layout import SplitLayout
from game_of_life.gui.widgets.board_game_view import BoardGameView
from game_of_life.gui.widgets.centered_button import CenteredButton
from game_of_life.gui.widgets.slider_input import SliderInput


class SimulationScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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
            min=1,
            max=100,
            step=1,
            initial_value=DEFAULT_FREQUENCY,
            update_function=self.update_frequency,
        )
        self.layout.actions_container.add_widget(self.frequency_setter)

        self.steps_setter = SliderInput(
            label='Steps',
            min=10,
            max=1000,
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

        # TODO: add status label

        self.add_widget(self.layout)

    def init_data(self, board: Board, back_label: str):
        # where to go back on back button
        self.back_label = back_label
        self.board = board
        self.game_model = Game(board=self.board)
        self.board_view = BoardGameView(model=self.board)
        self.layout.grid_container.add_widget(self.board_view)

    def reset(self, instance):
        self.back_label = None
        self.board = None
        self.game_model = None
        self.previous_step_button.disabled = True
        self.layout.grid_container.clear_widgets()
        self.frequency_setter.slider.value = DEFAULT_FREQUENCY
        self.steps_setter.slider.value = DEFAULT_STEPS

    def restart(self, instance):
        self.game_model.restart()
        self.board_view.reflect_model(self.game_model.board)
        self.check_step_buttons()
        # todo: undisable some buttons?

    def toggle_buttons(self, enabled: bool):
        # todo
        pass

    def run(self, instance):
        self.toggle_buttons(False)
        Clock.schedule_interval(self._run_step, self.game_model.time_delay)
        # todo: do not toggle next button and maybe more
        self.toggle_buttons(True)

    def _run_step(self, dt):
        output = self.game_model.run_step()
        self.board_view.reflect_model(self.game_model.board)
        return output

    def _update_left_column_width(self, instance, value):
        instance.width = value

    def go_back(self, instance):
        if self.back_label:
            self.manager.current = self.back_label
            self.reset(instance)

    def check_step_buttons(self):
        self.previous_step_button.disabled = not self.game_model.can_go_previous()
        self.next_step_button.disabled = not self.game_model.can_go_next()

    def previous_step(self, instance):
        if not self.game_model.can_go_previous():
            return
        self.game_model.previous_step()
        self.board_view.reflect_model(self.game_model.board)

        self.check_step_buttons()

    def update_frequency(self, instance, value):
        self.game_model.set_frequency(value)

    def update_steps(self, instance, value):
        self.game_model.set_steps(value)

    def next_step(self, instance):
        if not self.game_model.can_go_next():
            return
        self.game_model.next_step()
        self.board_view.reflect_model(self.game_model.board)

        self.check_step_buttons()
