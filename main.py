"""
main.py  -  Tequixquiac Educa
Ejecutar:  python main.py
"""
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.card import MDCard
from kivy.clock import Clock
import os, sys

sys.path.insert(0, os.path.dirname(__file__))
from database.db_manager import (
    inicializar_db, autenticar_usuario, registrar_usuario,
    registrar_sesion, cerrar_sesion,
    listar_cursos, obtener_curso, listar_lecciones,
    inscribir_estudiante, esta_inscrito, mis_cursos,
    marcar_leccion_completada, progreso_curso,
    lecciones_completadas, estadisticas_estudiante,
    mis_notificaciones, enviar_notificacion,
)

Window.size = (390, 844)
# ─── FUENTE PERSONALIZADA ────────────────────────────────────
LabelBase.register(
    name="Poppins",
    fn_regular="fonts/Poppins-Regular.ttf"
)

# ─── NUEVA PALETA MODERNA ────────────────────────────────────
BG_DARK        = "#121826"
BG_SURFACE     = "#1F2937"
ACCENT_TEAL    = "#8B5CF6"
ACCENT_AMBER   = "#F472B6"
TEXT_PRIMARY   = "#FFFFFF"      # Texto blanco
TEXT_SECONDARY = "#C7C7D1"      # Texto gris claro

COLORES = [
    "#8B5CF6",
    "#EC4899",
    "#06B6D4",
    "#10B981",
    "#F59E0B",
    "#F43F5E"
]

def _hex_to_rgba(h):
    h = h.lstrip('#')
    return [int(h[i:i+2], 16)/255 for i in (0, 2, 4)] + [1]

def _r(h): return ", ".join(str(round(v,4)) for v in _hex_to_rgba(h))

C = {k: _r(v) for k, v in {
    "bg": BG_DARK, "surf": BG_SURFACE,
    "teal": ACCENT_TEAL, "amb": ACCENT_AMBER,
    "tp": TEXT_PRIMARY, "ts": TEXT_SECONDARY,
}.items()}

# ─── SESION GLOBAL ────────────────────────────────────────────
_SESSION = {"usuario": None, "sesion_id": None}

