"""
db_manager.py
=============
Gestor central de la base de datos SQLite para Tequixquiac Educa.

Tablas:
  usuarios          – Datos de cada estudiante / administrador
  categorias        – Categorías de cursos
  cursos            – Catálogo de cursos
  lecciones         – Lecciones dentro de un curso
  matriculas        – Relación estudiante ↔ curso (inscripción)
  progreso_lecciones– Lecciones completadas por estudiante
  examenes          – Exámenes asociados a un curso
  preguntas         – Preguntas de un examen
  opciones_respuesta– Opciones de cada pregunta (opción múltiple)
  resultados_examen – Resultado obtenido por un estudiante en un examen
  certificados      – Certificados emitidos al completar un curso
  sesiones          – Registro de inicio/cierre de sesión
  notificaciones    – Notificaciones del sistema para cada usuario
  configuracion     – Preferencias globales de la app
"""

import sqlite3
import hashlib
import os
from datetime import datetime

# ── Ruta de la base de datos ──────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "tequixquiac.db")


def _conectar() -> sqlite3.Connection:
    """Abre una conexión con soporte de claves foráneas activado."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # acceso por nombre de columna
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ─────────────────────────────────────────────────────────────
# INICIALIZACIÓN
# ─────────────────────────────────────────────────────────────

SCHEMA = """
-- ── Usuarios ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS usuarios (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre          TEXT    NOT NULL,
    apellido        TEXT    NOT NULL,
    email           TEXT    NOT NULL UNIQUE,
    password_hash   TEXT    NOT NULL,
    rol             TEXT    NOT NULL DEFAULT 'estudiante',  -- 'estudiante' | 'instructor' | 'admin'
    foto_perfil     TEXT,
    fecha_nacimiento TEXT,
    genero          TEXT,
    telefono        TEXT,
    municipio       TEXT    DEFAULT 'Tequixquiac',
    estado          TEXT    DEFAULT 'Estado de México',
    activo          INTEGER DEFAULT 1,
    fecha_registro  TEXT    DEFAULT (datetime('now','localtime')),
    ultimo_acceso   TEXT
);

-- ── Categorías ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS categorias (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre      TEXT    NOT NULL UNIQUE,
    icono       TEXT,
    color_hex   TEXT,
    descripcion TEXT,
    activo      INTEGER DEFAULT 1
);

-- ── Cursos ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS cursos (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo          TEXT    NOT NULL,
    descripcion     TEXT,
    categoria_id    INTEGER REFERENCES categorias(id),
    instructor_id   INTEGER REFERENCES usuarios(id),
    nivel           TEXT    DEFAULT 'Básico',   -- 'Básico' | 'Intermedio' | 'Avanzado'
    duracion_semanas INTEGER DEFAULT 0,
    imagen          TEXT,
    activo          INTEGER DEFAULT 1,
    fecha_creacion  TEXT    DEFAULT (datetime('now','localtime')),
    fecha_actualizacion TEXT
);

-- ── Lecciones ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS lecciones (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    curso_id    INTEGER NOT NULL REFERENCES cursos(id) ON DELETE CASCADE,
    titulo      TEXT    NOT NULL,
    descripcion TEXT,
    contenido   TEXT,               -- texto / ruta de archivo / URL local
    tipo        TEXT DEFAULT 'texto', -- 'texto' | 'video' | 'pdf' | 'quiz'
    orden       INTEGER DEFAULT 0,
    duracion_min INTEGER DEFAULT 0,
    activo      INTEGER DEFAULT 1
);

-- ── Matrículas ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS matriculas (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id   INTEGER NOT NULL REFERENCES usuarios(id),
    curso_id        INTEGER NOT NULL REFERENCES cursos(id),
    fecha_inscripcion TEXT  DEFAULT (datetime('now','localtime')),
    estado          TEXT    DEFAULT 'activo',   -- 'activo' | 'completado' | 'abandonado'
    fecha_completado TEXT,
    UNIQUE(estudiante_id, curso_id)
);

