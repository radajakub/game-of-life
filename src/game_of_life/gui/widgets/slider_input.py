from typing import Callable
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label


class SliderInput(BoxLayout):
    def __init__(self, label: str, min: int, max: int, step: int, initial_value: int, update_function: Callable, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'
        self.size_hint_x = 1
        self.update_function = update_function

        self.label = Label(text=label)
        self.slider_row = BoxLayout(
            orientation='horizontal',
            size_hint_x=1,
            spacing=5,
        )
        self.slider = Slider(
            min=min,
            max=max,
            value=initial_value,
            step=step,
            cursor_size=(50, 50),
            size_hint_x=0.8,
        )
        self.slider.bind(value=self.update)
        self.slider_row.add_widget(self.slider)
        self.slider_value_label = Label(text=str(initial_value), size_hint_x=0.2)
        self.slider_row.add_widget(self.slider_value_label)
        self.add_widget(self.label)
        self.add_widget(self.slider_row)

    def update(self, instance, value):
        self.slider_value_label.text = str(value)
        self.update_function(instance, value)
