"""
test_db.py
==========
Script de prueba rápida para verificar que la base de datos
funciona correctamente. Ejecutar desde la raíz del proyecto:

    python test_db.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from database.db_manager import (
    inicializar_db, registrar_usuario, autenticar_usuario,
    listar_cursos, inscribir_estudiante, mis_cursos,
    marcar_leccion_completada, progreso_curso, estadisticas_estudiante,
    listar_lecciones, registrar_resultado_examen, emitir_certificado,
    mis_certificados, enviar_notificacion, mis_notificaciones,
    resumen_admin, obtener_config
)

SEP = "─" * 55

def titulo(texto):
    print(f"\n{SEP}\n  {texto}\n{SEP}")

if __name__ == "__main__":
    # 1. Inicializar
    titulo("1. Inicializando base de datos")
    inicializar_db()
    print("✅ BD creada / verificada")

    # 2. Registro de usuario
    titulo("2. Registro de estudiante")
    uid = registrar_usuario(
        nombre="Ana", apellido="López",
        email="ana@test.com", password="1234",
        telefono="5551234567", genero="F"
    )
    print(f"✅ Registrado con ID: {uid}" if uid else "⚠️  Email ya existe")

    # 3. Autenticación
    titulo("3. Autenticación")
    usuario = autenticar_usuario("ana@test.com", "1234")
    print(f"✅ Login: {usuario['nombre']} {usuario['apellido']}" if usuario
          else "❌ Credenciales incorrectas")
    uid = usuario["id"] if usuario else uid

    # 4. Listar cursos
    titulo("4. Cursos disponibles")
    cursos = listar_cursos()
    for c in cursos:
        print(f"  [{c['id']}] {c['titulo']} — {c['nivel']} — {c['categoria_nombre']}")

    # 5. Inscripción
    titulo("5. Inscribir al primer curso")
    curso_id = cursos[0]["id"]
    ok = inscribir_estudiante(uid, curso_id)
    print("✅ Inscrito" if ok else "⚠️  Ya estaba inscrito")

    # 6. Completar lecciones
    titulo("6. Completar lecciones")
    lecciones = listar_lecciones(curso_id)
    for i, l in enumerate(lecciones[:3]):   # completar las 3 primeras
        marcar_leccion_completada(uid, l["id"], tiempo_minutos=20)
        print(f"  ✅ Lección {i+1}: {l['titulo']}")

    # 7. Progreso
    titulo("7. Progreso en el curso")
    prog = progreso_curso(uid, curso_id)
    print(f"  Completadas: {prog['completadas']}/{prog['total']} → {prog['porcentaje']}%")

    # 8. Estadísticas personales
    titulo("8. Estadísticas del estudiante")
    stats = estadisticas_estudiante(uid)
    for k, v in stats.items():
        print(f"  {k}: {v}")

    # 9. Resultado de examen
    titulo("9. Registrar resultado de examen")
    from database.db_manager import _conectar
    with _conectar() as conn:
        examen = conn.execute(
            "SELECT id FROM examenes WHERE curso_id=?", (curso_id,)
        ).fetchone()
    if examen:
        rid = registrar_resultado_examen(uid, examen["id"], puntaje=85.5)
        print(f"✅ Resultado guardado (ID {rid})")

    # 10. Certificado
    titulo("10. Emitir certificado")
    folio = emitir_certificado(uid, curso_id)
    print(f"✅ Folio: {folio}" if folio else "⚠️  Ya emitido")
    certs = mis_certificados(uid)
    for c in certs:
        print(f"  📜 {c['folio']} — {c['curso_titulo']} ({c['fecha_emision']})")

    # 11. Notificaciones
    titulo("11. Notificaciones")
    enviar_notificacion(uid, "¡Bienvenido!", "Has iniciado tu camino educativo.", "logro")
    enviar_notificacion(uid, "Recordatorio", "Tienes lecciones pendientes.", "recordatorio")
    notifs = mis_notificaciones(uid)
    for n in notifs:
        print(f"  🔔 [{n['tipo']}] {n['titulo']}")

    # 12. Resumen admin
    titulo("12. Resumen del administrador")
    for k, v in resumen_admin().items():
        print(f"  {k}: {v}")

    # 13. Configuración
    titulo("13. Configuración de la app")
    print(f"  App: {obtener_config('app_nombre')} v{obtener_config('app_version')}")
    print(f"  Municipio: {obtener_config('municipio')}, {obtener_config('estado')}")

    print(f"\n{'='*55}")
    print("  ✅ Todas las pruebas completadas exitosamente")
    print(f"{'='*55}\n")