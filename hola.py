from kivymd.app import MDApp
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.screen import MDScreen
from kivy.uix.floatlayout import FloatLayout


class MyApp(MDApp):
    def build(self):
        screen = MDScreen()
        layout = FloatLayout()

        button = MDRectangleFlatButton(
            text="Hola, mundo!",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
        )

        layout.add_widget(button)
        screen.add_widget(layout)

        return screen


if __name__ == "__main__":
    MyApp().run()