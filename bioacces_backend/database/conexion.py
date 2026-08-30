"""
#database/conexion.py
#---------------------
#Este archivo tiene UNA sola responsabilidad: abrir una conexión hacia
#la base de datos MySQL local (la que administras en phpMyAdmin).

#Ningún otro archivo del proyecto debe escribir su propia conexión —
#todos deben importar y usar la función obtener_conexion() de aquí.
#Así, si en el futuro cambia el usuario, la contraseña o el nombre de
#la base de datos, solo se corrige en UN lugar.
"""

import mysql.connector
from mysql.connector import Error


# Datos de conexión a tu XAMPP/MySQL local.
# Por defecto, XAMPP usa el usuario "root" sin contraseña.
CONFIG_BD = {
    "host": "localhost",
    "user": "root",
    "password": "",          # si le pusiste contraseña a root en XAMPP, va aquí
    "database": "bioacces",  # el nombre exacto de tu base de datos en phpMyAdmin
}
try:
    from database.config_local import CONFIG_BD as CONFIG_BD_LOCAL
    CONFIG_BD = CONFIG_BD_LOCAL
except ImportError:
    pass


def obtener_conexion():
    """
    Abre y devuelve una nueva conexión a MySQL.
    Si algo falla (XAMPP apagado, mal nombre de base de datos, etc.),
    lanza una excepción clara en vez de fallar en silencio.
    """
    try:
        conexion = mysql.connector.connect(**CONFIG_BD)
        return conexion
    except Error as error:
        # Mensaje pensado para que sea fácil de diagnosticar
        raise ConnectionError(
            f"No se pudo conectar a la base de datos '{CONFIG_BD['database']}'. "
            f"Verifica que XAMPP/MySQL esté iniciado. Detalle: {error}"
        )