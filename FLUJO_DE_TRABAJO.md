# Flujo de Trabajo: Desarrollo y Despliegue

Esta guía describe el proceso para desarrollar nuevas funcionalidades, interactuar con la base de datos (PostgreSQL en Supabase) y desplegar una nueva versión de la aplicación a Google Cloud Run.

---

## Parte 1: Desarrollo Local y Gestión de la Base de Datos

El entorno de desarrollo local se conecta a una base de datos PostgreSQL hosteada en Supabase. Esto centraliza la información y asegura consistencia entre el desarrollo y la producción.

### Flujo de Desarrollo

1.  **Configurar el Entorno Local (Solo la primera vez):**
    *   Crea un archivo llamado `.env` en la raíz del proyecto.
    *   Añade una línea a este archivo con tu credencial de la base de datos:
        `DATABASE_URL="[TU_DATABASE_URL_DE_SUPABASE]"`
    *   **Importante:** Reemplaza `[TU_DATABASE_URL_DE_SUPABASE]` con el valor real que obtienes de tu panel de Supabase. El archivo `.env` es ignorado por Git, por lo que tus secretos no se subirán al repositorio.

2.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Ejecutar la Aplicación Localmente:**
    ```bash
    flask run
    ```
    La aplicación leerá la variable `DATABASE_URL` desde tu archivo `.env` y se conectará a Supabase.

### Gestión de la Base de Datos (Supabase)

Para inicializar o resetear la base de datos, la aplicación utiliza comandos de Flask que operan directamente sobre tu instancia remota en Supabase.

*   **`flask init-db`**: Crea las tablas y las puebla con datos iniciales.
*   **`flask reset-db`**: **¡CUIDADO!** Borra **TODOS** los datos y vuelve a poblarlos. Úsalo con precaución.

```bash
# Para borrar toda la data y empezar de cero
flask reset-db
```

---

## Parte 2: Cómo Desplegar una Nueva Versión a Cloud Run

El despliegue consiste en enviar el código a Google Cloud Run y configurar el servicio para que pueda conectarse a la base de datos de Supabase de forma segura.

### Paso Único: Desplegar con la Variable de Entorno

Debes pasar la cadena de conexión a la aplicación en la nube a través de una variable de entorno.

**Comando de Despliegue:**
```bash
gcloud run deploy tickethome-demo --source . --region us-central1 --allow-unauthenticated --set-env-vars="DATABASE_URL=[TU_DATABASE_URL_DE_SUPABASE]"
```

**Importante:** Al igual que en el entorno local, reemplaza `[TU_DATABASE_URL_DE_SUPABASE]` con tu credencial real de Supabase.

### Desglose del Comando

-   `--set-env-vars="DATABASE_URL=..."`: **(Crucial y Obligatorio)** Inyecta de forma segura la credencial de la base de datos en el entorno de producción.

---

## Parte 3: Cómo Gestionar el Código con Git

Este flujo no cambia. Sigue siendo la mejor manera de mantener un historial de cambios ordenado.

1.  **Revisar Cambios:** `git status`
2.  **Añadir Cambios:** `git add .`
3.  **Crear un Commit:** `git commit -m "Un mensaje claro sobre el cambio"`
4.  **Subir Cambios a GitHub:** `git push origin master`