# ─── KV ──────────────────────────────────────────────────────
KV = f"""
<CategoryCard>:
    cat_name: ""
    cat_icon: "book"
    cat_color: "{ACCENT_TEAL}"
    orientation: "vertical"
    size_hint_y: None
    height: "90dp"
    padding: 8
    spacing: 4
    md_bg_color: {C['surf']}
    radius: [12,12,12,12]
    elevation: 0
    MDIcon:
        icon: root.cat_icon
        halign: "center"
        font_size: "28sp"
        theme_text_color: "Custom"
        text_color: root._color_rgba
    MDLabel:
        text: root.cat_name
        halign: "center"
        font_style: "Caption"
        theme_text_color: "Custom"
        text_color: {C['ts']}
        size_hint_y: None
        height: self.texture_size[1]

<CourseCard>:
    course_title: ""
    course_cat: ""
    course_instructor: ""
    course_rating: ""
    course_duration: ""
    card_color: "{ACCENT_TEAL}"
    orientation: "vertical"
    size_hint_y: None
    height: "130dp"
    padding: [16,12]
    spacing: 6
    md_bg_color: {C['surf']}
    radius: [12,12,12,12]
    elevation: 0
    BoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: "22dp"
        MDLabel:
            text: root.course_cat
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: root._color_rgba
        Widget:
        MDLabel:
            text: "** " + root.course_rating
            font_style: "Caption"
            halign: "right"
            theme_text_color: "Custom"
            text_color: {C['amb']}
    MDLabel:
        text: root.course_title
        font_style: "Subtitle1"
        bold: True
        theme_text_color: "Custom"
        text_color: {C['tp']}
        size_hint_y: None
        height: self.texture_size[1]
    BoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: "18dp"
        spacing: 12
        MDLabel:
            text: root.course_instructor
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: {C['ts']}
        MDLabel:
            text: root.course_duration
            font_style: "Caption"
            halign: "right"
            theme_text_color: "Custom"
            text_color: {C['ts']}

<StatCard>:
    stat_value: ""
    stat_label: ""
    stat_icon: "star"
    stat_color: "{ACCENT_TEAL}"
    orientation: "vertical"
    size_hint_y: None
    height: "100dp"
    padding: 16
    spacing: 4
    md_bg_color: {C['surf']}
    radius: [12,12,12,12]
    elevation: 0
    MDIcon:
        icon: root.stat_icon
        font_size: "24sp"
        theme_text_color: "Custom"
        text_color: root._color_rgba
        size_hint_y: None
        height: self.texture_size[1]
    MDLabel:
        text: root.stat_value
        font_style: "H5"
        bold: True
        theme_text_color: "Custom"
        text_color: {C['tp']}
        size_hint_y: None
        height: self.texture_size[1]
    MDLabel:
        text: root.stat_label
        font_style: "Caption"
        theme_text_color: "Custom"
        text_color: {C['ts']}
        size_hint_y: None
        height: self.texture_size[1]

<ProgressCourseCard>:
    prog_title: ""
    prog_value: 0
    prog_color: "{ACCENT_TEAL}"
    orientation: "vertical"
    size_hint_y: None
    height: "90dp"
    padding: [16,12]
    spacing: 8
    md_bg_color: {C['surf']}
    radius: [24,24,24,24]
    elevation: 0
    BoxLayout:
        orientation: "horizontal"
        size_hint_y: None
        height: "20dp"
        MDLabel:
            text: root.prog_title
            font_style: "Subtitle2"
            theme_text_color: "Custom"
            text_color: {C['tp']}
        MDLabel:
            text: str(int(root.prog_value * 100)) + "%"
            halign: "right"
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: root._color_rgba
    MDProgressBar:
        value: root.prog_value * 100
        color: root._color_rgba

<ProfileOption>:
    opt_icon: "star"
    opt_text: ""
    orientation: "horizontal"
    size_hint_y: None
    height: "56dp"
    padding: [8,0]
    spacing: 16
    md_bg_color: 0,0,0,0
    MDIcon:
        icon: root.opt_icon
        font_size: "22sp"
        theme_text_color: "Custom"
        text_color: {C['teal']}
        size_hint_x: None
        width: "28dp"
    MDLabel:
        text: root.opt_text
        font_style: "Subtitle1"
        theme_text_color: "Custom"
        text_color: {C['tp']}
    MDIcon:
        icon: "chevron-right"
        font_size: "20sp"
        theme_text_color: "Custom"
        text_color: {C['ts']}
        size_hint_x: None
        width: "24dp"

<LessonItem>:
    lesson_num: ""
    lesson_title: ""
    lesson_done: False
    orientation: "horizontal"
    size_hint_y: None
    height: "60dp"
    padding: [16,0]
    spacing: 12
    md_bg_color: {C['surf']}
    radius: [10,10,10,10]
    elevation: 0
    MDLabel:
        text: root.lesson_num
        font_style: "Subtitle2"
        theme_text_color: "Custom"
        text_color: {C['teal']}
        size_hint_x: None
        width: "28dp"
    MDLabel:
        text: root.lesson_title
        font_style: "Subtitle2"
        theme_text_color: "Custom"
        text_color: {C['tp']}
    MDIcon:
        icon: "check-circle" if root.lesson_done else "circle-outline"
        font_size: "20sp"
        theme_text_color: "Custom"
        text_color: ({C['teal']}) if root.lesson_done else ({C['ts']})
        size_hint_x: None
        width: "28dp"

# ════ SPLASH ════════════════════════════════════════════════
<SplashScreen>:
    canvas.before:
        Color:
            rgba: {C['bg']}
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: "vertical"
        padding: [40,0]
        Widget:
            size_hint_y: 0.3
        MDIcon:
            icon: "school"
            halign: "center"
            font_size: "80sp"
            theme_text_color: "Custom"
            text_color: {C['teal']}
        MDLabel:
            text: "Tequixquiac"
            halign: "center"
            font_style: "H4"
            bold: True
            theme_text_color: "Custom"
            text_color: {C['tp']}
            size_hint_y: None
            height: self.texture_size[1]
        MDLabel:
            text: "Aprende - Crece - Transforma"
            halign: "center"
            font_style: "Subtitle1"
            theme_text_color: "Custom"
            text_color: {C['teal']}
            size_hint_y: None
            height: self.texture_size[1]
        MDLabel:
            text: "Educacion para la comunidad"
            halign: "center"
            font_style: "Caption"
            theme_text_color: "Custom"
            text_color: {C['ts']}
            size_hint_y: None
            height: self.texture_size[1]
        Widget:
            size_hint_y: 0.12
        MDSpinner:
            size_hint: None, None
            size: "36dp","36dp"
            pos_hint: {{"center_x": 0.5}}
            color: {C['teal']}
        Widget:
            size_hint_y: 0.2

# ════ LOGIN ══════════════════════════════════════════════════
<LoginScreen>:
    canvas.before:
        Color:
            rgba: {C['bg']}
        Rectangle:
            pos: self.pos
            size: self.size
    ScrollView:
        BoxLayout:
            orientation: "vertical"
            padding: [32,60,32,32]
            spacing: 20
            size_hint_y: None
            height: self.minimum_height
            MDIcon:
                icon: "school"
                halign: "center"
                font_size: "64sp"
                theme_text_color: "Custom"
                text_color: {C['teal']}
                size_hint_y: None
                height: "80dp"
            MDLabel:
                text: "Bienvenido"
                halign: "center"
                font_style: "H5"
                bold: True
                theme_text_color: "Custom"
                text_color: {C['tp']}
                size_hint_y: None
                height: self.texture_size[1]
            MDLabel:
                text: "Inicia sesion para continuar"
                halign: "center"
                font_style: "Body2"
                theme_text_color: "Custom"
                text_color: {C['ts']}
                size_hint_y: None
                height: self.texture_size[1]
            MDLabel:
                id: error_label
                text: ""
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.8,0.2,0.2,1
                size_hint_y: None
                height: self.texture_size[1]
            MDTextField:
                id: email_field
                hint_text: "Correo electronico"
                icon_right: "email-outline"
                mode: "rectangle"
                line_color_focus: {C['teal']}
                size_hint_y: None
                height: "56dp"
            MDTextField:
                id: password_field
                hint_text: "Contrasena"
                icon_right: "lock-outline"
                password: True
                mode: "rectangle"
                line_color_focus: {C['teal']}
                size_hint_y: None
                height: "56dp"
            MDRaisedButton:
                text: "Iniciar sesion"
                on_release: root.login()
                md_bg_color: {C['teal']}
                text_color: 0,0,0,1
                size_hint_x: 1
                size_hint_y: None
                height: "52dp"
                font_size: "16sp"
            MDFlatButton:
                text: "No tienes cuenta? Registrate"
                theme_text_color: "Custom"
                text_color: {C['teal']}
                pos_hint: {{"center_x": 0.5}}
                size_hint_y: None
                height: "40dp"
                on_release: root.go_register()

# ════ REGISTRO ═══════════════════════════════════════════════
<RegisterScreen>:
    canvas.before:
        Color:
            rgba: {C['bg']}
        Rectangle:
            pos: self.pos
            size: self.size
    ScrollView:
        BoxLayout:
            orientation: "vertical"
            padding: [32,40,32,32]
            spacing: 16
            size_hint_y: None
            height: self.minimum_height
            MDLabel:
                text: "Crear cuenta"
                halign: "center"
                font_style: "H5"
                bold: True
                theme_text_color: "Custom"
                text_color: {C['tp']}
                size_hint_y: None
                height: self.texture_size[1]
            MDLabel:
                id: reg_error
                text: ""
                halign: "center"
                font_style: "Caption"
                theme_text_color: "Custom"
                text_color: 0.8,0.2,0.2,1
                size_hint_y: None
                height: self.texture_size[1]
            MDTextField:
                id: reg_nombre
                hint_text: "Nombre"
                mode: "rectangle"
                line_color_focus: {C['teal']}
                size_hint_y: None
                height: "52dp"
            MDTextField:
                id: reg_apellido
                hint_text: "Apellido"
                mode: "rectangle"
                line_color_focus: {C['teal']}
                size_hint_y: None
                height: "52dp"
            MDTextField:
                id: reg_email
                hint_text: "Correo electronico"
                mode: "rectangle"
                line_color_focus: {C['teal']}
                size_hint_y: None
                height: "52dp"
            MDTextField:
                id: reg_tel
                hint_text: "Telefono (opcional)"
                mode: "rectangle"
                line_color_focus: {C['teal']}
                size_hint_y: None
                height: "52dp"
            MDTextField:
                id: reg_pass
                hint_text: "Contrasena"
                password: True
                mode: "rectangle"
                line_color_focus: {C['teal']}
                size_hint_y: None
                height: "52dp"
            MDTextField:
                id: reg_pass2
                hint_text: "Confirmar contrasena"
                password: True
                mode: "rectangle"
                line_color_focus: {C['teal']}
                size_hint_y: None
                height: "52dp"
            MDRaisedButton:
                text: "Registrarme"
                on_release: root.register()
                md_bg_color: {C['teal']}
                text_color: 0,0,0,1
                size_hint_x: 1
                size_hint_y: None
                height: "52dp"
            MDFlatButton:
                text: "Ya tengo cuenta"
                theme_text_color: "Custom"
                text_color: {C['teal']}
                pos_hint: {{"center_x": 0.5}}
                size_hint_y: None
                height: "40dp"
                on_release: root.go_login()

# ════ HOME ════════════════════════════════════════════════════
<HomeScreen>:
    canvas.before:
        Color:
            rgba: {C['bg']}
        Rectangle:
            pos: self.pos
            size: self.size
    MDBottomNavigation:
        panel_color: {C['surf']}
        text_color_active: {C['teal']}
        text_color_normal: {C['ts']}
        selected_color_background: 0,0,0,0

        MDBottomNavigationItem:
            name: "inicio"
            text: "Inicio"
            icon: "home-outline"
            ScrollView:
                BoxLayout:
                    id: inicio_box
                    orientation: "vertical"
                    padding: [16,16,16,80]
                    spacing: 20
                    size_hint_y: None
                    height: self.minimum_height
                    BoxLayout:
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: 4
                        MDLabel:
                            id: saludo_label
                            text: "Hola!"
                            font_style: "H6"
                            theme_text_color: "Custom"
                            text_color: {C['tp']}
                            size_hint_y: None
                            height: self.texture_size[1]
                        MDLabel:
                            text: "Que vas a aprender hoy?"
                            font_style: "Body2"
                            theme_text_color: "Custom"
                            text_color: {C['ts']}
                            size_hint_y: None
                            height: self.texture_size[1]
                    MDTextField:
                        id: buscador
                        hint_text: "Buscar cursos..."
                        icon_right: "magnify"
                        mode: "rectangle"
                        size_hint_y: None
                        height: "48dp"
                        line_color_focus: {C['teal']}
                        on_text: root.filtrar_cursos(self.text)
                    MDCard:
                        orientation: "vertical"
                        size_hint_y: None
                        height: "160dp"
                        padding: 20
                        spacing: 8
                        md_bg_color: {C['teal']}
                        radius: [16,16,16,16]
                        elevation: 0
                        MDLabel:
                            text: "Curso destacado"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: 0,0,0,0.7
                            size_hint_y: None
                            height: self.texture_size[1]
                        MDLabel:
                            id: banner_titulo
                            text: "Cargando..."
                            font_style: "H6"
                            bold: True
                            theme_text_color: "Custom"
                            text_color: 0,0,0,1
                            size_hint_y: None
                            height: self.texture_size[1]
                        MDLabel:
                            id: banner_info
                            text: ""
                            font_style: "Body2"
                            theme_text_color: "Custom"
                            text_color: 0,0,0,0.8
                            size_hint_y: None
                            height: self.texture_size[1]
                        MDRaisedButton:
                            text: "Ver curso"
                            size_hint_x: None
                            width: "120dp"
                            size_hint_y: None
                            height: "36dp"
                            md_bg_color: 0,0,0,0.2
                            text_color: 0,0,0,1
                            on_release: root.ver_curso_destacado()
                    MDLabel:
                        text: "Categorias"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: {C['tp']}
                        size_hint_y: None
                        height: self.texture_size[1]
                    GridLayout:
                        cols: 3
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: 12
                        CategoryCard:
                            cat_name: "Matematicas"
                            cat_icon: "calculator-variant"
                            cat_color: "{ACCENT_TEAL}"
                        CategoryCard:
                            cat_name: "Ciencias"
                            cat_icon: "flask"
                            cat_color: "#7C4DFF"
                        CategoryCard:
                            cat_name: "Historia"
                            cat_icon: "book-open-variant"
                            cat_color: "{ACCENT_AMBER}"
                        CategoryCard:
                            cat_name: "Tecnologia"
                            cat_icon: "laptop"
                            cat_color: "#00ACC1"
                        CategoryCard:
                            cat_name: "Arte"
                            cat_icon: "palette"
                            cat_color: "#E91E63"
                        CategoryCard:
                            cat_name: "Idiomas"
                            cat_icon: "translate"
                            cat_color: "#43A047"
                    MDLabel:
                        text: "Todos los cursos"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: {C['tp']}
                        size_hint_y: None
                        height: self.texture_size[1]
                    BoxLayout:
                        id: cursos_container
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: 12

        MDBottomNavigationItem:
            name: "mis_cursos"
            text: "Mis cursos"
            icon: "book-open-outline"
            ScrollView:
                BoxLayout:
                    orientation: "vertical"
                    padding: [16,16,16,80]
                    spacing: 16
                    size_hint_y: None
                    height: self.minimum_height
                    MDLabel:
                        text: "Mis cursos"
                        font_style: "H6"
                        theme_text_color: "Custom"
                        text_color: {C['tp']}
                        size_hint_y: None
                        height: self.texture_size[1]
                    BoxLayout:
                        id: mis_cursos_container
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: 12

        MDBottomNavigationItem:
            name: "progreso"
            text: "Progreso"
            icon: "chart-line"
            ScrollView:
                BoxLayout:
                    orientation: "vertical"
                    padding: [16,16,16,80]
                    spacing: 16
                    size_hint_y: None
                    height: self.minimum_height
                    MDLabel:
                        text: "Mi progreso"
                        font_style: "H6"
                        theme_text_color: "Custom"
                        text_color: {C['tp']}
                        size_hint_y: None
                        height: self.texture_size[1]
                    GridLayout:
                        id: stats_grid
                        cols: 2
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: 12
                    MDLabel:
                        text: "Cursos en progreso"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: {C['tp']}
                        size_hint_y: None
                        height: self.texture_size[1]
                    BoxLayout:
                        id: progreso_container
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: 12
                    MDLabel:
                        text: "Notificaciones"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: {C['tp']}
                        size_hint_y: None
                        height: self.texture_size[1]
                    BoxLayout:
                        id: notif_container
                        orientation: "vertical"
                        size_hint_y: None
                        height: self.minimum_height
                        spacing: 8

        MDBottomNavigationItem:
            name: "perfil"
            text: "Perfil"
            icon: "account-outline"
            ScrollView:
                BoxLayout:
                    orientation: "vertical"
                    padding: [16,24,16,80]
                    spacing: 20
                    size_hint_y: None
                    height: self.minimum_height
                    MDIcon:
                        icon: "account-circle"
                        halign: "center"
                        font_size: "80sp"
                        theme_text_color: "Custom"
                        text_color: {C['teal']}
                        size_hint_y: None
                        height: "90dp"
                    MDLabel:
                        id: perfil_nombre
                        text: ""
                        halign: "center"
                        font_style: "H6"
                        theme_text_color: "Custom"
                        text_color: {C['tp']}
                        size_hint_y: None
                        height: self.texture_size[1]
                    MDLabel:
                        id: perfil_email
                        text: ""
                        halign: "center"
                        font_style: "Body2"
                        theme_text_color: "Custom"
                        text_color: {C['ts']}
                        size_hint_y: None
                        height: self.texture_size[1]
                    MDLabel:
                        id: perfil_municipio
                        text: ""
                        halign: "center"
                        font_style: "Caption"
                        theme_text_color: "Custom"
                        text_color: {C['teal']}
                        size_hint_y: None
                        height: self.texture_size[1]
                    MDSeparator:
                    ProfileOption:
                        opt_icon: "account-edit-outline"
                        opt_text: "Editar perfil"
                    ProfileOption:
                        opt_icon: "bell-outline"
                        opt_text: "Notificaciones"
                    ProfileOption:
                        opt_icon: "certificate-outline"
                        opt_text: "Mis certificados"
                    ProfileOption:
                        opt_icon: "shield-lock-outline"
                        opt_text: "Privacidad"
                    ProfileOption:
                        opt_icon: "help-circle-outline"
                        opt_text: "Ayuda y soporte"
                    Widget:
                        size_hint_y: None
                        height: "16dp"
                    MDRaisedButton:
                        text: "Cerrar sesion"
                        md_bg_color: 0.2,0.05,0.05,1
                        text_color: {C['tp']}
                        size_hint_x: 1
                        size_hint_y: None
                        height: "48dp"
                        on_release: root.logout()

# ════ DETALLE DE CURSO ════════════════════════════════════════
<CourseDetailScreen>:
    canvas.before:
        Color:
            rgba: {C['bg']}
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            id: detail_toolbar
            title: "Detalle"
            elevation: 0
            md_bg_color: {C['bg']}
            specific_text_color: {C['tp']}
            left_action_items: [["arrow-left", lambda x: root.go_back()]]
        ScrollView:
            BoxLayout:
                orientation: "vertical"
                padding: [16,16,16,32]
                spacing: 20
                size_hint_y: None
                height: self.minimum_height
                MDCard:
                    id: hero_card
                    orientation: "vertical"
                    size_hint_y: None
                    height: "180dp"
                    padding: 20
                    spacing: 12
                    md_bg_color: {C['teal']}
                    radius: [16,16,16,16]
                    elevation: 0
                    MDLabel:
                        id: hero_cat
                        text: ""
                        font_style: "Caption"
                        theme_text_color: "Custom"
                        text_color: 0,0,0,0.7
                        size_hint_y: None
                        height: self.texture_size[1]
                    MDLabel:
                        id: hero_titulo
                        text: ""
                        font_style: "H5"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: 0,0,0,1
                        size_hint_y: None
                        height: self.texture_size[1]
                    BoxLayout:
                        orientation: "horizontal"
                        size_hint_y: None
                        height: "24dp"
                        spacing: 16
                        MDLabel:
                            id: hero_nivel
                            text: ""
                            font_style: "Body2"
                            theme_text_color: "Custom"
                            text_color: 0,0,0,0.8
                        MDLabel:
                            id: hero_dur
                            text: ""
                            font_style: "Body2"
                            theme_text_color: "Custom"
                            text_color: 0,0,0,0.8
                BoxLayout:
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: 8
                    MDLabel:
                        text: "Descripcion"
                        font_style: "Subtitle1"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: {C['tp']}
                        size_hint_y: None
                        height: self.texture_size[1]
                    MDLabel:
                        id: detail_desc
                        text: ""
                        font_style: "Body2"
                        theme_text_color: "Custom"
                        text_color: {C['ts']}
                        size_hint_y: None
                        height: self.texture_size[1]
                MDCard:
                    orientation: "horizontal"
                    size_hint_y: None
                    height: "60dp"
                    padding: [16,0]
                    spacing: 12
                    md_bg_color: {C['surf']}
                    radius: [12,12,12,12]
                    elevation: 0
                    MDIcon:
                        icon: "account-tie"
                        font_size: "28sp"
                        theme_text_color: "Custom"
                        text_color: {C['teal']}
                        size_hint_x: None
                        width: "36dp"
                    BoxLayout:
                        orientation: "vertical"
                        MDLabel:
                            id: detail_instructor
                            text: ""
                            font_style: "Subtitle2"
                            theme_text_color: "Custom"
                            text_color: {C['tp']}
                        MDLabel:
                            text: "Instructor"
                            font_style: "Caption"
                            theme_text_color: "Custom"
                            text_color: {C['ts']}
                BoxLayout:
                    id: progreso_box
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: 4
                MDLabel:
                    text: "Lecciones del curso"
                    font_style: "Subtitle1"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: {C['tp']}
                    size_hint_y: None
                    height: self.texture_size[1]
                BoxLayout:
                    id: lecciones_container
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: 8
                Widget:
                    size_hint_y: None
                    height: "16dp"
                MDRaisedButton:
                    id: inscribir_btn
                    text: "Inscribirme al curso"
                    md_bg_color: {C['teal']}
                    text_color: 0,0,0,1
                    size_hint_x: 1
                    size_hint_y: None
                    height: "52dp"
                    font_size: "16sp"
                    on_release: root.inscribir_o_continuar()

<RootSM>:
    SplashScreen:
        name: "splash"
    LoginScreen:
        name: "login"
    RegisterScreen:
        name: "register"
    HomeScreen:
        name: "home"
    CourseDetailScreen:
        name: "course_detail"
"""

