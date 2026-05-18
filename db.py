"""
data/db.py
Base de datos simulada con cursos, módulos, posts y eventos de Tequixquiac.
En producción reemplazar con SQLite o API REST.
"""

CURSOS = [
    {
        "id": 1,
        "titulo": "Agricultura Sostenible",
        "instructor": "Juan Ramírez",
        "iniciales": "JR",
        "categoria": "Oficio",
        "emoji": "🌱",
        "color_icono": "Teal",
        "duracion": "3h 20m",
        "alumnos": 142,
        "calificacion": 4.9,
        "gratis": True,
        "nuevo": False,
        "descripcion": (
            "Aprende técnicas de cultivo sostenible adaptadas al clima y suelo de "
            "la región de Tequixquiac. Incluye prácticas de riego eficiente, manejo "
            "de semillas nativas y uso de abonos orgánicos locales."
        ),
        "modulos": [
            {"titulo": "Introducción al cultivo", "duracion": "25 min", "completado": True},
            {"titulo": "Tipos de suelo en Tequixquiac", "duracion": "30 min", "completado": True},
            {"titulo": "Sistemas de riego eficiente", "duracion": "40 min", "completado": False},
            {"titulo": "Abonos orgánicos", "duracion": "35 min", "completado": False},
            {"titulo": "Semillas nativas", "duracion": "28 min", "completado": False},
            {"titulo": "Calendario de siembra", "duracion": "22 min", "completado": False},
            {"titulo": "Control natural de plagas", "duracion": "30 min", "completado": False},
            {"titulo": "Cosecha y almacenamiento", "duracion": "30 min", "completado": False},
        ],
    },
    {
        "id": 2,
        "titulo": "Computación Básica",
        "instructor": "Ana López",
        "iniciales": "AL",
        "categoria": "Digital",
        "emoji": "💻",
        "color_icono": "Amber",
        "duracion": "2h 15m",
        "alumnos": 89,
        "calificacion": 4.7,
        "gratis": True,
        "nuevo": False,
        "descripcion": (
            "Curso introductorio de computación pensado para adultos y jóvenes sin "
            "experiencia previa. Aprenderás a usar una computadora, navegar en internet "
            "y manejar documentos básicos de texto."
        ),
        "modulos": [
            {"titulo": "¿Qué es una computadora?", "duracion": "20 min", "completado": True},
            {"titulo": "El teclado y el ratón", "duracion": "25 min", "completado": False},
            {"titulo": "Navegando internet", "duracion": "30 min", "completado": False},
            {"titulo": "Correo electrónico", "duracion": "25 min", "completado": False},
            {"titulo": "Documentos de texto", "duracion": "20 min", "completado": False},
            {"titulo": "Seguridad en línea", "duracion": "15 min", "completado": False},
        ],
    },
    {
        "id": 3,
        "titulo": "Primeros Auxilios",
        "instructor": "Dr. Roberto Silva",
        "iniciales": "RS",
        "categoria": "Salud",
        "emoji": "🏥",
        "color_icono": "Blue",
        "duracion": "1h 50m",
        "alumnos": 67,
        "calificacion": 5.0,
        "gratis": True,
        "nuevo": True,
        "descripcion": (
            "Aprende las técnicas esenciales de primeros auxilios para emergencias "
            "cotidianas. Impartido por médicos voluntarios de la región. Incluye "
            "RCP, manejo de heridas y actuación ante accidentes comunes."
        ),
        "modulos": [
            {"titulo": "Qué hacer ante una emergencia", "duracion": "20 min", "completado": False},
            {"titulo": "RCP básico", "duracion": "30 min", "completado": False},
            {"titulo": "Heridas y hemorragias", "duracion": "20 min", "completado": False},
            {"titulo": "Quemaduras y fracturas", "duracion": "20 min", "completado": False},
            {"titulo": "Botiquín de primeros auxilios", "duracion": "20 min", "completado": False},
        ],
    },
    {
        "id": 4,
        "titulo": "Artesanía Regional",
        "instructor": "Doña Esperanza Cruz",
        "iniciales": "EC",
        "categoria": "Arte",
        "emoji": "🎨",
        "color_icono": "Pink",
        "duracion": "4h 00m",
        "alumnos": 201,
        "calificacion": 4.8,
        "gratis": True,
        "nuevo": False,
        "descripcion": (
            "Rescata y aprende las técnicas artesanales tradicionales de Tequixquiac. "
            "Desde el trabajo con barro hasta el tejido típico de la región. "
            "Impartido por artesanas con más de 30 años de experiencia."
        ),
        "modulos": [
            {"titulo": "Historia de la artesanía local", "duracion": "20 min", "completado": True},
            {"titulo": "Materiales y herramientas", "duracion": "25 min", "completado": True},
            {"titulo": "Modelado en barro", "duracion": "40 min", "completado": True},
            {"titulo": "Decoración y pintura", "duracion": "30 min", "completado": False},
            {"titulo": "Tejido en telar", "duracion": "45 min", "completado": False},
            {"titulo": "Bordado tradicional", "duracion": "30 min", "completado": False},
            {"titulo": "Papel amate", "duracion": "25 min", "completado": False},
            {"titulo": "Comercialización y emprendimiento", "duracion": "25 min", "completado": False},
            {"titulo": "Exportación artesanal", "duracion": "20 min", "completado": False},
            {"titulo": "Taller final integrador", "duracion": "20 min", "completado": False},
        ],
    },
    {
        "id": 5,
        "titulo": "Emprendimiento Comunitario",
        "instructor": "Ing. Patricia Vega",
        "iniciales": "PV",
        "categoria": "Oficio",
        "emoji": "🚀",
        "color_icono": "Purple",
        "duracion": "2h 45m",
        "alumnos": 53,
        "calificacion": 4.6,
        "gratis": True,
        "nuevo": False,
        "descripcion": (
            "Desarrolla habilidades para crear y gestionar un pequeño negocio dentro "
            "de la comunidad. Aprende sobre finanzas básicas, marketing local y "
            "cómo acceder a apoyos gubernamentales para emprendedores."
        ),
        "modulos": [
            {"titulo": "Idea de negocio", "duracion": "25 min", "completado": False},
            {"titulo": "Plan de negocios básico", "duracion": "35 min", "completado": False},
            {"titulo": "Finanzas para emprendedores", "duracion": "30 min", "completado": False},
            {"titulo": "Marketing en redes sociales", "duracion": "25 min", "completado": False},
            {"titulo": "Apoyos gubernamentales", "duracion": "20 min", "completado": False},
            {"titulo": "Casos de éxito locales", "duracion": "30 min", "completado": False},
        ],
    },
    {
        "id": 6,
        "titulo": "Inglés Básico",
        "instructor": "Mtra. Sandra Méndez",
        "iniciales": "SM",
        "categoria": "Digital",
        "emoji": "🗣️",
        "color_icono": "Green",
        "duracion": "5h 00m",
        "alumnos": 118,
        "calificacion": 4.5,
        "gratis": True,
        "nuevo": False,
        "descripcion": (
            "Aprende las bases del idioma inglés con un enfoque práctico y cotidiano. "
            "Ideal para quienes buscan mejorar sus oportunidades laborales o "
            "comunicarse con turistas que visitan la región."
        ),
        "modulos": [
            {"titulo": "El alfabeto y los números", "duracion": "30 min", "completado": False},
            {"titulo": "Saludos y presentaciones", "duracion": "35 min", "completado": False},
            {"titulo": "Vocabulario cotidiano", "duracion": "40 min", "completado": False},
            {"titulo": "Frases esenciales", "duracion": "35 min", "completado": False},
            {"titulo": "Inglés en el trabajo", "duracion": "40 min", "completado": False},
            {"titulo": "Práctica de conversación", "duracion": "40 min", "completado": False},
            {"titulo": "Comprensión auditiva", "duracion": "30 min", "completado": False},
            {"titulo": "Evaluación final", "duracion": "30 min", "completado": False},
        ],
    },
]

