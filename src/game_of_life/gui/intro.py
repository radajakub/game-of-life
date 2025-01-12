from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label

from game_of_life.gui.widgets.centered_button import CenteredButton
from game_of_life.gui.consts import BASE_PADDING, CREATE_SIMULATION_SCREEN_LABEL, TITLE_FONT_SIZE, CREATE_PATTERN_SCREEN_LABEL


class IntroScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        layout = BoxLayout(
            orientation='vertical',
            padding=BASE_PADDING,
            spacing=10,
        )

        # Create the counter label
        title = Label(
            text='Welcome to the Game of Life!',
            font_size=TITLE_FONT_SIZE,
            size_hint_y=0.7
        )
        layout.add_widget(title)

        pattern_button = CenteredButton(text='Patterns')
        pattern_button.bind(on_press=self.go_to_pattern_screen)
        layout.add_widget(pattern_button)

        simulation_button = CenteredButton(text='Simulation')
        simulation_button.bind(on_press=self.go_to_prepare_simulation_screen)
        layout.add_widget(simulation_button)

        end_button = CenteredButton(text='End')
        end_button.bind(on_press=self.end_app)
        layout.add_widget(end_button)

        self.add_widget(layout)

    def go_to_pattern_screen(self, _):
        self.manager.current = CREATE_PATTERN_SCREEN_LABEL

    def go_to_prepare_simulation_screen(self, _):
        self.manager.current = CREATE_SIMULATION_SCREEN_LABEL

    def end_app(self, _):
        App.get_running_app().stop()