-- ── Progreso por lección ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS progreso_lecciones (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id   INTEGER NOT NULL REFERENCES usuarios(id),
    leccion_id      INTEGER NOT NULL REFERENCES lecciones(id),
    completada      INTEGER DEFAULT 0,
    fecha_inicio    TEXT    DEFAULT (datetime('now','localtime')),
    fecha_completado TEXT,
    tiempo_minutos  INTEGER DEFAULT 0,
    UNIQUE(estudiante_id, leccion_id)
);

-- ── Exámenes ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS examenes (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    curso_id        INTEGER NOT NULL REFERENCES cursos(id) ON DELETE CASCADE,
    titulo          TEXT    NOT NULL,
    descripcion     TEXT,
    puntaje_minimo  REAL    DEFAULT 70.0,   -- % mínimo para aprobar
    intentos_max    INTEGER DEFAULT 3,
    tiempo_limite_min INTEGER DEFAULT 0,    -- 0 = sin límite
    activo          INTEGER DEFAULT 1,
    fecha_creacion  TEXT    DEFAULT (datetime('now','localtime'))
);

-- ── Preguntas ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS preguntas (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    examen_id   INTEGER NOT NULL REFERENCES examenes(id) ON DELETE CASCADE,
    enunciado   TEXT    NOT NULL,
    tipo        TEXT    DEFAULT 'opcion_multiple', -- 'opcion_multiple' | 'verdadero_falso' | 'abierta'
    puntaje     REAL    DEFAULT 1.0,
    orden       INTEGER DEFAULT 0
);

-- ── Opciones de respuesta ────────────────────────────────────
CREATE TABLE IF NOT EXISTS opciones_respuesta (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    pregunta_id INTEGER NOT NULL REFERENCES preguntas(id) ON DELETE CASCADE,
    texto       TEXT    NOT NULL,
    es_correcta INTEGER DEFAULT 0
);

-- ── Resultados de examen ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS resultados_examen (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id   INTEGER NOT NULL REFERENCES usuarios(id),
    examen_id       INTEGER NOT NULL REFERENCES examenes(id),
    puntaje         REAL    DEFAULT 0,
    aprobado        INTEGER DEFAULT 0,
    intento         INTEGER DEFAULT 1,
    fecha           TEXT    DEFAULT (datetime('now','localtime')),
    tiempo_min      INTEGER DEFAULT 0,
    respuestas_json TEXT    -- JSON con las respuestas del estudiante
);

-- ── Certificados ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS certificados (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    estudiante_id   INTEGER NOT NULL REFERENCES usuarios(id),
    curso_id        INTEGER NOT NULL REFERENCES cursos(id),
    folio           TEXT    NOT NULL UNIQUE,
    fecha_emision   TEXT    DEFAULT (datetime('now','localtime')),
    ruta_archivo    TEXT,
    UNIQUE(estudiante_id, curso_id)
);

-- ── Sesiones ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS sesiones (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id      INTEGER NOT NULL REFERENCES usuarios(id),
    fecha_inicio    TEXT    DEFAULT (datetime('now','localtime')),
    fecha_cierre    TEXT,
    dispositivo     TEXT,
    ip_local        TEXT
);

-- ── Notificaciones ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS notificaciones (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id  INTEGER NOT NULL REFERENCES usuarios(id),
    titulo      TEXT    NOT NULL,
    mensaje     TEXT,
    tipo        TEXT    DEFAULT 'info',  -- 'info' | 'logro' | 'recordatorio' | 'alerta'
    leida       INTEGER DEFAULT 0,
    fecha       TEXT    DEFAULT (datetime('now','localtime'))
);

