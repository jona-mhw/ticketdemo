# Flujo de Trabajo: Desarrollo y Despliegue

## Gestión de la Base de Datos para Demo

Para facilitar el desarrollo y la demostración, el proyecto utiliza un sistema de base de datos reproducible y automatizado. En lugar de mantener un archivo de base de datos estático, la base de datos se puede (re)construir desde cero con un conjunto completo de datos de muestra para todas las clínicas.

**Características Principales:**

*   **Contraseñas Simplificadas:** Todos los usuarios de prueba usan la misma contraseña: `password123`.
*   **Datos por Clínica:** Cada una de las 9 clínicas tiene su propio conjunto de usuarios, médicos, cirugías y tickets, identificados con un prefijo único (ej. `prov`, `iqui`).
*   **Usuarios de Prueba:** Se crean usuarios con roles `admin`, `clinical` y `visualizador` para cada clínica. Los nombres de usuario siguen el formato `rol_prefijo` (ej. `admin_prov`, `clinical_iqui`).

### Comandos Esenciales de Base de Datos

**1. Para Inicializar o Resetear la Base de Datos:**

Este es el comando más importante para tu flujo de trabajo local. Úsalo cada vez que quieras empezar con una base de datos limpia y completamente poblada para todas las clínicas.

```bash
flask reset-db
```

Este comando ejecuta dos acciones:
1.  `db.drop_all()`: Elimina todas las tablas existentes.
2.  `init_db_command`: Reconstruye las tablas y las puebla con los datos de muestra definidos en `commands.py`.

**2. Para Iniciar la Aplicación:**

Una vez que la base de datos está lista, inicia la aplicación como de costumbre:

```bash
flask run
```

En la página de inicio de sesión, encontrarás una tabla con todos los nombres de usuario disponibles para que puedas copiar y pegar fácilmente.

---

# Flujo de Trabajo Original: Desarrollo y Despliegue

Esta guía describe el proceso para desarrollar nuevas funcionalidades en tu entorno local y cómo desplegar una nueva versión de la aplicación a Google Cloud Run de forma segura y eficiente.

---

## Parte 1: Cómo Desarrollar Nuevas Funcionalidades (Local)

Gracias a la configuración con el archivo `.env`, tu entorno de desarrollo local está aislado y apunta a tu base de datos de trabajo (`instance/tickethome.db`), permitiéndote probar cambios sin afectar la configuración de producción.

**Tu flujo de trabajo para añadir o modificar funcionalidades es el siguiente:**

1.  **Instalar Dependencias (si es necesario):** Si clonas el proyecto en una nueva máquina o hay nuevas librerías en `requirements.txt`, asegúrate de instalarlas.
    ```bash
    pip install -r requirements.txt
    ```

2.  **Verificar el archivo `.env`:** Asegúrate de que el archivo `.env` que creamos exista en la raíz del proyecto. Su contenido debe ser:
    ```
    # Variables de entorno para desarrollo local
    FLASK_ENV=development
    FLASK_DEBUG=True
    DATABASE_URL=sqlite:///instance/tickethome.db
    ```

3.  **Ejecutar la Aplicación Localmente:** Inicia la aplicación como siempre lo has hecho.
    ```bash
    python app.py
    ```
    La aplicación se iniciará en modo de depuración y se conectará automáticamente a `instance/tickethome.db` gracias a la variable `DATABASE_URL` en tu archivo `.env`.

4.  **Desarrollar y Probar:** Ahora puedes modificar tu código, añadir nuevas rutas, cambiar plantillas, etc. Guarda los cambios y prueba directamente en tu navegador local (`http://127.0.0.1:5000`).

---

## Parte 2: Cómo Desplegar una Nueva Versión a Cloud Run

Una vez que has terminado de desarrollar y probar una nueva funcionalidad en tu entorno local, estás listo para actualizar la aplicación en la nube.

Sigue estos pasos:

### Paso 1 (Crucial): Actualizar la Base de Datos de la Demo

**Si has hecho cambios en tu base de datos local** (nuevas tablas, columnas, registros de ejemplo, etc.) y quieres que se reflejen en la demo, **DEBES** actualizar el archivo `demo_tickethome.db` **ANTES** de desplegar.

La base de datos en la nube **NO** se actualiza automáticamente. El despliegue solo incluye la versión de `demo_tickethome.db` que existe en tu PC en ese momento.

Ejecuta este comando en tu terminal para copiar tu base de datos de desarrollo sobre la de la demo:

```powershell
Copy-Item -Path .\instance\tickethome.db -Destination .\demo_tickethome.db -Force; 
Write-Host "Base de datos demo_tickethome.db actualizada exitosamente."
```

### Paso 2: Desplegar la Aplicación

Con la base de datos de demo ya actualizada, ejecuta el comando de despliegue. Este empaquetará tu nuevo código y la nueva versión de la base de datos.

**Comando de Despliegue (Úsalo siempre para actualizar):**


```bash
gcloud run deploy tickethome-demo --source . --region us-central1 --allow-unauthenticated --set-env-vars="DATABASE_URL=sqlite:////app/demo_tickethome.db"
```

### Desglose del Comando

-   `gcloud run deploy tickethome-demo`: Despliega al servicio llamado `tickethome-demo`.
-   `--source .`: Usa el código del directorio actual.
-   `--allow-unauthenticated`: Mantiene el servicio público.
-   `--set-env-vars="DATABASE_URL=..."`: **Esta es la parte clave.** Establece la variable de entorno `DATABASE_URL` **solo para el entorno de Cloud Run**. Le dice a la aplicación en la nube que debe usar la base de datos de demostración que está empaquetada dentro del contenedor en la ruta absoluta `/app/demo_tickethome.db`.

### ¿Por Qué Este Flujo es Mejor?

-   **Cero Cambios en el Código:** No necesitas modificar `config.py` ni ningún otro archivo para pasar de desarrollo a producción. El mismo código funciona en ambos entornos.
-   **Configuración Explícita:** La configuración de cada entorno (local y producción) es explícita y está separada. La local en `.env` y la de producción en el comando de despliegue.
-   **Flexibilidad a Futuro:** Si mañana decides usar una base de datos en la nube (como Cloud SQL), solo necesitarás cambiar el valor de `DATABASE_URL` en el comando de despliegue, sin tocar una sola línea de tu aplicación.