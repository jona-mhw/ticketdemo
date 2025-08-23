# Backlog de Mejoras y Correcciones (22-08-2025)

Este backlog se ha generado a partir de la transcripción de las grabaciones de audio proporcionadas.

---

### Gestión de Tickets y Documentos Impresos

1.  **[LISTO] Modificación de Alta Médica en Impreso:**
    *   **Tarea:** Ampliar el espacio de la firma del médico en el ticket impreso.
    *   **Detalle:** Añadir un campo de "Notas Adicionales" para que el médico pueda anotar a mano cambios en la fecha/hora de alta, sirviendo como respaldo físico para futuras modificaciones en el sistema.

2.  **[LISTO] Privacidad en Ticket Impreso:**
    *   **Tarea:** Ocultar la razón de modificación del alta en el ticket impreso.
    *   **Detalle:** La justificación de un cambio (ej. "complicación médica") no debe ser visible en el documento físico para proteger la privacidad del paciente.

3.  **[LISTO] Deshabilitar Impresión para Tickets Anulados:**
    *   **Tarea:** Impedir la impresión de tickets con estado "Anulado".
    *   **Detalle:** La opción de "Imprimir" o "Exportar PDF" debe estar deshabilitada o no visible para los tickets que ya han sido anulados.

---

### Funcionalidades del Administrador (Admin)

4.  **Edición Completa de Tickets para Admin:**
    *   **Tarea:** Permitir al administrador editar todos los campos de un ticket existente.
    *   **Detalle:** El rol de administrador debe poder modificar cualquier dato de un ticket (RUT, nombre, fechas, estado, etc.), incluyendo la capacidad de revertir un ticket anulado. Todos los cambios deben quedar registrados en el log de auditoría.

---

### Exportación a Excel y Visualización de Datos

5.  **Unificar Comorbilidades en Excel:**
    *   **Tarea:** Consolidar todos los criterios de ajuste (comorbilidades) en una sola columna en el archivo Excel.
    *   **Detalle:** En lugar de múltiples columnas, los criterios deben listarse en una única celda, separados por comas.

6.  **Añadir RUT a la Tabla Principal:**
    *   **Tarea:** Hacer visible el RUT del paciente en la tabla principal del listado de tickets.
    *   **Detalle:** Agregar la columna "RUT" a la vista de `tickets/list.html` para una identificación más rápida.

---

### Búsqueda y Filtros

7.  **Búsqueda Flexible por RUT:**
    *   **Tarea:** Mejorar el campo de búsqueda de RUT para que sea más flexible.
    *   **Detalle:** El sistema debe ser capaz de encontrar a un paciente por su RUT aunque se ingrese sin puntos y sin guion/dígito verificador. El sistema debería formatear la entrada internamente.

8.  **Claridad en Filtros de Fecha:**
    *   **Tarea:** Etiquetar claramente los filtros de búsqueda por fecha.
    *   **Detalle:** Los campos de filtro de fecha deben especificar a qué fecha se refieren (ej. "Fecha de Cirugía", "Fecha de Alta Proyectada", "Fecha de Admisión").

---

### Lógica de Creación y Cálculo de Tickets

9.  **Renombrar Campo de Fecha de Inicio:**
    *   **Tarea:** Cambiar el nombre del campo "Fecha y hora de pabellón".
    *   **Detalle:** Renombrar a "Fecha y hora de admisión", ya que es el punto de partida real para los cálculos de estadía.

10. **Cálculo Automático del Bloque Horario de Alta:**
    *   **Tarea:** Eliminar la selección manual del "Bloque horario de alta" y hacerlo un campo calculado.
    *   **Detalle:** El bloque horario debe calcularse automáticamente basándose en la `Fecha y hora de admisión` + `Horas de estadía de la cirugía/técnica` + `Horas de criterios de ajuste`.

11. **Regla de Negocio para Altas Nocturnas:**
    *   **Tarea:** Implementar una regla de negocio para gestionar altas calculadas en horarios nocturnos.
    *   **Detalle:** Si la FPA calculada es posterior a una hora definida (ej. 20:00 hrs), el sistema debe proponer automáticamente el alta para la mañana del día siguiente en un horario hábil.

12. **Información Quirúrgica Detallada:**
    *   **Tarea:** Añadir más detalle a la información quirúrgica en la creación del ticket.
    *   **Detalles:**
        *   Añadir un campo **"Especialidad"**. La selección de una especialidad debe filtrar la lista de cirugías disponibles.
        *   La selección principal debe ser por **nombre de la cirugía**, no por código.
        *   Añadir un campo de texto libre tipo **"Observaciones" o "Comentarios"** para notas adicionales.