# ─── WIDGETS ──────────────────────────────────────────────────
class CategoryCard(MDCard):
    cat_name = ""; cat_icon = "book"; cat_color = ACCENT_TEAL
    @property
    def _color_rgba(self): return _hex_to_rgba(self.cat_color)

class CourseCard(MDCard):
    course_title = ""; course_cat = ""; course_instructor = ""
    course_rating = ""; course_duration = ""; card_color = ACCENT_TEAL; curso_id = 0
    @property
    def _color_rgba(self): return _hex_to_rgba(self.card_color)

class StatCard(MDCard):
    stat_value = ""; stat_label = ""; stat_icon = "star"; stat_color = ACCENT_TEAL
    @property
    def _color_rgba(self): return _hex_to_rgba(self.stat_color)

class ProgressCourseCard(MDCard):
    prog_title = ""; prog_value = 0; prog_color = ACCENT_TEAL; curso_id = 0
    @property
    def _color_rgba(self): return _hex_to_rgba(self.prog_color)

class ProfileOption(MDCard):
    opt_icon = "star"; opt_text = ""

class LessonItem(MDCard):
    lesson_num = ""; lesson_title = ""; lesson_done = False; leccion_id = 0

# ─── PANTALLAS ────────────────────────────────────────────────
class SplashScreen(Screen):
    def on_enter(self):
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'login'), 2.5)

