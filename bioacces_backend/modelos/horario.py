"""
modelos/horario.py
------------------------
Este archivo contiene las consultas SQL relacionadas con la
tabla `horarios`.
"""

from database.conexion import obtener_conexion

CAMPOS_HORA = [
    "hora_entrada", "hora_inicio_desayuno", "hora_fin_desayuno",
    "hora_inicio_almuerzo", "hora_fin_almuerzo", "hora_salida"
]


def _formatear_hora(valor):
    """Convierte un timedelta de MySQL a texto 'HH:MM:SS' con ceros a la
    izquierda. str(timedelta) por sí solo NO rellena con cero las horas
    de un solo dígito (da '6:00:00' en vez de '06:00:00'), lo que rompe
    el <input type="time"> del frontend."""
    if valor is None:
        return None
    total_segundos = int(valor.total_seconds())
    horas = total_segundos // 3600
    minutos = (total_segundos % 3600) // 60
    segundos = total_segundos % 60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"


def listar_horarios():
    """
    Devuelve SOLO los horarios activos (estado = 1), para llenar
    un <select> en el frontend.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT id_horario, nombre_turno, hora_entrada, hora_salida
        FROM horarios
        WHERE estado = 1
        ORDER BY nombre_turno ASC
    """
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    for fila in resultados:
        fila["hora_entrada"] = _formatear_hora(fila["hora_entrada"])
        fila["hora_salida"] = _formatear_hora(fila["hora_salida"])

    return resultados


def listar_horarios_admin():
    """
    Devuelve TODOS los horarios (activos e inactivos), con todas las
    columnas, para la tabla "Horarios del sistema" en Configuración.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT id_horario, nombre_turno, hora_entrada, hora_inicio_desayuno,
               hora_fin_desayuno, hora_inicio_almuerzo, hora_fin_almuerzo,
               hora_salida, tiempo_almuerzo_permitido, estado
        FROM horarios
        ORDER BY id_horario ASC
    """
    cursor.execute(consulta)
    resultados = cursor.fetchall()
    cursor.close()
    conexion.close()

    for fila in resultados:
        for campo in CAMPOS_HORA:
            fila[campo] = _formatear_hora(fila[campo])
        fila["codigo"] = f"HOR-{fila['id_horario']:03d}"

    return resultados


def crear_horario(datos):
    """Inserta un nuevo horario, siempre con estado = 1 (Activo)."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        INSERT INTO horarios
            (nombre_turno, hora_entrada, hora_inicio_desayuno, hora_fin_desayuno,
             hora_inicio_almuerzo, hora_fin_almuerzo, hora_salida,
             tiempo_almuerzo_permitido, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 1)
    """
    valores = (
        datos["nombre_turno"], datos["hora_entrada"], datos["hora_inicio_desayuno"],
        datos["hora_fin_desayuno"], datos["hora_inicio_almuerzo"], datos["hora_fin_almuerzo"],
        datos["hora_salida"], datos["tiempo_almuerzo_permitido"]
    )
    cursor.execute(consulta, valores)
    conexion.commit()
    id_creado = cursor.lastrowid

    cursor.close()
    conexion.close()
    return id_creado


def actualizar_horario(id_horario, datos):
    """Actualiza los datos de un horario existente (no toca su estado)."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        UPDATE horarios
        SET nombre_turno = %s, hora_entrada = %s, hora_inicio_desayuno = %s,
            hora_fin_desayuno = %s, hora_inicio_almuerzo = %s, hora_fin_almuerzo = %s,
            hora_salida = %s, tiempo_almuerzo_permitido = %s
        WHERE id_horario = %s
    """
    valores = (
        datos["nombre_turno"], datos["hora_entrada"], datos["hora_inicio_desayuno"],
        datos["hora_fin_desayuno"], datos["hora_inicio_almuerzo"], datos["hora_fin_almuerzo"],
        datos["hora_salida"], datos["tiempo_almuerzo_permitido"], id_horario
    )
    cursor.execute(consulta, valores)
    conexion.commit()
    filas_afectadas = cursor.rowcount

    cursor.close()
    conexion.close()
    return filas_afectadas > 0


def cambiar_estado_horario(id_horario, nuevo_estado):
    """Cambia el estado del horario a 'ACTIVO' o 'INACTIVO' (borrado lógico)."""
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    valor_estado = 1 if nuevo_estado == "ACTIVO" else 0
    cursor.execute("UPDATE horarios SET estado = %s WHERE id_horario = %s", (valor_estado, id_horario))
    conexion.commit()
    filas_afectadas = cursor.rowcount

    cursor.close()
    conexion.close()
    return filas_afectadas > 0