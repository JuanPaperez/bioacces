"""
modelos/auditoria.py
---------------------
MÓDULO: Auditoría
Consultas SQL relacionadas con la tabla `auditoria_logs`.

Por ahora esta tabla registra únicamente acciones sobre
Gestión de administradores (crear, editar, cambiar contraseña,
activar/desactivar). Más adelante se puede ampliar a usuarios,
horarios y configuración general.
"""

from database.conexion import obtener_conexion


def registrar_log(id_usuario, tipo_accion, detalle_cambio):
    """
    Inserta una fila en auditoria_logs.
    id_usuario: quién ejecutó la acción (el admin con sesión activa).
    tipo_accion: texto corto, ej. 'CREAR_ADMIN', 'CAMBIAR_ESTADO_ADMIN'.
    detalle_cambio: texto libre explicando qué pasó.

    Si algo falla aquí, NO debe tumbar la acción principal (crear
    el admin sí debe quedar guardado aunque el log falle) — por eso
    quien llama a esta función debe envolverla en su propio try/except
    y solo registrar el error, nunca dejar que rompa la operación real.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        INSERT INTO auditoria_logs (id_usuario, tipo_accion, detalle_cambio, fecha_hora)
        VALUES (%s, %s, %s, NOW())
    """
    cursor.execute(consulta, (id_usuario, tipo_accion, detalle_cambio))
    conexion.commit()

    cursor.close()
    conexion.close()


def listar_logs(limite=100):
    """
    Devuelve los últimos 'limite' registros de auditoría, del más
    reciente al más antiguo, con el nombre del administrador que
    hizo cada acción (JOIN contra usuarios_administrative).
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT a.id_log, a.tipo_accion, a.detalle_cambio, a.fecha_hora,
               u.nombre_completo AS nombre_usuario, u.usuario AS usuario_login
        FROM auditoria_logs a
        LEFT JOIN usuarios_administrative u ON u.id_usuario = a.id_usuario
        ORDER BY a.fecha_hora DESC
        LIMIT %s
    """
    cursor.execute(consulta, (limite,))
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    for fila in resultados:
        if fila.get("fecha_hora"):
            fila["fecha_hora"] = fila["fecha_hora"].strftime("%d/%m/%Y %I:%M %p")

    return resultados