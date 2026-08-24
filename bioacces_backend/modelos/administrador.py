"""
modelos/administrador.py
------------------------
Este archivo contiene TODAS las consultas SQL relacionadas con la
tabla `usuarios_administrative` (las personas que pueden iniciar
sesión y gestionar el sistema).

Las contraseñas NUNCA se guardan en texto plano — se protegen con
bcrypt, que además de "revolver" la contraseña le agrega una "sal"
aleatoria distinta cada vez, para que dos personas con la misma
contraseña no queden con el mismo hash guardado.
"""

import bcrypt
from database.conexion import obtener_conexion


def listar_administradores():
    """
    Devuelve todos los administradores registrados, para llenar la
    lista del modal "Administrador del sistema".
    NO incluye password_hash en la respuesta, por seguridad —
    nunca debe viajar hacia el frontend, ni siquiera hasheada.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    consulta = """
        SELECT id_usuario, usuario, nombre_completo, documento,
               correo_electronico, fecha_creacion, estado
        FROM usuarios_administrative
        ORDER BY nombre_completo ASC
    """

    cursor.execute(consulta)
    resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    # fecha_creacion llega como datetime de Python, no serializable a JSON.
    for fila in resultados:
        if fila.get("fecha_creacion"):
            fila["fecha_creacion"] = fila["fecha_creacion"].strftime("%d/%m/%Y %I:%M %p")

    return resultados


def obtener_id_rol_administrador():
    """
    Busca el id_role del rol 'Administrador' (el único que existe
    por ahora). Si en el futuro hay más roles, esta función habría
    que ajustarla para recibir cuál rol usar.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT id_role FROM roles WHERE nombre_rol = 'Administrador' LIMIT 1")
    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    if not resultado:
        raise Exception("No existe el rol 'Administrador' en la tabla roles.")

    return resultado["id_role"]


def crear_administrador(datos):
    """
    Crea un nuevo administrador. 'datos' llega desde JS con:
    nombre_completo, documento, usuario, correo_electronico, password.

    La contraseña se hashea con bcrypt antes de guardarla — nunca
    se guarda en texto plano.
    """
    id_role = obtener_id_rol_administrador()

    password_texto = datos.get("password", "")
    password_bytes = password_texto.encode("utf-8")
    password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        INSERT INTO usuarios_administrative (
            usuario, password_hash, nombre_completo, documento,
            correo_electronico, fecha_creacion, estado, id_role
        ) VALUES (%s, %s, %s, %s, %s, NOW(), 1, %s)
    """

    valores = (
        datos.get("usuario"),
        password_hash,
        datos.get("nombre_completo"),
        datos.get("documento"),
        datos.get("correo_electronico"),
        id_role,
    )

    cursor.execute(consulta, valores)
    conexion.commit()

    id_creado = cursor.lastrowid

    cursor.close()
    conexion.close()

    return id_creado


def actualizar_administrador(id_usuario, datos):
    """
    Actualiza los datos personales de un administrador existente.
    NO cambia la contraseña — eso lo hace cambiar_password_administrador()
    por separado, para no arriesgarnos a "borrar" sin querer el hash
    en un guardado normal.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = """
        UPDATE usuarios_administrative
        SET nombre_completo = %s,
            documento = %s,
            usuario = %s,
            correo_electronico = %s
        WHERE id_usuario = %s
    """

    valores = (
        datos.get("nombre_completo"),
        datos.get("documento"),
        datos.get("usuario"),
        datos.get("correo_electronico"),
        id_usuario,
    )

    cursor.execute(consulta, valores)
    conexion.commit()

    filas_afectadas = cursor.rowcount

    cursor.close()
    conexion.close()

    return filas_afectadas > 0


def cambiar_password_administrador(id_usuario, password_nueva):
    """
    Cambia solo la contraseña de un administrador, hasheándola con
    bcrypt antes de guardarla.
    """
    password_bytes = password_nueva.encode("utf-8")
    password_hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    consulta = "UPDATE usuarios_administrative SET password_hash = %s WHERE id_usuario = %s"
    cursor.execute(consulta, (password_hash, id_usuario))
    conexion.commit()

    filas_afectadas = cursor.rowcount

    cursor.close()
    conexion.close()

    return filas_afectadas > 0


def cambiar_estado_administrador(id_usuario, nuevo_estado):
    """
    Cambia el estado de un administrador a ACTIVO o INACTIVO.
    Igual que con los funcionarios, NUNCA se borra físicamente —
    un administrador inactivo no puede iniciar sesión, pero su
    historial de auditoría (qué hizo mientras estuvo activo) se
    conserva intacto.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    valor_estado = 1 if nuevo_estado == "ACTIVO" else 0

    consulta = "UPDATE usuarios_administrative SET estado = %s WHERE id_usuario = %s"
    cursor.execute(consulta, (valor_estado, id_usuario))
    conexion.commit()

    filas_afectadas = cursor.rowcount

    cursor.close()
    conexion.close()

    return filas_afectadas > 0