## [1.4.0] - 2025-08-15

### Added
- Se rediseñó por completo la funcionalidad de exportación a PDF de un ticket individual.
- El nuevo diseño es visualmente fiel a la maqueta de referencia, usando la paleta de colores y una maquetación profesional.
- El PDF ahora muestra la FPA original y la última modificación (si existe) en secciones separadas y claras.
- Se anonimiza el nombre del paciente en el PDF para proteger su privacidad (Primer Nombre + Inicial de Apellido).
- El PDF se abre en una nueva pestaña del navegador en lugar de descargarse automáticamente.

### Fixed
- Se corrigieron múltiples errores en la librería `reportlab` que impedían la generación del PDF.
- Se solucionaron problemas de contraste de color y disposición de elementos en el diseño del PDF.

### Security
- Se eliminó la credencial de la base de datos que estaba escrita directamente en el código (`config.py`).
- La conexión a la base de datos ahora depende exclusivamente de la variable de entorno `DATABASE_URL`, siguiendo las mejores prácticas de seguridad.
- Se actualizó toda la documentación para reflejar el nuevo método seguro de gestión de credenciales.

## [1.3.1] - 2025-08-15

### Fixed
- Se corrigió un error en el despliegue a Google Cloud Run que impedía que la aplicación se iniciara correctamente debido a que la base de datos de demo no se incluía en la imagen de Docker.
- Se solucionó un error en el login que ocurría cuando un usuario con el rol de 'Visualizador' intentaba iniciar sesión.
- Se corrigió un error en el archivo `requirements.txt` que impedía la correcta instalación de las dependencias.

### Changed
- Se actualizó el archivo `.gitignore` para excluir el archivo `demo_tickethome.db` del control de versiones.

## [1.3.0] - 2025-08-15

### Changed
- **Migración de Base de Datos a Supabase/PostgreSQL:** Se ha migrado la base de datos del proyecto desde SQLite a una instancia de PostgreSQL gestionada en Supabase.
- Se actualizó la configuración de la aplicación para conectarse a la nueva base de datos.
- Se eliminó la lógica de auto-creación de la base de datos local desde `app.py`.
- El proceso de inicialización de la base de datos ahora se maneja exclusivamente a través del comando `flask reset-db`, que opera sobre la instancia remota.

### Added
- Se añadió la dependencia `psycopg2-binary` a `requirements.txt` para la conexión con PostgreSQL.

## [1.2.0] - 2025-08-09

### Added

*   Refactored the ticket list views to improve code quality and maintainability.
*   Created a reusable macro for the tickets table to ensure consistency between different views.
*   Moved the "detalle" button to the left in the ticket list view.
*   Removed the "detalle" action from the visualizador view.

### Fixed

*   **Issue 1:** Corrected inconsistent styling on the `/admin/clinics` page by applying Tailwind CSS to match the rest of the admin section.
*   **Issue 2:** Fixed an "Internal Server Error" on the `/admin/master-data` page by ensuring that all master data tables are correctly populated for all clinics.
*   **Issue 3:** Resolved an issue where "Bloque Horario de Alta" and "criterios de ajuste de estancia" were missing data when creating a new ticket.
*   **Issue 4:** Implemented disaggregated name fields in the ticket list view, allowing users to see and select "Primer Nombre", "Segundo Nombre", "Apellido Paterno", and "Apellido Materno" as separate columns.
*   **Issue 5:** Fixed the column sorting functionality in the ticket list view.
