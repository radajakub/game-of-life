from kivy.uix.boxlayout import BoxLayout


class ButtonRowLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'horizontal'
        self.size_hint_y = 1
        self.spacing = 50
        self.padding = (10, 10)
