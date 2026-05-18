import os
os.environ["KIVY_NO_ENV_CONFIG"] = "1"

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

# Importar pantallas
from screens.home_screen import HomeScreen
from screens.course_detail_screen import CourseDetailScreen
from screens.community_screen import CommunityScreen
from screens.profile_screen import ProfileScreen
from screens.courses_screen import CoursesScreen
from screens.login_screen import LoginScreen

# Simular tamaño de celular en escritorio
Window.size = (400, 750)

KV = """
<RootScreenManager>:
    LoginScreen:
        name: "login"
    HomeScreen:
        name: "home"
    CoursesScreen:
        name: "courses"
    CourseDetailScreen:
        name: "course_detail"
    CommunityScreen:
        name: "community"
    ProfileScreen:
        name: "profile"
"""

Builder.load_string(KV)


class RootScreenManager(MDScreenManager):
    pass


class AprendeTeqApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.primary_hue = "600"
        self.theme_cls.accent_palette = "Amber"
        self.theme_cls.accent_hue = "600"
        self.theme_cls.theme_style = "Light"
        self.title = "AprendeTeq"

        sm = RootScreenManager()
        return sm

    def on_start(self):
        # Al iniciar, ir a login (o home si ya está autenticado)
        self.root.current = "login"


if __name__ == "__main__":
    AprendeTeqApp().run()