class LoginScreen(Screen):
    def login(self):
        email = self.ids.email_field.text.strip()
        pwd   = self.ids.password_field.text
        if not email or not pwd:
            self.ids.error_label.text = "Completa todos los campos"; return
        usuario = autenticar_usuario(email, pwd)
        if not usuario:
            self.ids.error_label.text = "Correo o contrasena incorrectos"; return
        _SESSION["usuario"]   = usuario
        _SESSION["sesion_id"] = registrar_sesion(usuario["id"], dispositivo="Kivy App")
        self.ids.email_field.text = self.ids.password_field.text = self.ids.error_label.text = ""
        self.manager.current = "home"

    def go_register(self): self.manager.current = "register"

class RegisterScreen(Screen):
    def register(self):
        n=self.ids.reg_nombre.text.strip(); a=self.ids.reg_apellido.text.strip()
        e=self.ids.reg_email.text.strip();  t=self.ids.reg_tel.text.strip()
        p1=self.ids.reg_pass.text;          p2=self.ids.reg_pass2.text
        if not all([n,a,e,p1]):
            self.ids.reg_error.text = "Nombre, apellido, correo y contrasena son obligatorios"; return
        if p1 != p2:
            self.ids.reg_error.text = "Las contrasenas no coinciden"; return
        uid = registrar_usuario(n, a, e, p1, telefono=t or None)
        if uid is None:
            self.ids.reg_error.text = "Ese correo ya esta registrado"; return
        enviar_notificacion(uid, "Bienvenido!", "Tu cuenta fue creada exitosamente.", "logro")
        self.ids.reg_error.text = ""
        self.manager.current = "login"

    def go_login(self): self.manager.current = "login"

