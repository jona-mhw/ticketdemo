

#### **1. Corrección Visual (UI) - Listado de Tickets**

*   **Tarea:** Corregir transparencia en columnas fijas durante el scroll.
*   **Descripción:** Al desplazarse horizontalmente en el listado de tickets, el texto de las columnas móviles se transparenta y es visible detrás de las columnas fijas "FPA actual" e "ID ticket". Se debe asegurar que el fondo de las columnas fijas sea opaco para ocultar el contenido que pasa por detrás.

---

#### **2. Limpieza de Filtros - Listado de Tickets**

*   **Tarea:** Eliminar filtros obsoletos y simplificar la vista.
*   **Descripción:** Se deben realizar los siguientes cambios en los filtros del listado de tickets:
    1.  **Eliminar el filtro "Cumplimiento de FPA"**, ya que el concepto no se utiliza.
    2.  **Eliminar el filtro "Cirugías"**.
    3.  Los únicos filtros que deben permanecer son: **Búsqueda general**, **Estado** y **Fecha de creación**.

---

#### **3. Corrección de Funcionalidad - Filtro de Estado**

*   **Tarea:** Arreglar el comportamiento del filtro por estado "Vigente".
*   **Descripción:** El filtro de estado funciona correctamente para la opción "Anulado", pero no filtra los resultados de manera correcta cuando se selecciona la opción **"Vigente"**. Es necesario corregir esta funcionalidad.

---

#### **4. Funcionalidad de Administración - Gestión de Clínicas**

*   **Tarea:** Añadir opción para activar y desactivar clínicas.
*   **Descripción:** En la sección de **"Administración de clínicas"**, no existe la funcionalidad para activar o desactivar registros. Se debe implementar esta opción para permitir una mejor gestión de las clínicas.

---

#### **5. Corrección de Errores - Exportación a Excel**

*   **Tarea:** Solucionar error en la exportación de datos a Excel.
*   **Descripción:** La funcionalidad de exportar a Excel está generando un error que impide su uso. Se debe diagnosticar y corregir el problema.

---

#### **6. Corrección de Errores - Exportación a PDF (Tickets SID)**

*   **Tarea:** Mostrar el rango de fechas en el PDF para tickets importados.
*   **Descripción:** En los tickets que provienen del SID, el rango de fechas de la cirugía no se está mostrando en el documento PDF generado. Este problema es específico de los tickets importados, ya que los nuevos sí lo muestran. Hay que corregir la visualización de este dato en el PDF para dichos tickets.

---

#### **7. Limpieza de Datos Maestros - Razones Estandarizadas**

*   **Tarea:** Eliminar la razón "no cumplimiento" de los datos maestros.
*   **Descripción:** En `Administración > Datos maestros > Razones estandarizadas`, se debe eliminar la opción **"Razón de no cumplimiento"**. Solo deben permanecer las razones de **modificación** y **anulación**.

---

#### **8. Corrección Visual (UI) - Alineación de Títulos**

*   **Tarea:** Centrar o alinear correctamente el título de la página.
*   **Descripción:** El título principal de las vistas (ej. "Listado de tickets") no está bien alineado. Se encuentra en una posición intermedia, sin estar pegado al menú hamburguesa ni centrado sobre la tabla de contenido. Se debe definir una alineación consistente (centrada o a la izquierda) y aplicarla.

---

#### **9. Nueva Característica - Añadir Footer a la Aplicación**

*   **Tarea:** Implementar un pie de página (footer) en toda la plataforma.
*   **Descripción:** Se debe agregar un footer que sea visible en todas las páginas de la aplicación. El texto debe ser:
    *   Línea 1: **Plataforma Ticket Home 2025**
    *   Línea 2: **Versión Beta 1.0**



    considera acà lo de la hamburguesa: C:\Users\mhw-s\Desktop\ticket\image.png 
    y este trace del error de excel: 37:13] "GET / HTTP/1.1" 302 -
127.0.0.1 - - [23/Aug/2025 12:37:17] "GET /dashboard/ HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2025 12:37:17] "GET /static/js/tickets.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Aug/2025 12:37:23] "GET /tickets/ HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2025 12:37:23] "GET /static/js/tickets.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Aug/2025 12:38:09] "GET /tickets/?search=&status=Vigente&surgery=&date_from=&date_to=&compliance= HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2025 12:38:09] "GET /static/js/tickets.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Aug/2025 12:38:17] "GET /tickets/?search=&status=Anulado&surgery=&date_from=&date_to=&compliance= HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2025 12:38:17] "GET /static/js/tickets.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Aug/2025 12:39:20] "GET /tickets/ HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2025 12:39:21] "GET /static/js/tickets.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Aug/2025 12:39:33] "GET /admin/ HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2025 12:39:33] "GET /static/js/tickets.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Aug/2025 12:39:35] "GET /admin/clinics HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2025 12:39:35] "GET /static/js/tickets.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Aug/2025 12:39:47] "GET /admin/ HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2025 12:39:47] "GET /static/js/tickets.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Aug/2025 12:39:49] "GET /admin/users HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2025 12:39:49] "GET /static/js/tickets.js HTTP/1.1" 304 -
127.0.0.1 - - [23/Aug/2025 12:40:06] "GET /tickets/ HTTP/1.1" 200 -
127.0.0.1 - - [23/Aug/2025 12:40:06] "GET /static/js/tickets.js HTTP/1.1" 304 -
[2025-08-23 12:40:09,506] ERROR in app: Exception on /export/tickets/reports/excel [GET]
Traceback (most recent call last):
  File "C:\Users\mhw-s\Desktop\ticket\routes\exports.py", line 184, in export_excel
    adjustments = json.loads(ticket.adjustment_criteria_snapshot)
                  ^^^^
NameError: name 'json' is not defined

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "C:\Users\mhw-s\Desktop\ticket\venv\Lib\site-packages\flask\app.py", line 2190, in wsgi_app
    response = self.full_dispatch_request()
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\mhw-s\Desktop\ticket\venv\Lib\site-packages\flask\app.py", line 1486, in full_dispatch_request
    rv = self.handle_user_exception(e)
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\mhw-s\Desktop\ticket\venv\Lib\site-packages\flask\app.py", line 1484, in full_dispatch_request
    rv = self.dispatch_request()
         ^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\mhw-s\Desktop\ticket\venv\Lib\site-packages\flask\app.py", line 1469, in dispatch_request
    return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\mhw-s\Desktop\ticket\venv\Lib\site-packages\flask_login\utils.py", line 290, in decorated_view
    return current_app.ensure_sync(func)(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\mhw-s\Desktop\ticket\routes\exports.py", line 186, in export_excel
    except (json.JSONDecodeError, TypeError):
            ^^^^
NameError: name 'json' is not defined