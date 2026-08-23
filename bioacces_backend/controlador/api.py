"""
controlador/api.py
--------------------
Esta clase conecta pywebview con el JavaScript del frontend.
Cada método público queda disponible en el HTML/JS como:
window.pywebview.api.nombre_del_metodo(...)
"""

from modelos import funcionario, area, horario


class Api:

    def listar_funcionarios(self):
        """Llamado desde JS cuando se carga la pantalla de Usuarios."""
        try:
            datos = funcionario.listar_funcionarios()
            return {"ok": True, "datos": datos}
        except Exception as error:
            return {"ok": False, "error": str(error)}
        
    def listar_areas(self):
        """Llamado desde JS al abrir el modal de Agregar Usuario, para llenar el select de Área."""
        try:
            datos = area.listar_areas()
            return {"ok": True, "datos": datos}
        except Exception as error:
            return {"ok": False, "error": str(error)}
    def obtener_funcionario(self, id_funcionario):
        """Llamado desde JS al abrir el modal de Editar, para precargar los datos."""
        try:
            datos = funcionario.obtener_funcionario(id_funcionario)
            if datos:
                return {"ok": True, "datos": datos}
            return {"ok": False, "error": "No se encontró el funcionario."}
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