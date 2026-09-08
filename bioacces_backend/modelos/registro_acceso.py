"""
modelos/registro_acceso.py
----------------------------
MÓDULO: Registro de Accesos / Reportes
Consultas SQL sobre la tabla `registros_acceso` — cada fila es un
intento de marcación de huella en el Kiosco (permitido o denegado),
asociado a un funcionario.

Este modelo lo usan dos pantallas: registro.html (vista del momento
actual) y, más adelante, reportes.html (vista histórica con más
filtros) — ambas reusan listar_registros() con distintos filtros,
para no duplicar la misma consulta en dos archivos.
"""

from database.conexion import obtener_conexion


def listar_registros(fecha_desde=None, fecha_hasta=None, estado=None, texto_busqueda=None):
    """
    Devuelve los registros de acceso que cumplen los filtros dados,
    del más reciente al más antiguo, con nombre/documento/categoría
    del funcionario ya incluidos (LEFT JOIN contra funcionarios).

    Todos los filtros son opcionales — si no se pasa ninguno, trae
    todo. El filtro de texto busca coincidencia parcial en nombre,
    apellido o documento.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    condiciones = []
    valores = []

    if fecha_desde:
        condiciones.append("r.fecha >= %s")
        valores.append(fecha_desde)
    if fecha_hasta:
        condiciones.append("r.fecha <= %s")
        valores.append(fecha_hasta)
    if estado:
        condiciones.append("r.estado = %s")
        valores.append(estado)
    if texto_busqueda:
        condiciones.append("(f.nombres LIKE %s OR f.apellidos LIKE %s OR f.id_funcionario LIKE %s)")
        patron = f"%{texto_busqueda}%"
        valores.extend([patron, patron, patron])

    where_sql = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""

    consulta = f"""
        SELECT
            r.id_registro, r.fecha, r.hora, r.tipo_acceso,
            r.estado, r.codigo_registro,
            f.id_funcionario, f.nombres, f.apellidos, f.categoria
        FROM registros_acceso r
        LEFT JOIN funcionarios f ON r.id_funcionario = f.id_funcionario
        {where_sql}
        ORDER BY r.fecha DESC, r.hora DESC
    """

    cursor.execute(consulta, valores)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    for fila in resultados:
        if fila.get("fecha"):
            fila["fecha"] = fila["fecha"].strftime("%d/%m/%Y")
        if fila.get("hora"):
            fila["hora"] = _formatear_hora(fila["hora"])

    return resultados


def _formatear_hora(valor_hora):
    """
    mysql-connector entrega una columna TIME como timedelta, no como
    hora legible. Esta función la convierte a texto tipo '06:48 a.m.'
    """
    total_segundos = int(valor_hora.total_seconds())
    horas = (total_segundos // 3600) % 24
    minutos = (total_segundos % 3600) // 60

    sufijo = "a.m." if horas < 12 else "p.m."
    horas_12 = horas % 12 or 12

    return f"{horas_12:02d}:{minutos:02d} {sufijo}"