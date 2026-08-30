"""
Plantilla de configuración personal de conexión a MySQL.

Cómo usarla:
1. Copia este archivo y renómbralo a "config_local.py" (mismo carpeta).
2. Ajusta host/user/password/database con tus datos reales de XAMPP.
3. config_local.py NO se sube a GitHub (está en .gitignore), así que
   puedes escribir tu contraseña real ahí sin ningún problema.
"""

CONFIG_BD = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "bioacces",
}