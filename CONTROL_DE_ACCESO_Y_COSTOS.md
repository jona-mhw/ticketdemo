# Guía de Control de Acceso y Costos en Google Cloud

Esta guía proporciona los comandos y estrategias para gestionar quién puede acceder a tu aplicación y cómo mantener los costos de Google Cloud Platform (GCP) bajo control.

---

## 1. Control de Acceso al Servicio (Público vs. Privado)

Por defecto, tu servicio está desplegado para ser accesible públicamente (`--allow-unauthenticated`). Puedes cambiar esto en cualquier momento para restringir el acceso solo a usuarios autenticados con permisos específicos en tu proyecto de GCP.

### Suspender Acceso Público (Hacer el servicio privado)

Este comando elimina el acceso público. Después de ejecutarlo, solo las cuentas con los roles adecuados (ej. `roles/run.invoker`) podrán acceder a la URL del servicio.

```bash
gcloud run services update tickethome-demo --region us-central1 --no-allow-unauthenticated
```

**Cuándo usarlo:**
*   Si quieres suspender temporalmente el acceso a la demo.
*   Durante mantenimientos o si detectas actividad sospechosa.

### Restaurar Acceso Público

Este comando vuelve a hacer que el servicio sea accesible para cualquier persona en internet.

```bash
gcloud run deploy tickethome-demo --source . --region us-central1 --allow-unauthenticated
```

**Nota:** Usamos el comando `deploy` aquí en lugar de `update` para asegurar que se despliega la última versión del código junto con la configuración de acceso público.

---

## 2. Estrategias para el Control de Costos

La clave para evitar sorpresas en la facturación es la prevención y la monitorización.

### 1. Configurar Presupuestos y Alertas (Recomendación Principal)

Esta es la forma más efectiva de estar al tanto de tus gastos. Un presupuesto no detiene los servicios, pero te notifica cuando te acercas a un límite que tú defines.

**Cómo hacerlo:**
1.  Ve a la sección **"Facturación"** en la consola de Google Cloud.
2.  En el menú de la izquierda, selecciona **"Presupuestos y alertas"**.
3.  Haz clic en **"Crear presupuesto"**.
4.  **Alcance:** Déjalo por defecto para que aplique a todo tu proyecto.
5.  **Importe:** Define un importe de presupuesto mensual (ej. 5 USD, 10 USD). Empieza con un valor bajo.
6.  **Acciones:** Aquí está la magia. Configura **"Acciones de umbral"** para recibir notificaciones por correo electrónico cuando tu gasto alcance un porcentaje de tu presupuesto (ej. al 50%, 90% y 100%).

### 2. Limitar el Escalado del Servicio (Cloud Run)

Para prevenir que un pico de tráfico (malicioso o viral) dispare tus costos, puedes limitar el número máximo de "instancias" que tu aplicación puede usar.

**Comando para limitar las instancias:**

Este comando actualiza tu servicio para que nunca escale a más de 2 instancias simultáneamente. Este es un límite seguro para una aplicación de demo.

```bash
gcloud run services update tickethome-demo --region us-central1 --max-instances=2
```

*   **`--max-instances=2`**: Puedes ajustar este número. Para una demo, un valor entre 1 y 5 es razonable. El valor por defecto es 100, lo cual puede ser demasiado alto si no se controla.
*   **Instancias mínimas:** Por defecto, Cloud Run escala a 0 instancias cuando no hay tráfico, lo cual es ideal para no incurrir en costos innecesarios.

### 3. Implementar reCAPTCHA para Prevenir Abuso

Como bien mencionaste, una de las principales fuentes de costos inesperados por abuso proviene de bots que envían información a tus formularios (login, creación de tickets, etc.).

**Acción recomendada:**
*   **Integrar Google reCAPTCHA v3:** Esta versión es invisible para los usuarios y no interrumpe la experiencia. Analiza el comportamiento y asigna una puntuación a cada petición. En tu backend (la aplicación Flask), puedes verificar esta puntuación y decidir si procesas la petición o la rechazas.
*   Esto requiere añadir lógica tanto en el frontend (HTML/JavaScript) como en el backend (Python), pero es la mejor defensa contra el abuso automatizado a nivel de aplicación.

### 4. (Avanzado) Google Cloud Armor

Si en el futuro la aplicación crece y requiere una capa de seguridad más robusta, puedes considerar **Google Cloud Armor**. Es un servicio de seguridad que se integra con el balanceador de carga de Google y ayuda a proteger tus aplicaciones contra ataques de denegación de servicio (DDoS) y otras amenazas web. Para una demo, no es necesario, pero es bueno conocer su existencia.
