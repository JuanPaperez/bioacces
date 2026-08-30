# Instalación de BioAccess (para el equipo)

BioAccess **no es una página web**: es una aplicación de escritorio hecha con Python + pywebview, que necesita una base de datos MySQL corriendo **en tu propio computador** (vía XAMPP). Por eso no basta con abrir los `.html` en el navegador, ni con Live Server — hay que seguir estos pasos.

## 1. Instalar XAMPP

Descarga e instala XAMPP: https://www.apachefriends.org/es/index.html

Abre el **Panel de control de XAMPP** e inicia el módulo **MySQL** (el botón "Start" a la izquierda de MySQL).

## 2. Crear la base de datos

1. Con MySQL iniciado, entra a `http://localhost/phpmyadmin` en tu navegador.
2. Crea una base de datos nueva llamada exactamente **`bioacces`**.
3. Entra a la pestaña **SQL** de esa base de datos y pega el contenido del archivo `bioacces_backend/database/esquema_bioacces.sql` (está en el repositorio). Ejecuta.
4. *(Opcional pero recomendado)* Pega también el contenido de `bioacces_backend/database/datos_prueba.sql` para tener información de ejemplo (áreas, horarios, funcionarios y un usuario administrador) y probar el sistema sin partir de cero. Con esto ya puedes iniciar sesión con:
   - **Usuario:** `admin`
   - **Contraseña:** `admin123`

   ⚠️ Solo úsalo si tu base de datos está vacía (recién creada en el paso 2). No lo ejecutes sobre una base que ya tenga información real, porque duplicaría filas en áreas, horarios y roles.

## 3. Clonar el repositorio

```bash
git clone https://github.com/JuanPaperez/bioacces.git
cd bioacces/bioacces_backend
```

## 4. Instalar Python y las dependencias

Necesitas Python 3.10 o superior instalado: https://www.python.org/downloads/

Dentro de la carpeta `bioacces_backend`, instala las librerías necesarias con un solo comando:

```bash
pip install -r requirements.txt
```

## 5. Configurar tu conexión a MySQL (solo si es distinta a la de XAMPP por defecto)

Por defecto, el sistema usa usuario `root` sin contraseña (el estándar de XAMPP). Si tu MySQL local es distinto:

1. Ve a `database/config_local.example.py`.
2. Cópialo y renómbralo a `database/config_local.py` (en la misma carpeta).
3. Edita ahí tu `host`, `user`, `password` y `database`.

Este archivo (`config_local.py`) es **tuyo y personal** — nunca se sube a GitHub, así que puedes escribir tu contraseña real sin ningún problema.

Si tu XAMPP es el estándar (root sin contraseña), puedes saltarte este paso — el sistema funciona con los valores por defecto.

## 6. Ejecutar la aplicación

Desde la carpeta `bioacces_backend`:

```bash
python main.py
```

Debería abrirse la ventana nativa de BioAccess.

## Notas importantes

- **Cada computador tiene su propia base de datos.** Los datos que tú agregues (usuarios, configuración, etc.) solo existen en tu MySQL local — no se comparten automáticamente con el resto del equipo.
- **El código sí se comparte por Git**, pero no en tiempo real: cada quien debe correr `git pull` para traer los cambios más recientes que otros hayan subido.
- Si al abrir la app aparece un error de conexión, verifica primero que el módulo **MySQL de XAMPP esté iniciado** (paso 1).
