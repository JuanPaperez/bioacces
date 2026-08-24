"""
modelos/area.py
------------------------es
Este archivo contiene las consultas SQL relacionadas con la
tabla `areas`. Por ahora solo necesitamos listarlas, para llenar
el select de "Área" en el formulario de Agregar Usuario.
"""

from database.conexion import obtener_conexion


def listar_areas():
    """
    Devuelve TODAS las áreas registradas, para llenar un <select>
    en el frontend.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT id_area, nombre_area
        FROM areas
        ORDER BY nombre_area ASC
    """

    cursor.execute(consulta)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados