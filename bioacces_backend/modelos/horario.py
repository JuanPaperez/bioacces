"""
modelos/horario.py
------------------------
Este archivo contiene las consultas SQL relacionadas con la
tabla `horarios`. Por ahora solo necesitamos listarlos, para llenar
el select de "Horario" en el formulario de Agregar Usuario.
"""

from database.conexion import obtener_conexion


def listar_horarios():
    """
    Devuelve TODOS los horarios activos (estado = 1), para llenar
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

    # MySQL devuelve las columnas TIME como objetos timedelta de Python,
    # y esos NO se pueden convertir a JSON para mandarlos al frontend.
    # Por eso los pasamos a texto ("07:00:00") antes de devolverlos.
    for fila in resultados:
        fila["hora_entrada"] = str(fila["hora_entrada"])
        fila["hora_salida"] = str(fila["hora_salida"])

    return resultados