class HomeScreen(Screen):
    _todos = []
    _dest_id = None

    def on_enter(self):
        Clock.schedule_once(lambda dt: self.cargar(), 0.1)

    def cargar(self, *args):
        u = _SESSION.get("usuario")
        if u:
            self.ids.saludo_label.text = f"Hola, {u['nombre']}!"
            self.ids.perfil_nombre.text    = f"{u['nombre']} {u['apellido']}"
            self.ids.perfil_email.text     = u["email"]
            self.ids.perfil_municipio.text = f"{u.get('municipio','Tequixquiac')}, {u.get('estado','Edo. Mex.')}"

        # Cursos
        cursos = listar_cursos()
        self._todos = cursos
        if cursos:
            self._dest_id = cursos[0]["id"]
            self.ids.banner_titulo.text = cursos[0]["titulo"]
            self.ids.banner_info.text = (
                f"{cursos[0]['duracion_semanas']} semanas - "
                f"{cursos[0]['total_estudiantes']} estudiantes"
            )
        self._poblar_cursos(cursos)

        # Mis cursos
        if u: self._poblar_mis_cursos(u["id"])

        # Progreso
        if u: self._poblar_progreso(u["id"])

    def _poblar_cursos(self, cursos):
        c = self.ids.cursos_container
        c.clear_widgets()
        for i, curso in enumerate(cursos):
            card = CourseCard()
            card.course_title      = curso["titulo"]
            card.course_cat        = curso.get("categoria_nombre", "")
            card.course_instructor = curso.get("instructor_nombre", "")
            card.course_rating     = str(curso.get("rating", "-"))
            card.course_duration   = f"{curso['duracion_semanas']} sem."
            card.card_color        = curso.get("color_hex") or COLORES[i % len(COLORES)]
            card.curso_id          = curso["id"]
            card.bind(on_release=lambda inst, cid=curso["id"]: self._abrir_curso(cid))
            c.add_widget(card)

    def _poblar_mis_cursos(self, uid):
        c = self.ids.mis_cursos_container
        c.clear_widgets()
        cursos = mis_cursos(uid)
        for i, curso in enumerate(cursos):
            card = CourseCard()
            card.course_title      = curso["titulo"]
            card.course_cat        = curso.get("categoria_nombre", "")
            card.course_instructor = curso.get("estado_matricula", "activo")
            card.course_rating     = "-"
            card.course_duration   = f"{curso['duracion_semanas']} sem."
            card.card_color        = curso.get("color_hex") or COLORES[i % len(COLORES)]
            c.add_widget(card)
        if not cursos:
            from kivymd.uix.label import MDLabel as L
            c.add_widget(L(text="Aun no estas inscrito en ningun curso",
                           halign="center", font_style="Body2",
                           theme_text_color="Custom",
                           text_color=_hex_to_rgba(TEXT_SECONDARY),
                           size_hint_y=None, height="40dp"))

    def _poblar_progreso(self, uid):
        # Stats
        s = estadisticas_estudiante(uid)
        g = self.ids.stats_grid
        g.clear_widgets()
        for val, lbl, icono, color in [
            (str(s["cursos_activos"]),     "Cursos activos",   "book-open",     ACCENT_TEAL),
            (str(s["lecciones_hechas"]),   "Lecciones hechas", "check-circle",  "#43A047"),
            (f"{s['tiempo_total_min']}m",  "Tiempo estudio",   "clock-outline", ACCENT_AMBER),
            (str(s["certificados"]),        "Certificados",     "certificate",   "#7C4DFF"),
        ]:
            sc = StatCard(); sc.stat_value=val; sc.stat_label=lbl
            sc.stat_icon=icono; sc.stat_color=color; g.add_widget(sc)

        # Barras progreso
        pc = self.ids.progreso_container; pc.clear_widgets()
        for i, curso in enumerate(mis_cursos(uid)):
            prog = progreso_curso(uid, curso["id"])
            pcard = ProgressCourseCard()
            pcard.prog_title = curso["titulo"]
            pcard.prog_value = prog["porcentaje"] / 100
            pcard.prog_color = COLORES[i % len(COLORES)]
            pc.add_widget(pcard)

        # Notificaciones
        nc = self.ids.notif_container; nc.clear_widgets()
        from kivymd.uix.label import MDLabel as L
        for n in mis_notificaciones(uid, solo_no_leidas=True)[:5]:
            lbl = L(
                text=f"[{n['tipo'].upper()}]  {n['titulo']} - {n.get('mensaje','')}",
                font_style="Caption", theme_text_color="Custom",
                text_color=_hex_to_rgba(TEXT_SECONDARY),
                size_hint_y=None, height="28dp"
            )
            nc.add_widget(lbl)

    def filtrar_cursos(self, texto):
        if not texto: self._poblar_cursos(self._todos); return
        self._poblar_cursos([c for c in self._todos if
            texto.lower() in c["titulo"].lower() or
            texto.lower() in (c.get("categoria_nombre") or "").lower()])

    def ver_curso_destacado(self):
        if self._dest_id: self._abrir_curso(self._dest_id)

    def _abrir_curso(self, curso_id):
        self.manager.get_screen("course_detail").cargar_curso(curso_id)
        self.manager.current = "course_detail"

    def logout(self):
        sid = _SESSION.get("sesion_id")
        if sid: cerrar_sesion(sid)
        _SESSION["usuario"] = _SESSION["sesion_id"] = None
        self.manager.current = "login"

class CourseDetailScreen(Screen):
    _curso_id = None

    def cargar_curso(self, curso_id):
        self._curso_id = curso_id
        curso = obtener_curso(curso_id)
        if not curso: return
        self.ids.detail_toolbar.title   = curso["titulo"]
        self.ids.hero_cat.text          = curso.get("categoria_nombre", "")
        self.ids.hero_titulo.text       = curso["titulo"]
        self.ids.hero_nivel.text        = curso["nivel"]
        self.ids.hero_dur.text          = f"{curso['duracion_semanas']} semanas"
        self.ids.detail_desc.text       = curso.get("descripcion", "Sin descripcion")
        self.ids.detail_instructor.text = curso.get("instructor_nombre", "-")
        self.ids.hero_card.md_bg_color  = _hex_to_rgba(curso.get("color_hex") or ACCENT_TEAL)

        u = _SESSION.get("usuario")
        completadas = lecciones_completadas(u["id"], curso_id) if u else set()
        lc = self.ids.lecciones_container; lc.clear_widgets()
        for lec in listar_lecciones(curso_id):
            item = LessonItem()
            item.lesson_num   = str(lec["orden"]).zfill(2)
            item.lesson_title = lec["titulo"]
            item.lesson_done  = lec["id"] in completadas
            item.leccion_id   = lec["id"]
            if u: item.bind(on_release=lambda inst, lid=lec["id"]: self._completar(lid))
            lc.add_widget(item)

        pb = self.ids.progreso_box; pb.clear_widgets()
        if u and esta_inscrito(u["id"], curso_id):
            from kivymd.uix.label import MDLabel as L
            from kivymd.uix.progressbar import MDProgressBar as PB
            prog = progreso_curso(u["id"], curso_id)
            pb.add_widget(L(text=f"Progreso: {prog['porcentaje']}%  ({prog['completadas']}/{prog['total']} lecciones)",
                            font_style="Caption", theme_text_color="Custom",
                            text_color=_hex_to_rgba(TEXT_SECONDARY),
                            size_hint_y=None, height="20dp"))
            pb.add_widget(PB(value=prog["porcentaje"], color=_hex_to_rgba(ACCENT_TEAL)))
            self.ids.inscribir_btn.text = "Continuar curso"
        else:
            self.ids.inscribir_btn.text = "Inscribirme al curso"

    def _completar(self, leccion_id):
        u = _SESSION.get("usuario")
        if not u or not self._curso_id: return
        if esta_inscrito(u["id"], self._curso_id):
            marcar_leccion_completada(u["id"], leccion_id, tiempo_minutos=15)
            self.cargar_curso(self._curso_id)

    def inscribir_o_continuar(self):
        u = _SESSION.get("usuario")
        if not u or not self._curso_id: return
        if not esta_inscrito(u["id"], self._curso_id):
            inscribir_estudiante(u["id"], self._curso_id)
            enviar_notificacion(u["id"], "Nuevo curso!", "Te inscribiste exitosamente.", "logro")
        self.cargar_curso(self._curso_id)

    def go_back(self):
        self.manager.current = "home"

# ─── APP ──────────────────────────────────────────────────────
class RootSM(ScreenManager):
    pass

class TequixquiacApp(MDApp):
    def build(self):
        inicializar_db()
        self.theme_cls.theme_style     = "Dark"
        self.theme_cls.primary_palette = "Teal"
        self.theme_cls.accent_palette  = "Amber"
        Builder.load_string(KV)
        return RootSM(transition=FadeTransition(duration=0.3))

if __name__ == "__main__":
    TequixquiacApp().run()
