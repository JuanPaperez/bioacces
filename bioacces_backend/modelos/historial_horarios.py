"""
modelos/historial_horarios.py
------------------------
Registra los cambios de horario/turno de un funcionario, para
trazabilidad. No confundir con el catálogo de `horarios` — esta
tabla guarda el HISTORIAL de asignaciones individuales.
"""

from database.conexion import obtener_conexion


def registrar_cambio_horario(id_funcionario, id_horario_anterior, id_horario_nuevo, motivo, modificado_por):
    """Inserta una fila de historial cada vez que se reasigna el turno de alguien."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        INSERT INTO historial_horarios
            (id_funcionario, id_horario_anterior, id_horario_nuevo, fecha_cambio, motivo, modificado_por)
        VALUES (%s, %s, %s, NOW(), %s, %s)
    """
    cursor.execute(consulta, (id_funcionario, id_horario_anterior, id_horario_nuevo, motivo, modificado_por))
    conexion.commit()
    id_creado = cursor.lastrowid

    cursor.close()
    conexion.close()
    return id_creado

def obtener_ultimo_cambio():
    """
    Trae el cambio de horario más reciente registrado, con el nombre
    del funcionario y el nombre del turno nuevo ya "traducidos", para
    mostrar en la tarjeta de Gestión de horarios en Configuración.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT hh.id_historial, hh.fecha_cambio, hh.motivo,
               f.id_funcionario, f.nombres, f.apellidos, f.categoria,
               hn.nombre_turno AS horario_nuevo
        FROM historial_horarios hh
        JOIN funcionarios f      ON hh.id_funcionario = f.id_funcionario
        LEFT JOIN horarios hn    ON hh.id_horario_nuevo = hn.id_horario
        ORDER BY hh.fecha_cambio DESC
        LIMIT 1
    """
    cursor.execute(consulta)
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()

    if resultado and resultado.get("fecha_cambio"):
        resultado["fecha_cambio"] = str(resultado["fecha_cambio"])

    return resultado