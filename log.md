# Log de Cambios - 2025-08-14

**1. Correcciones del Backlog (Tareas 5, 6, 7):**

*   **Tarea 5:** Se mejoró el comando `reset-db` para poblar la base de datos con una lista más extensa de médicos por clínica.
*   **Tarea 6:** Se ajustó la página de login para mostrar las credenciales de los 3 perfiles de usuario (admin, clinical, visualizador), asegurando consistencia con los datos de demo.
*   **Tarea 7:** Se añadió un botón para ocultar/mostrar los controles de filtros en el dashboard del visualizador, mejorando la experiencia en monitores.

**2. Corrección de Bug (Tarea 8):**

*   Se solucionó un error que impedía guardar y mostrar el segundo nombre y el segundo apellido del paciente al crear un nuevo ticket.
*   Se actualizó la ruta de creación de tickets para procesar y almacenar correctamente estos campos.

---

# Log de Despliegue - 2025-08-09

**1. Generación de Changelog:**

*   Se ha creado el archivo `CHANGELOG.md` con el resumen de los cambios realizados.

**2. Control de Versiones (Git):**

*   Se han añadido los cambios al área de preparación (staging).
*   Se ha creado un commit con el mensaje "feat: Implementa correcciones del backlog".
*   Se ha creado un tag `fix-group-1` para la versión actual.
*   Se ha subido el commit y el tag al repositorio remoto.

**3. Despliegue a Google Cloud Run:**

*   Se ha copiado la base de datos de instancia a la base de datos de demo.
*   Se ha desplegado la aplicación a Google Cloud Run con el tag `fix-group-1`.