-- ── Configuración global ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS configuracion (
    clave   TEXT PRIMARY KEY,
    valor   TEXT,
    descripcion TEXT
);
"""


def inicializar_db():
    """Crea todas las tablas y siembra datos iniciales si no existen."""
    with _conectar() as conn:
        conn.executescript(SCHEMA)
        _sembrar_datos_iniciales(conn)
    print(f"[DB] Base de datos lista → {DB_PATH}")


def _sembrar_datos_iniciales(conn: sqlite3.Connection):
    """Inserta registros base solo si las tablas están vacías."""

    # Configuración
    config = [
        ("app_nombre",    "Tequixquiac Educa", "Nombre de la aplicación"),
        ("app_version",   "1.0.0",             "Versión actual"),
        ("municipio",     "Tequixquiac",        "Municipio objetivo"),
        ("estado",        "Estado de México",   "Estado"),
        ("puntaje_minimo","70",                 "Calificación mínima aprobatoria global"),
        ("tema",          "oscuro",             "Tema visual de la app"),
    ]
    conn.executemany(
        "INSERT OR IGNORE INTO configuracion(clave, valor, descripcion) VALUES(?,?,?)",
        config
    )

    # Admin por defecto
    if not conn.execute("SELECT 1 FROM usuarios WHERE rol='admin'").fetchone():
        conn.execute("""
            INSERT INTO usuarios(nombre, apellido, email, password_hash, rol)
            VALUES(?, ?, ?, ?, ?)
        """, ("Admin", "Tequixquiac", "admin@tequixquiac.edu",
              _hash("admin1234"), "admin"))

    # Categorías
    categorias = [
        ("Matemáticas",  "calculator-variant", "#00BFA5",
         "Aritmética, álgebra, geometría y más"),
        ("Ciencias",     "flask",              "#7C4DFF",
         "Biología, química, física y ciencias naturales"),
        ("Historia",     "book-open-variant",  "#FFB300",
         "Historia de México y el mundo"),
        ("Tecnología",   "laptop",             "#00ACC1",
         "Programación, informática y robótica"),
        ("Arte",         "palette",            "#E91E63",
         "Dibujo, música, danza y expresión artística"),
        ("Idiomas",      "translate",          "#43A047",
         "Español, inglés y lenguas indígenas"),
    ]
    for cat in categorias:
        conn.execute(
            "INSERT OR IGNORE INTO categorias(nombre, icono, color_hex, descripcion) VALUES(?,?,?,?)",
            cat
        )

    # Instructor de muestra
    if not conn.execute("SELECT 1 FROM usuarios WHERE rol='instructor'").fetchone():
        conn.execute("""
            INSERT INTO usuarios(nombre, apellido, email, password_hash, rol)
            VALUES(?, ?, ?, ?, ?)
        """, ("María", "García", "mgarcia@tequixquiac.edu",
              _hash("instructor1234"), "instructor"))

    # Cursos de muestra
    if not conn.execute("SELECT 1 FROM cursos").fetchone():
        instructor_id = conn.execute(
            "SELECT id FROM usuarios WHERE rol='instructor'"
        ).fetchone()["id"]

        cursos = [
            ("Álgebra Básica",
             "Aprende los fundamentos del álgebra: variables, ecuaciones y sistemas.",
             1, instructor_id, "Básico", 8),
            ("Biología Celular",
             "Explora la estructura y función de las células.",
             2, instructor_id, "Intermedio", 6),
            ("Historia de México",
             "Recorre los momentos clave de la historia mexicana.",
             3, instructor_id, "Básico", 10),
            ("Programación Python",
             "Aprende a programar desde cero con Python.",
             4, instructor_id, "Básico", 12),
        ]
        conn.executemany("""
            INSERT INTO cursos(titulo, descripcion, categoria_id,
                               instructor_id, nivel, duracion_semanas)
            VALUES(?,?,?,?,?,?)
        """, cursos)

        # Lecciones para Álgebra
        algebra_id = conn.execute(
            "SELECT id FROM cursos WHERE titulo='Álgebra Básica'"
        ).fetchone()["id"]
        lecciones = [
            (algebra_id, "Introducción a variables",    "¿Qué es una variable?", 1),
            (algebra_id, "Operaciones básicas",         "Suma, resta, mult., div.", 2),
            (algebra_id, "Ecuaciones de primer grado",  "Resolver ecuaciones simples.", 3),
            (algebra_id, "Sistemas de ecuaciones",      "Método de sustitución.", 4),
            (algebra_id, "Problemas aplicados",         "Ejercicios de la vida real.", 5),
        ]
        conn.executemany("""
            INSERT INTO lecciones(curso_id, titulo, descripcion, orden)
            VALUES(?,?,?,?)
        """, lecciones)

        # Examen de Álgebra
        conn.execute("""
            INSERT INTO examenes(curso_id, titulo, descripcion, puntaje_minimo, intentos_max)
            VALUES(?, ?, ?, ?, ?)
        """, (algebra_id, "Examen final – Álgebra Básica",
              "Evaluación de todos los temas del curso.", 70.0, 3))

    conn.commit()


# ─────────────────────────────────────────────────────────────
# USUARIOS
# ─────────────────────────────────────────────────────────────

def registrar_usuario(nombre, apellido, email, password,
                      rol="estudiante", telefono=None,
                      fecha_nacimiento=None, genero=None) -> int | None:
    """Registra un nuevo usuario. Retorna su ID o None si el email ya existe."""
    try:
        with _conectar() as conn:
            cur = conn.execute("""
                INSERT INTO usuarios(nombre, apellido, email, password_hash,
                                     rol, telefono, fecha_nacimiento, genero)
                VALUES(?,?,?,?,?,?,?,?)
            """, (nombre, apellido, email, _hash(password),
                  rol, telefono, fecha_nacimiento, genero))
            return cur.lastrowid
    except sqlite3.IntegrityError:
        return None


def autenticar_usuario(email: str, password: str) -> dict | None:
    """Verifica credenciales. Retorna el registro del usuario o None."""
    with _conectar() as conn:
        row = conn.execute("""
            SELECT * FROM usuarios
            WHERE email=? AND password_hash=? AND activo=1
        """, (email, _hash(password))).fetchone()
        if row:
            conn.execute(
                "UPDATE usuarios SET ultimo_acceso=datetime('now','localtime') WHERE id=?",
                (row["id"],)
            )
            return dict(row)
    return None


def obtener_usuario(usuario_id: int) -> dict | None:
    with _conectar() as conn:
        row = conn.execute(
            "SELECT * FROM usuarios WHERE id=?", (usuario_id,)
        ).fetchone()
        return dict(row) if row else None


def actualizar_perfil(usuario_id: int, **campos) -> bool:
    permitidos = {"nombre", "apellido", "telefono", "foto_perfil",
                  "fecha_nacimiento", "genero", "municipio", "estado"}
    datos = {k: v for k, v in campos.items() if k in permitidos}
    if not datos:
        return False
    set_clause = ", ".join(f"{k}=?" for k in datos)
    valores = list(datos.values()) + [usuario_id]
    with _conectar() as conn:
        conn.execute(
            f"UPDATE usuarios SET {set_clause} WHERE id=?", valores
        )
    return True


def cambiar_password(usuario_id: int, password_actual: str,
                     password_nueva: str) -> bool:
    with _conectar() as conn:
        row = conn.execute(
            "SELECT id FROM usuarios WHERE id=? AND password_hash=?",
            (usuario_id, _hash(password_actual))
        ).fetchone()
        if not row:
            return False
        conn.execute(
            "UPDATE usuarios SET password_hash=? WHERE id=?",
            (_hash(password_nueva), usuario_id)
        )
    return True


def listar_usuarios(rol: str | None = None) -> list[dict]:
    with _conectar() as conn:
        if rol:
            rows = conn.execute(
                "SELECT * FROM usuarios WHERE rol=? AND activo=1", (rol,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM usuarios WHERE activo=1"
            ).fetchall()
        return [dict(r) for r in rows]


# ─────────────────────────────────────────────────────────────
# CURSOS
# ─────────────────────────────────────────────────────────────

def listar_cursos(categoria_id: int | None = None,
                  nivel: str | None = None) -> list[dict]:
    query = """
        SELECT c.*, cat.nombre AS categoria_nombre, cat.color_hex,
               u.nombre || ' ' || u.apellido AS instructor_nombre,
               (SELECT COUNT(*) FROM matriculas m WHERE m.curso_id=c.id) AS total_estudiantes
        FROM cursos c
        LEFT JOIN categorias cat ON cat.id = c.categoria_id
        LEFT JOIN usuarios u    ON u.id   = c.instructor_id
        WHERE c.activo=1
    """
    params = []
    if categoria_id:
        query += " AND c.categoria_id=?"
        params.append(categoria_id)
    if nivel:
        query += " AND c.nivel=?"
        params.append(nivel)
    with _conectar() as conn:
        return [dict(r) for r in conn.execute(query, params).fetchall()]


def obtener_curso(curso_id: int) -> dict | None:
    with _conectar() as conn:
        row = conn.execute("""
            SELECT c.*, cat.nombre AS categoria_nombre, cat.color_hex,
                   u.nombre || ' ' || u.apellido AS instructor_nombre
            FROM cursos c
            LEFT JOIN categorias cat ON cat.id = c.categoria_id
            LEFT JOIN usuarios u    ON u.id   = c.instructor_id
            WHERE c.id=?
        """, (curso_id,)).fetchone()
        return dict(row) if row else None


def crear_curso(titulo, descripcion, categoria_id, instructor_id,
                nivel="Básico", duracion_semanas=0) -> int:
    with _conectar() as conn:
        cur = conn.execute("""
            INSERT INTO cursos(titulo, descripcion, categoria_id,
                               instructor_id, nivel, duracion_semanas)
            VALUES(?,?,?,?,?,?)
        """, (titulo, descripcion, categoria_id, instructor_id,
              nivel, duracion_semanas))
        return cur.lastrowid


# ─────────────────────────────────────────────────────────────
# LECCIONES
# ─────────────────────────────────────────────────────────────

def listar_lecciones(curso_id: int) -> list[dict]:
    with _conectar() as conn:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM lecciones WHERE curso_id=? AND activo=1 ORDER BY orden",
            (curso_id,)
        ).fetchall()]


def agregar_leccion(curso_id, titulo, descripcion="",
                    contenido="", tipo="texto", orden=0, duracion_min=0) -> int:
    with _conectar() as conn:
        cur = conn.execute("""
            INSERT INTO lecciones(curso_id, titulo, descripcion,
                                  contenido, tipo, orden, duracion_min)
            VALUES(?,?,?,?,?,?,?)
        """, (curso_id, titulo, descripcion, contenido, tipo, orden, duracion_min))
        return cur.lastrowid


# ─────────────────────────────────────────────────────────────
# MATRÍCULAS
# ─────────────────────────────────────────────────────────────

def inscribir_estudiante(estudiante_id: int, curso_id: int) -> bool:
    try:
        with _conectar() as conn:
            conn.execute("""
                INSERT INTO matriculas(estudiante_id, curso_id)
                VALUES(?,?)
            """, (estudiante_id, curso_id))
        return True
    except sqlite3.IntegrityError:
        return False   # Ya inscrito


def mis_cursos(estudiante_id: int) -> list[dict]:
    with _conectar() as conn:
        return [dict(r) for r in conn.execute("""
            SELECT c.*, m.estado AS estado_matricula,
                   m.fecha_inscripcion, m.fecha_completado,
                   cat.nombre AS categoria_nombre, cat.color_hex
            FROM matriculas m
            JOIN cursos c     ON c.id  = m.curso_id
            JOIN categorias cat ON cat.id = c.categoria_id
            WHERE m.estudiante_id=?
        """, (estudiante_id,)).fetchall()]


def esta_inscrito(estudiante_id: int, curso_id: int) -> bool:
    with _conectar() as conn:
        return bool(conn.execute(
            "SELECT 1 FROM matriculas WHERE estudiante_id=? AND curso_id=?",
            (estudiante_id, curso_id)
        ).fetchone())


# ─────────────────────────────────────────────────────────────
# PROGRESO
# ─────────────────────────────────────────────────────────────

def marcar_leccion_completada(estudiante_id: int, leccion_id: int,
                               tiempo_minutos: int = 0):
    with _conectar() as conn:
        conn.execute("""
            INSERT INTO progreso_lecciones
                (estudiante_id, leccion_id, completada,
                 fecha_completado, tiempo_minutos)
            VALUES(?,?,1,datetime('now','localtime'),?)
            ON CONFLICT(estudiante_id, leccion_id) DO UPDATE SET
                completada=1,
                fecha_completado=datetime('now','localtime'),
                tiempo_minutos=excluded.tiempo_minutos
        """, (estudiante_id, leccion_id, tiempo_minutos))


def progreso_curso(estudiante_id: int, curso_id: int) -> dict:
    """Retorna total de lecciones, completadas y porcentaje."""
    with _conectar() as conn:
        total = conn.execute(
            "SELECT COUNT(*) FROM lecciones WHERE curso_id=? AND activo=1",
            (curso_id,)
        ).fetchone()[0]
        completadas = conn.execute("""
            SELECT COUNT(*) FROM progreso_lecciones pl
            JOIN lecciones l ON l.id = pl.leccion_id
            WHERE pl.estudiante_id=? AND l.curso_id=? AND pl.completada=1
        """, (estudiante_id, curso_id)).fetchone()[0]
        porcentaje = round((completadas / total * 100) if total else 0, 1)

        # Si llegó al 100% actualizar matrícula
        if porcentaje == 100:
            conn.execute("""
                UPDATE matriculas SET estado='completado',
                    fecha_completado=datetime('now','localtime')
                WHERE estudiante_id=? AND curso_id=? AND estado='activo'
            """, (estudiante_id, curso_id))

        return {
            "total": total,
            "completadas": completadas,
            "porcentaje": porcentaje
        }


def lecciones_completadas(estudiante_id: int, curso_id: int) -> set[int]:
    with _conectar() as conn:
        rows = conn.execute("""
            SELECT pl.leccion_id FROM progreso_lecciones pl
            JOIN lecciones l ON l.id = pl.leccion_id
            WHERE pl.estudiante_id=? AND l.curso_id=? AND pl.completada=1
        """, (estudiante_id, curso_id)).fetchall()
        return {r[0] for r in rows}


def estadisticas_estudiante(estudiante_id: int) -> dict:
    with _conectar() as conn:
        cursos_activos = conn.execute(
            "SELECT COUNT(*) FROM matriculas WHERE estudiante_id=? AND estado='activo'",
            (estudiante_id,)
        ).fetchone()[0]
        cursos_completados = conn.execute(
            "SELECT COUNT(*) FROM matriculas WHERE estudiante_id=? AND estado='completado'",
            (estudiante_id,)
        ).fetchone()[0]
        lecciones_hechas = conn.execute(
            "SELECT COUNT(*) FROM progreso_lecciones WHERE estudiante_id=? AND completada=1",
            (estudiante_id,)
        ).fetchone()[0]
        tiempo_total = conn.execute(
            "SELECT COALESCE(SUM(tiempo_minutos),0) FROM progreso_lecciones WHERE estudiante_id=?",
            (estudiante_id,)
        ).fetchone()[0]
        certificados = conn.execute(
            "SELECT COUNT(*) FROM certificados WHERE estudiante_id=?",
            (estudiante_id,)
        ).fetchone()[0]
        examenes_aprobados = conn.execute(
            "SELECT COUNT(*) FROM resultados_examen WHERE estudiante_id=? AND aprobado=1",
            (estudiante_id,)
        ).fetchone()[0]
        return {
            "cursos_activos":     cursos_activos,
            "cursos_completados": cursos_completados,
            "lecciones_hechas":   lecciones_hechas,
            "tiempo_total_min":   tiempo_total,
            "certificados":       certificados,
            "examenes_aprobados": examenes_aprobados,
        }


# ─────────────────────────────────────────────────────────────
# EXÁMENES
# ─────────────────────────────────────────────────────────────

def obtener_examen(examen_id: int) -> dict | None:
    with _conectar() as conn:
        row = conn.execute(
            "SELECT * FROM examenes WHERE id=?", (examen_id,)
        ).fetchone()
        return dict(row) if row else None


def preguntas_examen(examen_id: int) -> list[dict]:
    with _conectar() as conn:
        preguntas = [dict(r) for r in conn.execute(
            "SELECT * FROM preguntas WHERE examen_id=? ORDER BY orden",
            (examen_id,)
        ).fetchall()]
        for p in preguntas:
            p["opciones"] = [dict(o) for o in conn.execute(
                "SELECT * FROM opciones_respuesta WHERE pregunta_id=?",
                (p["id"],)
            ).fetchall()]
        return preguntas


def registrar_resultado_examen(estudiante_id, examen_id,
                                puntaje, respuestas_json="") -> int:
    with _conectar() as conn:
        intento = (conn.execute(
            "SELECT COALESCE(MAX(intento),0) FROM resultados_examen WHERE estudiante_id=? AND examen_id=?",
            (estudiante_id, examen_id)
        ).fetchone()[0] or 0) + 1

        examen = conn.execute(
            "SELECT puntaje_minimo FROM examenes WHERE id=?", (examen_id,)
        ).fetchone()
        aprobado = 1 if examen and puntaje >= examen["puntaje_minimo"] else 0

        cur = conn.execute("""
            INSERT INTO resultados_examen
                (estudiante_id, examen_id, puntaje, aprobado,
                 intento, respuestas_json)
            VALUES(?,?,?,?,?,?)
        """, (estudiante_id, examen_id, puntaje, aprobado,
              intento, respuestas_json))
        return cur.lastrowid


def historial_examenes(estudiante_id: int) -> list[dict]:
    with _conectar() as conn:
        return [dict(r) for r in conn.execute("""
            SELECT re.*, e.titulo AS examen_titulo,
                   c.titulo AS curso_titulo
            FROM resultados_examen re
            JOIN examenes e ON e.id = re.examen_id
            JOIN cursos c   ON c.id = e.curso_id
            WHERE re.estudiante_id=?
            ORDER BY re.fecha DESC
        """, (estudiante_id,)).fetchall()]


# ─────────────────────────────────────────────────────────────
# CERTIFICADOS
# ─────────────────────────────────────────────────────────────

def emitir_certificado(estudiante_id: int, curso_id: int,
                        ruta_archivo: str | None = None) -> str | None:
    """Genera un folio único y registra el certificado."""
    import uuid
    folio = "TEQ-" + str(uuid.uuid4()).upper()[:12]
    try:
        with _conectar() as conn:
            conn.execute("""
                INSERT INTO certificados
                    (estudiante_id, curso_id, folio, ruta_archivo)
                VALUES(?,?,?,?)
            """, (estudiante_id, curso_id, folio, ruta_archivo))
        return folio
    except sqlite3.IntegrityError:
        return None   # Ya existe


def mis_certificados(estudiante_id: int) -> list[dict]:
    with _conectar() as conn:
        return [dict(r) for r in conn.execute("""
            SELECT cert.*, c.titulo AS curso_titulo,
                   cat.nombre AS categoria_nombre
            FROM certificados cert
            JOIN cursos c       ON c.id   = cert.curso_id
            JOIN categorias cat ON cat.id = c.categoria_id
            WHERE cert.estudiante_id=?
            ORDER BY cert.fecha_emision DESC
        """, (estudiante_id,)).fetchall()]


# ─────────────────────────────────────────────────────────────
# SESIONES
# ─────────────────────────────────────────────────────────────

def registrar_sesion(usuario_id: int, dispositivo: str = "",
                     ip_local: str = "") -> int:
    with _conectar() as conn:
        cur = conn.execute("""
            INSERT INTO sesiones(usuario_id, dispositivo, ip_local)
            VALUES(?,?,?)
        """, (usuario_id, dispositivo, ip_local))
        return cur.lastrowid


def cerrar_sesion(sesion_id: int):
    with _conectar() as conn:
        conn.execute(
            "UPDATE sesiones SET fecha_cierre=datetime('now','localtime') WHERE id=?",
            (sesion_id,)
        )


# ─────────────────────────────────────────────────────────────
# NOTIFICACIONES
# ─────────────────────────────────────────────────────────────

def enviar_notificacion(usuario_id: int, titulo: str,
                         mensaje: str = "", tipo: str = "info") -> int:
    with _conectar() as conn:
        cur = conn.execute("""
            INSERT INTO notificaciones(usuario_id, titulo, mensaje, tipo)
            VALUES(?,?,?,?)
        """, (usuario_id, titulo, mensaje, tipo))
        return cur.lastrowid


def mis_notificaciones(usuario_id: int,
                        solo_no_leidas: bool = False) -> list[dict]:
    query = "SELECT * FROM notificaciones WHERE usuario_id=?"
    params = [usuario_id]
    if solo_no_leidas:
        query += " AND leida=0"
    query += " ORDER BY fecha DESC"
    with _conectar() as conn:
        return [dict(r) for r in conn.execute(query, params).fetchall()]


def marcar_notificacion_leida(notif_id: int):
    with _conectar() as conn:
        conn.execute(
            "UPDATE notificaciones SET leida=1 WHERE id=?", (notif_id,)
        )


# ─────────────────────────────────────────────────────────────
# CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────

def obtener_config(clave: str) -> str | None:
    with _conectar() as conn:
        row = conn.execute(
            "SELECT valor FROM configuracion WHERE clave=?", (clave,)
        ).fetchone()
        return row["valor"] if row else None


def guardar_config(clave: str, valor: str):
    with _conectar() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO configuracion(clave, valor) VALUES(?,?)",
            (clave, valor)
        )


# ─────────────────────────────────────────────────────────────
# UTILIDADES
# ─────────────────────────────────────────────────────────────

def resumen_admin() -> dict:
    """Panel de estadísticas para el administrador."""
    with _conectar() as conn:
        return {
            "total_estudiantes": conn.execute(
                "SELECT COUNT(*) FROM usuarios WHERE rol='estudiante' AND activo=1"
            ).fetchone()[0],
            "total_cursos": conn.execute(
                "SELECT COUNT(*) FROM cursos WHERE activo=1"
            ).fetchone()[0],
            "total_matriculas": conn.execute(
                "SELECT COUNT(*) FROM matriculas"
            ).fetchone()[0],
            "matriculas_completadas": conn.execute(
                "SELECT COUNT(*) FROM matriculas WHERE estado='completado'"
            ).fetchone()[0],
            "certificados_emitidos": conn.execute(
                "SELECT COUNT(*) FROM certificados"
            ).fetchone()[0],
            "examenes_realizados": conn.execute(
                "SELECT COUNT(*) FROM resultados_examen"
            ).fetchone()[0],
        }


if __name__ == "__main__":
    inicializar_db()
    print("Resumen:", resumen_admin())