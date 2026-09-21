"""
controlador/api.py
--------------------
Esta clase conecta pywebview con el JavaScript del frontend.
Cada método público queda disponible en el HTML/JS como:
window.pywebview.api.nombre_del_metodo(...)
"""

import webview
from modelos import funcionario, area, horario, administrador, configuracion, auditoria, registro_acceso,historial_horarios
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
    
        # ============================================================
        # MÓDULO: Auditoría — integrado con Gestión de administradores
        # ============================================================

    def _registrar_log_seguro(self, tipo_accion, detalle_cambio):
        """
        Envoltorio para registrar_log(): si el log falla (por lo que
        sea), NO debe tumbar la acción principal que ya se guardó.
        Solo lo dejamos pasar en silencio por ahora; si quieren un
        registro de estos fallos, se puede loguear a un archivo después.
        """
        if not self.admin_actual:
            return
        try:
            auditoria.registrar_log(self.admin_actual["id_usuario"], tipo_accion, detalle_cambio)
        except Exception:
            pass
        
    def _comparar_cambios_admin(self, datos_anteriores, datos_nuevos, id_usuario):
        """
        MÓDULO: Auditoría
        Compara los datos de un administrador antes y después de editarlo,
        y arma un texto legible con exactamente qué campos cambiaron
        (ej: "usuario: 'Isabel30' → 'IsabelV'"). Si no cambió nada, lo dice.
        """
        etiquetas = {
            "nombre_completo": "nombre completo",
            "documento": "documento",
            "usuario": "usuario",
            "correo_electronico": "correo electrónico",
        }

        cambios = []
        if datos_anteriores:
            for campo, etiqueta in etiquetas.items():
                valor_anterior = datos_anteriores.get(campo)
                valor_nuevo = datos_nuevos.get(campo)
                if str(valor_anterior) != str(valor_nuevo):
                    cambios.append(f"{etiqueta}: '{valor_anterior}' → '{valor_nuevo}'")

        nombre_referencia = datos_anteriores["nombre_completo"] if datos_anteriores else f"ID {id_usuario}"

        if cambios:
            return f"Se editó al administrador '{nombre_referencia}' (ID {id_usuario}). Cambios: " + "; ".join(cambios)
        return f"Se guardó el formulario del administrador '{nombre_referencia}' (ID {id_usuario}) sin cambios detectados."

    def listar_auditoria(self):
        """Llamado desde JS al abrir el acordeón de Auditoría."""
        try:
            datos = auditoria.listar_logs()
            return {"ok": True, "datos": datos}
        except Exception as error:
            return {"ok": False, "error": str(error)}

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

    def listar_horarios(self):
        """Llamado desde JS al abrir el modal de Agregar Usuario, para llenar el select de Horario."""
        try:
            datos = horario.listar_horarios()
            return {"ok": True, "datos": datos}
        except Exception as error:
            return {"ok": False, "error": str(error)}
    
    def listar_horarios_admin(self):
        """Llamado desde JS al cargar el panel 'Gestión de horarios' en Configuración."""
        try:
            datos = horario.listar_horarios_admin()
            return {"ok": True, "datos": datos}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def crear_horario(self, datos):
        """Recibe un diccionario desde JS con los campos del nuevo horario."""
        try:
            id_creado = horario.crear_horario(datos)
            self._registrar_log_seguro(
                "CREAR_HORARIO",
                f"Se creó el horario '{datos.get('nombre_turno')}' (ID {id_creado})."
            )
            return {"ok": True, "id": id_creado, "mensaje": "Horario creado correctamente."}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def actualizar_horario(self, id_horario, datos):
        """Actualiza los datos de un horario existente."""
        try:
            exito = horario.actualizar_horario(id_horario, datos)
            if exito:
                self._registrar_log_seguro(
                    "EDITAR_HORARIO",
                    f"Se editó el horario '{datos.get('nombre_turno')}' (ID {id_horario})."
                )
                return {"ok": True, "mensaje": "Horario actualizado correctamente."}
            return {"ok": False, "error": "No se encontró el registro para actualizar."}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def cambiar_estado_horario(self, id_horario, nuevo_estado):
        """Cambia el estado de un horario a 'ACTIVO' o 'INACTIVO'."""
        try:
            exito = horario.cambiar_estado_horario(id_horario, nuevo_estado)
            if exito:
                self._registrar_log_seguro(
                    "CAMBIAR_ESTADO_HORARIO",
                    f"Se cambió el estado del horario ID {id_horario} a {nuevo_estado}."
                )
                return {"ok": True, "mensaje": f"Estado cambiado a {nuevo_estado}."}
            return {"ok": False, "error": "No se pudo actualizar el estado."}
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
        
    def obtener_funcionario(self, id_funcionario):
        """Llamado desde JS al abrir el modal de Editar Usuario."""
        try:
            datos = funcionario.obtener_funcionario(id_funcionario)
            if datos:
                return {"ok": True, "datos": datos}
            return {"ok": False, "error": "No se encontró el funcionario."}
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
        
    def cambiar_horario_funcionario(self, id_funcionario, id_horario_nuevo, motivo):
        """
        Reasigna el horario/turno de un funcionario (rotación individual),
        dejando trazabilidad en historial_horarios. NO toca el catálogo
        de horarios, solo la asignación de esta persona.
        """
        try:
            datos_actuales = funcionario.obtener_funcionario(id_funcionario)
            if not datos_actuales:
                return {"ok": False, "error": "No se encontró el funcionario."}

            id_horario_anterior = datos_actuales.get("id_horario")

            exito = funcionario.cambiar_horario_funcionario(id_funcionario, id_horario_nuevo)
            if not exito:
                return {"ok": False, "error": "No se pudo actualizar el horario del funcionario."}

            id_admin = self.admin_actual["id_usuario"] if self.admin_actual else None
            historial_horarios.registrar_cambio_horario(
                id_funcionario, id_horario_anterior, id_horario_nuevo, motivo, id_admin
            )

            nombre_completo = f"{datos_actuales.get('nombres', '')} {datos_actuales.get('apellidos', '')}".strip()
            self._registrar_log_seguro(
                "CAMBIAR_HORARIO_FUNCIONARIO",
                f"Se cambió el horario de '{nombre_completo}' (ID {id_funcionario}). Motivo: {motivo}."
            )

            return {"ok": True, "mensaje": "Horario del funcionario actualizado correctamente."}
        except Exception as error:
            return {"ok": False, "error": str(error)}
        
    def obtener_ultimo_cambio_horario(self):
        """Llamado desde JS al cargar Configuración, para la tarjeta de 'Gestión de horarios'."""
        try:
            datos = historial_horarios.obtener_ultimo_cambio()
            return {"ok": True, "datos": datos}
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
            self._registrar_log_seguro(
                "CREAR_ADMIN",
                f"Se creó el administrador '{datos.get('usuario')}' ({datos.get('nombre_completo')})."
            )
            return {"ok": True, "id": id_creado, "mensaje": "Administrador creado correctamente."}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def actualizar_administrador(self, id_usuario, datos):
        """Actualiza los datos personales de un administrador existente."""
        try:
            datos_anteriores = administrador.obtener_datos_administrador(id_usuario)
            exito = administrador.actualizar_administrador(id_usuario, datos)
            if exito:
                detalle = self._comparar_cambios_admin(datos_anteriores, datos, id_usuario)
                self._registrar_log_seguro("EDITAR_ADMIN", detalle)
                return {"ok": True, "mensaje": "Administrador actualizado correctamente."}
            return {"ok": False, "error": "No se encontró el registro para actualizar."}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def cambiar_password_administrador(self, id_usuario, password_nueva):
        """Cambia la contraseña de un administrador."""
        try:
            exito = administrador.cambiar_password_administrador(id_usuario, password_nueva)
            if exito:
                info_admin = administrador.obtener_nombre_administrador(id_usuario)
                nombre = info_admin["nombre_completo"] if info_admin else f"ID {id_usuario}"
                self._registrar_log_seguro(
                    "CAMBIAR_PASSWORD_ADMIN",
                    f"Se cambió la contraseña del administrador '{nombre}' (ID {id_usuario})."
                )
                return {"ok": True, "mensaje": "Contraseña actualizada correctamente."}
            return {"ok": False, "error": "No se encontró el registro para actualizar."}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def cambiar_estado_administrador(self, id_usuario, nuevo_estado):
        """Cambia el estado de un administrador a 'ACTIVO' o 'INACTIVO'."""
        try:
            exito = administrador.cambiar_estado_administrador(id_usuario, nuevo_estado)
            if exito:
                info_admin = administrador.obtener_nombre_administrador(id_usuario)
                nombre = info_admin["nombre_completo"] if info_admin else f"ID {id_usuario}"
                self._registrar_log_seguro(
                    "CAMBIAR_ESTADO_ADMIN",
                    f"Se cambió el estado del administrador '{nombre}' (ID {id_usuario}) a {nuevo_estado}."
                )
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
        
    def listar_registros_acceso(self, filtros):
        """
        Llamado desde JS en registro.html y reportes.html. 'filtros' es
        un diccionario con: fecha_desde, fecha_hasta, estado, categoria,
        texto_busqueda — todos opcionales (se puede mandar vacío para
        traer todo).
        """
        try:
            datos = registro_acceso.listar_registros(
                fecha_desde=filtros.get("fecha_desde") or None,
                fecha_hasta=filtros.get("fecha_hasta") or None,
                estado=filtros.get("estado") or None,
                area=filtros.get("area") or None,
                texto_busqueda=filtros.get("texto_busqueda") or None,
            )
            return {"ok": True, "datos": datos}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def obtener_estadisticas_reportes(self, filtros):
        """Llamado desde JS en reportes.html para llenar las 4 tarjetas de arriba."""
        try:
            datos = registro_acceso.obtener_estadisticas_reportes(
                fecha_desde=filtros.get("fecha_desde") or None,
                fecha_hasta=filtros.get("fecha_hasta") or None,
                area=filtros.get("area") or None,
                texto_busqueda=filtros.get("texto_busqueda") or None,
            )
            return {"ok": True, "datos": datos}
        except Exception as error:
            return {"ok": False, "error": str(error)}

    def obtener_tendencia_reportes(self, filtros):
        """Llamado desde JS en reportes.html para llenar la gráfica de barras."""
        try:
            datos = registro_acceso.obtener_tendencia_accesos(
                fecha_desde=filtros.get("fecha_desde") or None,
                fecha_hasta=filtros.get("fecha_hasta") or None,
                area=filtros.get("area") or None,
                texto_busqueda=filtros.get("texto_busqueda") or None,
            )
            return {"ok": True, "datos": datos}
        except Exception as error:
            return {"ok": False, "error": str(error)}
        
    def exportar_reportes_excel(self, filtros):
        """
        Llamado desde JS al hacer clic en 'Exportar excel' en reportes.html.
        Abre el diálogo nativo de guardar archivo y genera el .xlsx con
        los mismos filtros que la tabla.
        """
        try:
            ventana = webview.windows[0]
            ruta_elegida = ventana.create_file_dialog(
                webview.SAVE_DIALOG,
                save_filename="reporte_accesos.xlsx",
                file_types=("Archivos Excel (*.xlsx)",)
            )

            if not ruta_elegida:
                return {"ok": False, "cancelado": True}

            ruta_destino = ruta_elegida if isinstance(ruta_elegida, str) else ruta_elegida[0]
            if not ruta_destino.lower().endswith(".xlsx"):
                ruta_destino += ".xlsx"

            total = registro_acceso.generar_excel_reportes(
                ruta_destino,
                fecha_desde=filtros.get("fecha_desde") or None,
                fecha_hasta=filtros.get("fecha_hasta") or None,
                estado=filtros.get("estado") or None,
                area=filtros.get("area") or None,
                texto_busqueda=filtros.get("texto_busqueda") or None,
            )
            return {"ok": True, "mensaje": f"Se exportaron {total} registros correctamente.", "ruta": ruta_destino}
        except Exception as error:
            return {"ok": False, "error": str(error)}