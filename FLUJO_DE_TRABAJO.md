# Flujo de Trabajo: Desarrollo y Despliegue

Esta guía describe el proceso para desarrollar nuevas funcionalidades en tu entorno local y cómo desplegar una nueva versión de la aplicación a Google Cloud Run de forma segura y eficiente.

---

## Parte 1: Cómo Desarrollar Nuevas Funcionalidades (Local)

Tu entorno de desarrollo local está configurado para ser independiente y seguro, utilizando la base de datos de trabajo `instance/tickethome.db`.

**Tu flujo de trabajo para añadir o modificar funcionalidades es el siguiente:**

1.  **Instalar Dependencias (si es necesario):** Si clonas el proyecto o se añaden nuevas librerías, asegúrate de instalarlas.
    ```bash
    pip install -r requirements.txt
    ```

2.  **Ejecutar la Aplicación Localmente:** Inicia la aplicación con el comando habitual.
    ```bash
    flask run
    ```
    La aplicación se iniciará en modo de depuración y se conectará automáticamente a `instance/tickethome.db`.

3.  **Desarrollar y Probar:** Modifica tu código, añade nuevas rutas, cambia plantillas, etc. Guarda los cambios y prueba directamente en tu navegador local (`http://127.0.0.1:5000`).

---

## Parte 2: Cómo Desplegar una Nueva Versión a Cloud Run

Una vez que has terminado de desarrollar y probar una nueva funcionalidad, estás listo para actualizar la aplicación en la nube. **Gracias a los últimos ajustes, el proceso es ahora más directo y seguro.**

### Paso Único: Desplegar la Aplicación

**Ya no es necesario copiar manualmente la base de datos.** El proceso de despliegue ahora incluye automáticamente el contenido del directorio `instance`, asegurando que la base de datos (`tickethome.db`) esté siempre actualizada.

Simplemente ejecuta el siguiente comando para desplegar:

**Comando de Despliegue (Úsalo siempre para actualizar):**
```bash
gcloud run deploy tickethome-demo --source . --region us-central1 --allow-unauthenticated
```

### Desglose del Comando

-   `gcloud run deploy tickethome-demo`: Despliega al servicio llamado `tickethome-demo`.
-   `--source .`: Usa el código del directorio actual para construir la imagen del contenedor.
-   `--allow-unauthenticated`: Mantiene el servicio público para la demo.

Como puedes ver, ya no se necesita el argumento `--set-env-vars`. La aplicación está configurada para encontrar la base de datos en la ruta correcta de forma automática.

### Cómo Revisar los Logs en Cloud Run

Si el despliegue falla o la aplicación no se comporta como esperas, puedes revisar los logs directamente desde la terminal con este comando:

```bash
gcloud logging read 'resource.type="cloud_run_revision" AND resource.labels.service_name="tickethome-demo"' --limit=20
```

### ¿Por Qué Este Flujo es Mejor?

-   **Cero Pasos Manuales:** Se elimina el riesgo de olvidar copiar la base de datos antes de desplegar.
-   **Consistencia:** La estructura de archivos (con la base de datos dentro de `instance/`) es idéntica en tu entorno local y en la nube.
-   **Simplicidad:** El comando de despliegue es más limpio, más corto y más fácil de recordar.
-   **Flexibilidad a Futuro:** Si mañana decides usar una base de datos en la nube (como Cloud SQL), solo necesitarás **volver a añadir** el argumento `--set-env-vars` apuntando a la nueva base de datos, sin tocar una sola línea de tu aplicación.

---

## Parte 3: Cómo Gestionar el Código con Git

Para mantener un historial de cambios ordenado y colaborar de manera efectiva, seguimos un flujo de trabajo simple con Git.

1.  **Revisar Cambios:** Antes de hacer nada, revisa los archivos que has modificado.
    ```bash
    git status
    ```

2.  **Añadir Cambios al Staging:** Prepara todos tus cambios para el commit.
    ```bash
    git add .
    ```

3.  **Crear un Commit:** Guarda tus cambios en el historial local con un mensaje descriptivo.
    ```bash
    git commit -m "Un mensaje claro sobre el cambio"
    ```

4.  **Crear un Tag (Opcional pero Recomendado):** Para marcar versiones importantes, crea un tag. Reemplaza los espacios en el nombre del tag con guiones.
    ```bash
    git tag -a "v1.2.0-nombre-descriptivo" -m "Descripción del tag"
    ```

5.  **Subir Cambios a GitHub:** Envía tus commits y tags al repositorio remoto.
    ```bash
    git push origin master --tags
    ```