"""
controlador/api.py
--------------------
Esta clase conecta pywebview con el JavaScript del frontend.
Cada método público queda disponible en el HTML/JS como:
window.pywebview.api.nombre_del_metodo(...)
"""

from modelos import funcionario, area, horario, administrador, configuracion


class Api:

    def __init__(self):
        # Guarda al administrador que inició sesión mientras la app
        # está abierta. None = nadie ha iniciado sesión todavía.
        self.admin_actual = None

    def iniciar_sesion(self, usuario, password):
        """Llamado desde JS en index.html al enviar el formulario de login."""
        try:
            resultado = administrador.autenticar_administrador(usuario, password)
            if resultado["exito"]:
                self.admin_actual = resultado["datos"]
                return {"ok": True, "datos": resultado["datos"]}
            return {"ok": False, "error": resultado["error"]}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def obtener_sesion_actual(self):
        """Llamado desde cualquier pantalla para saber quién está logueado (topbar, auditoría, etc.)."""
        if self.admin_actual:
            return {"ok": True, "datos": self.admin_actual}
        return {"ok": False, "error": "No hay sesión activa."}

    def cerrar_sesion(self):
        """Llamado desde el link 'Cierre de Sesión' del sidebar."""
        self.admin_actual = None
        return {"ok": True}

    def listar_funcionarios(self):
        """Llamado desde JS cuando se carga la pantalla de Usuarios."""
        try:
            datos = funcionario.listar_funcionarios()
            return {"ok": True, "datos": datos}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def listar_horarios(self):
        """Llamado desde JS al abrir el modal de Agregar Usuario, para llenar el select de Horario."""
        try:
            datos = horario.listar_horarios()
            return {"ok": True, "datos": datos}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def buscar_funcionarios(self, texto_busqueda):
        """Llamado desde JS al escribir en la barra de búsqueda."""
        try:
            datos = funcionario.buscar_funcionarios(texto_busqueda)
            return {"ok": True, "datos": datos}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def agregar_funcionario(self, datos):
        """Recibe un diccionario desde JS con los campos del formulario."""
        try:
            id_creado = funcionario.crear_funcionario(datos)
            return {"ok": True, "id": id_creado, "mensaje": "Usuario creado correctamente."}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def actualizar_funcionario(self, id_funcionario, datos):
        """Recibe el ID del funcionario y un diccionario con los campos modificados."""
        try:
            exito = funcionario.actualizar_funcionario(id_funcionario, datos)
            if exito:
                return {"ok": True, "mensaje": "Usuario actualizado correctamente."}
            return {"ok": False, "error": "No se encontró el registro para actualizar."}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def cambiar_estado_funcionario(self, id_funcionario, nuevo_estado):
        """Cambia el estado del funcionario a 'ACTIVO' o 'INACTIVO'."""
        try:
            exito = funcionario.cambiar_estado_funcionario(id_funcionario, nuevo_estado)
            if exito:
                return {"ok": True, "mensaje": f"Estado cambiado a {nuevo_estado}."}
            return {"ok": False, "error": "No se pudo actualizar el estado."}
        except Exception as error:
            return {"ok": False, "error": str(error)}
        
    def listar_administradores(self):
        """Llamado desde JS al abrir el modal de Administrador del sistema."""
        try:
            datos = administrador.listar_administradores()
            return {"ok": True, "datos": datos}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def crear_administrador(self, datos):
        """Recibe un diccionario desde JS con los campos del nuevo administrador."""
        try:
            id_creado = administrador.crear_administrador(datos)
            return {"ok": True, "id": id_creado, "mensaje": "Administrador creado correctamente."}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def actualizar_administrador(self, id_usuario, datos):
        """Actualiza los datos personales de un administrador existente."""
        try:
            exito = administrador.actualizar_administrador(id_usuario, datos)
            if exito:
                return {"ok": True, "mensaje": "Administrador actualizado correctamente."}
            return {"ok": False, "error": "No se encontró el registro para actualizar."}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def cambiar_password_administrador(self, id_usuario, password_nueva):
        """Cambia la contraseña de un administrador."""
        try:
            exito = administrador.cambiar_password_administrador(id_usuario, password_nueva)
            if exito:
                return {"ok": True, "mensaje": "Contraseña actualizada correctamente."}
            return {"ok": False, "error": "No se encontró el registro para actualizar."}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def cambiar_estado_administrador(self, id_usuario, nuevo_estado):
        """Cambia el estado de un administrador a 'ACTIVO' o 'INACTIVO'."""
        try:
            exito = administrador.cambiar_estado_administrador(id_usuario, nuevo_estado)
            if exito:
                return {"ok": True, "mensaje": f"Estado cambiado a {nuevo_estado}."}
            return {"ok": False, "error": "No se pudo actualizar el estado."}
        except Exception as error:
            return {"ok": False, "error": str(error)}
    
    def obtener_configuracion(self):
        """Llamado desde JS al abrir la sección Configuración general, para precargar los datos."""
        try:
            datos = configuracion.obtener_configuracion()
            return {"ok": True, "datos": datos}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def guardar_configuracion(self, datos):
        """Recibe un diccionario desde JS con los campos del formulario de Configuración general."""
        try:
            resultado = configuracion.guardar_configuracion(datos)
            return {"ok": True, "mensaje": resultado["mensaje"]}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def obtener_estado_sistema(self):
        """Llamado desde JS al cargar Configuración, para el indicador de Estado del sistema."""
        try:
            datos = configuracion.obtener_estado_sistema()
            return {"ok": True, "datos": datos}
        except Exception as error:
            return {"ok": False, "error": str(error)}