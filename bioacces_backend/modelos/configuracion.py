from database.conexion import obtener_conexion

def obtener_configuracion():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM configuraciones LIMIT 1")
    resultado = cursor.fetchone()
    cursor.close()
    conexion.close()
    return resultado

def guardar_configuracion(datos):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(*) FROM configuraciones")
    existe = cursor.fetchone()[0]

    if existe > 0:
        cursor.execute("""
            UPDATE configuraciones
            SET nombre_institucion = %s,
                nit_institucion = %s,
                minutos_tolerancia_entrada = %s,
                correo_notificaciones = %s,
                ruta_backup_local = %s
        """, (
            datos['nombre_institucion'],
            datos['nit_institucion'],
            datos['minutos_tolerancia_entrada'],
            datos['correo_notificaciones'],
            datos['ruta_backup_local']
        ))
    else:
        cursor.execute("""
            INSERT INTO configuraciones
            (nombre_institucion, nit_institucion, minutos_tolerancia_entrada, correo_notificaciones, ruta_backup_local)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            datos['nombre_institucion'],
            datos['nit_institucion'],
            datos['minutos_tolerancia_entrada'],
            datos['correo_notificaciones'],
            datos['ruta_backup_local']
        ))

    conexion.commit()
    cursor.close()
    conexion.close()
    return {"exito": True, "mensaje": "Configuración guardada correctamente"}