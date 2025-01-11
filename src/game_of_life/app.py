from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, NoTransition

from game_of_life.gui.intro import IntroScreen
from game_of_life.gui.create_pattern import CreatePatternScreen
from game_of_life.gui.consts import INTRO_SCREEN_LABEL, CREATE_PATTERN_SCREEN_LABEL, SIMULATION_SCREEN_LABEL
from game_of_life.gui.simulation import SimulationScreen


class GameOfLifeApp(App):
    def build(self):
        Window.size = (1200, 800)
        Window.minimum_width = 600
        Window.minimum_height = 400

        sm = ScreenManager(transition=NoTransition())

        sm.add_widget(IntroScreen(name=INTRO_SCREEN_LABEL))
        sm.add_widget(CreatePatternScreen(name=CREATE_PATTERN_SCREEN_LABEL))
        sm.add_widget(SimulationScreen(name=SIMULATION_SCREEN_LABEL))

        return sm


if __name__ == "__main__":
    GameOfLifeApp().run()
