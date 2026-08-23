"""
#modelos/funcionario.py
#------------------------
#Este archivo contiene TODAS las consultas SQL relacionadas con la
#tabla `funcionarios`. Ningún otro archivo debe escribir un "SELECT"
#o un "INSERT" sobre esta tabla directamente — siempre deben pasar
#por una función de aquí.

#Por ahora solo tiene listar y buscar. Las funciones de agregar,
#editar e inactivar las agregamos en el siguiente paso.
"""

from database.conexion import obtener_conexion


def listar_funcionarios():
    """
    Devuelve TODOS los funcionarios registrados, con el nombre de su
    área y su horario ya "traducidos" (en vez de solo mostrar el
    id_area / id_horario numérico).

    Devuelve una lista de diccionarios, por ejemplo:
    [
      {"id_funcionario": "1.234.567.890", "nombres": "Juan", ...},
      ...
    ]
    """
    conexion = obtener_conexion()
    # dictionary=True hace que cada fila regrese como un diccionario
    # (nombre_columna -> valor), en vez de una tupla sin nombres.
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT
            f.id_funcionario,
            f.nombres,
            f.apellidos,
            f.categoria,
            f.estado,
            a.nombre_area,
            h.nombre_turno
        FROM funcionarios f
        LEFT JOIN areas a    ON f.id_area = a.id_area
        LEFT JOIN horarios h ON f.id_horario = h.id_horario
        WHERE f.estado = 1
        ORDER BY f.nombres ASC
    """

    cursor.execute(consulta)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados


def buscar_funcionarios(texto_busqueda):
    """
    Igual que listar_funcionarios(), pero filtrando por nombre,
    apellido o documento que contenga el texto que escribió el
    usuario en el buscador de la pantalla de Usuarios.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT
            f.id_funcionario,
            f.nombres,
            f.apellidos,
            f.categoria,
            f.estado,
            a.nombre_area,
            h.nombre_turno
        FROM funcionarios f
        LEFT JOIN areas a    ON f.id_area = a.id_area
        LEFT JOIN horarios h ON f.id_horario = h.id_horario
        WHERE f.nombres LIKE %s
           OR f.apellidos LIKE %s
           OR f.id_funcionario LIKE %s
        ORDER BY f.nombres ASC
    """

    # El símbolo %s es un "espacio reservado": mysql-connector se encarga
    # de insertar el texto de forma segura, evitando inyección SQL.
    patron = f"%{texto_busqueda}%"
    cursor.execute(consulta, (patron, patron, patron))
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return resultados

def crear_funcionario(datos):
    """
    Inserta un nuevo funcionario en la base de datos.

    'datos' es un diccionario que llega desde JS con las llaves:
    id_funcionario, nombres, apellidos, cargo, categoria, genero,
    telefono, correo_electronico, id_area, id_horario,
    fecha_ingreso, observaciones.

    Devuelve el id_funcionario (documento) del registro creado.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        INSERT INTO funcionarios (
            id_funcionario, nombres, apellidos, cargo, categoria,
            genero, telefono, correo_electronico, id_area, id_horario,
            fecha_ingreso, estado, observaciones
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    valores = (
        datos.get("id_funcionario"),
        datos.get("nombres"),
        datos.get("apellidos"),
        datos.get("cargo") or None,
        datos.get("categoria"),
        datos.get("genero") or None,
        datos.get("telefono") or None,
        datos.get("correo_electronico") or None,
        datos.get("id_area"),
        datos.get("id_horario"),
        datos.get("fecha_ingreso"),
        1,  # estado: ACTIVO al crearlo
        datos.get("observaciones") or None,
    )

    cursor.execute(consulta, valores)
    conexion.commit()

    id_creado = datos.get("id_funcionario")

    cursor.close()
    conexion.close()

    return id_creado

def cambiar_estado_funcionario(id_funcionario, nuevo_estado):
    """
    Cambia el estado de un funcionario a ACTIVO o INACTIVO
    (NUNCA lo borra físicamente de la base de datos, para no
    perder su historial de asistencias, accesos y permisos).

    'nuevo_estado' llega desde JS como el texto "ACTIVO" o "INACTIVO".
    Devuelve True si se actualizó una fila, False si no se encontró
    el id_funcionario.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    valor_estado = 1 if nuevo_estado == "ACTIVO" else 0

    consulta = """
        UPDATE funcionarios
        SET estado = %s
        WHERE id_funcionario = %s
    """

    cursor.execute(consulta, (valor_estado, id_funcionario))
    conexion.commit()

    filas_afectadas = cursor.rowcount

    cursor.close()
    conexion.close()

    return filas_afectadas > 0

def obtener_funcionario(id_funcionario):
    """
    Trae TODOS los datos de un funcionario específico (para precargar
    el formulario de Editar), incluyendo el nombre del área y el
    nombre del turno de horario (de solo lectura en el formulario).
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT f.*, a.nombre_area, h.nombre_turno
        FROM funcionarios f
        LEFT JOIN areas a    ON f.id_area = a.id_area
        LEFT JOIN horarios h ON f.id_horario = h.id_horario
        WHERE f.id_funcionario = %s
    """

    cursor.execute(consulta, (id_funcionario,))
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    # fecha_ingreso llega como objeto date de Python, que tampoco es
    # serializable a JSON (mismo problema que tuvimos con las horas).
    if resultado and resultado.get("fecha_ingreso"):
        resultado["fecha_ingreso"] = str(resultado["fecha_ingreso"])

    return resultado


def actualizar_funcionario(id_funcionario, datos):
    """
    Actualiza los datos personales de un funcionario existente.
    NO permite cambiar id_funcionario (documento, llave primaria)
    ni id_horario (eso se gestiona desde Configuración).
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        UPDATE funcionarios
        SET nombres = %s,
            apellidos = %s,
            cargo = %s,
            categoria = %s,
            genero = %s,
            telefono = %s,
            correo_electronico = %s,
            id_area = %s,
            fecha_ingreso = %s,
            observaciones = %s
        WHERE id_funcionario = %s
    """

    valores = (
        datos.get("nombres"),
        datos.get("apellidos"),
        datos.get("cargo") or None,
        datos.get("categoria"),
        datos.get("genero") or None,
        datos.get("telefono") or None,
        datos.get("correo_electronico") or None,
        datos.get("id_area"),
        datos.get("fecha_ingreso"),
        datos.get("observaciones") or None,
        id_funcionario,
    )

    cursor.execute(consulta, valores)
    conexion.commit()

    cursor.close()
    conexion.close()

    return True
