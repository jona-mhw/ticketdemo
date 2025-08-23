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

4.  **[LISTO] Edición Completa de Tickets para Admin:**
    *   **Tarea:** Permitir al administrador editar todos los campos de un ticket existente.
    *   **Detalle:** El rol de administrador debe poder modificar cualquier dato de un ticket (RUT, nombre, fechas, estado, etc.), incluyendo la capacidad de revertir un ticket anulado. Todos los cambios deben quedar registrados en el log de auditoría.

---

### Exportación a Excel y Visualización de Datos

5.  **[LISTO] Unificar Comorbilidades en Excel:**
    *   **Tarea:** Consolidar todos los criterios de ajuste (comorbilidades) en una sola columna en el archivo Excel.
    *   **Detalle:** En lugar de múltiples columnas, los criterios deben listarse en una única celda, separados por comas.

6.  **[LISTO] Añadir RUT a la Tabla Principal:**
    *   **Tarea:** Hacer visible el RUT del paciente en la tabla principal del listado de tickets.
    *   **Detalle:** Agregar la columna "RUT" a la vista de `tickets/list.html` para una identificación más rápida.

---

### Búsqueda y Filtros

7.  **[LISTO] Búsqueda Flexible por RUT:**
    *   **Tarea:** Mejorar el campo de búsqueda de RUT para que sea más flexible.
    *   **Detalle:** El sistema debe ser capaz de encontrar a un paciente por su RUT aunque se ingrese sin puntos y sin guion/dígito verificador. El sistema debería formatear la entrada internamente.

8.  **[LISTO] Claridad en Filtros de Fecha:**
    *   **Tarea:** Etiquetar claramente los filtros de búsqueda por fecha.
    *   **Detalle:** Los campos de filtro de fecha deben especificar a qué fecha se refieren (ej. "Fecha de Cirugía", "Fecha de Alta Proyectada", "Fecha de Admisión").

---

### Lógica de Creación y Cálculo de Tickets

9.  **[LISTO] Renombrar Campo de Fecha de Inicio:**
    *   **Tarea:** Cambiar el nombre del campo "Fecha y hora de pabellón".
    *   **Detalle:** Renombrar a "Fecha y hora de admisión", ya que es el punto de partida real para los cálculos de estadía.

10. **[LISTO] Cálculo Automático del Bloque Horario de Alta:**
    *   **Tarea:** Eliminar la selección manual del "Bloque horario de alta" y hacerlo un campo calculado que entregarà un bloque de hora de salida, no una hora especifica
    *   **Detalle:** El bloque horario debe calcularse automáticamente basándose en la `Fecha y hora de admisión` + `Horas de estadía de la cirugía/técnica` + `Horas de criterios de ajuste`. Si por ejemplo el calculo da FPA a las 16:45 horas, el rango de salida será entre 14:45 y 16:45. Osea que se deja como fin del bloque de 2 horas la FPA, pero se debe expresar en rango de horas en la impresion, como ya hemos visto antes

11.  **[LISTO] mover ubicacion donde se muetra el càlculo de estadìa mientras se competan los datos del ticket -++:**
    *   **Tarea:** ajuste estetico a como se muetra al usuario el càlculo de FPA mientras se completa el ticket . 
    *   **Detalle:**actualmente està al final del sitio y me gustaria que se muetre de forma estàtica en la parte inferior mientras se completa el fomrulario

12. **[LISTO] Relacionar cirugia y especialidad:**
    *   ya es lo que necesito en esta tarea es ya no trabajar con cirugía y una columna adicional para seleccionar la técnica ahora la cirugía se llamará con su nombre de técnica eso quiere decir que esta cirugía va a ser la que está asociada a una cantidad de horas y a esas horas finalmente se les agrega los ajustes y desde ahí en el cálculo esto es lo definitivo entonces pienso en que como se piensa en una cirugía y una especialidad asociada a un nombre sin nada de código o algo similar que muestre el usuario digamos código definido por el sistema de salud me refiero no ya no incremental bueno el punto es que lo que necesito acá es que al seleccionar la cirugía al querer crear una cirugía se pregunte siempre la especialidad creo que vamos a necesitar un mantenedor de especialidades y además que al momento de estar creando el ticket lo primero que pregunta sea la especialidad y desde ahí se desprendan cuáles son las cirugías en el nombre de la cirugía va a decir entonces el texto completo y desde ahí yo voy a manejar manualmente las técnicas así que olvídate del concepto de técnica porque ahora yo voy a indicar por ejemplo el nombre de la cirugía laparoscopia gastrectomía laparoscópica entonces ahí tengo las dos cosas y es un único campo entonces ahí es donde se debe entender cómo se relaciona este cambio con los reportes con lo que se ve por pantalla con el cálculo con cómo se muestra el cálculo con todo lo que tenga la aplicación por eso me importa mucho que revises bien a fondo todo