CATEGORIAS = ["Todos", "Oficio", "Digital", "Salud", "Arte"]

POSTS = [
    {
        "id": 1,
        "autor": "Lupita Morales",
        "iniciales": "LM",
        "color_avatar": "Teal",
        "tiempo": "hace 2 horas",
        "texto": "¿Alguien más tuvo problemas con el módulo 3 de agricultura? La parte del riego por goteo me dejó con muchas dudas 💧",
        "likes": 12,
        "comentarios": 5,
    },
    {
        "id": 2,
        "autor": "Carlos Reyes",
        "iniciales": "CR",
        "color_avatar": "Blue",
        "tiempo": "hace 5 horas",
        "texto": "¡Completé el curso de primeros auxilios! 🎉 Lo recomiendo muchísimo para toda la familia. El Dr. Silva explica muy claro.",
        "likes": 34,
        "comentarios": 8,
    },
    {
        "id": 3,
        "autor": "Fernanda Ortiz",
        "iniciales": "FO",
        "color_avatar": "Amber",
        "tiempo": "hace 1 día",
        "texto": "Gracias al curso de computación pude mandar mi primer correo sola 😊 Nunca es tarde para aprender. ¡Gracias a todos!",
        "likes": 67,
        "comentarios": 14,
    },
    {
        "id": 4,
        "autor": "Miguel Ángel Torres",
        "iniciales": "MT",
        "color_avatar": "Green",
        "tiempo": "hace 2 días",
        "texto": "Busco compañeros para el taller presencial de artesanía del sábado. ¿Quién se apunta? 🏺",
        "likes": 21,
        "comentarios": 11,
    },
]

EVENTOS = [
    {
        "id": 1,
        "fecha": "Sáb 22 Jun · 10:00 AM",
        "titulo": "Taller presencial: Artesanía con barro",
        "lugar": "Casa de Cultura, Tequixquiac",
        "color": "Teal",
    },
    {
        "id": 2,
        "fecha": "Dom 23 Jun · 9:00 AM",
        "titulo": "Jornada de salud comunitaria",
        "lugar": "Plaza Principal, Tequixquiac",
        "color": "Blue",
    },
    {
        "id": 3,
        "fecha": "Vie 28 Jun · 4:00 PM",
        "titulo": "Demostración de agricultura: Riego por goteo",
        "lugar": "Parcela demostrativa, Ejido Tequixquiac",
        "color": "Green",
    },
]

USUARIO = {
    "nombre": "María González",
    "iniciales": "MG",
    "municipio": "Tequixquiac, Estado de México",
    "cursos_completados": 2,
    "cursos_en_progreso": 3,
    "horas_aprendidas": 8,
    "logros": [
        {"emoji": "🌱", "titulo": "Primer cultivo", "desc": "Completaste tu primer módulo de agricultura"},
        {"emoji": "💻", "titulo": "Nativo digital", "desc": "Iniciaste el curso de computación"},
        {"emoji": "❤️", "titulo": "Buen samaritano", "desc": "Respondiste 5 preguntas en el foro"},
    ],
}