##
#main.py
#--------
#Punto de entrada del programa. Al ejecutar "python main.py":

#1. Se crea la ventana de escritorio con pywebview.
#2. Se le "conecta" la clase Api, para que el JavaScript de la
 #  interfaz pueda llamar funciones de Python.
#3. Se carga tu interfaz ya construida (bioaccess/index.html).
##

import webview
from controlador.api import Api


if __name__ == "__main__":
    api = Api()

    ventana = webview.create_window(
        title="BioAccess - Sistema de Control de Acceso",
        # Ruta relativa hacia tu carpeta de interfaz ya construida.
        # Ajusta esta ruta si tu carpeta "bioaccess" (el HTML) está
        # en otro lugar respecto a este archivo main.py.
        url="../index.html",
        js_api=api,
        width=1280,
        height=800,
        min_size=(1024, 700),
    )

    webview.start(debug=True)
    # debug=True abre las herramientas de desarrollador dentro de la
    # ventana (clic derecho -> Inspeccionar), útil mientras programamos.
    # Cuando el sistema esté terminado, se cambia a debug=False.