# Resumen del Proyecto Tickethome

## Descripción General

Tickethome es una aplicación web desarrollada en Flask, diseñada para la gestión y seguimiento de pacientes en el proceso post-quirúrgico. Su principal objetivo es el cálculo y monitoreo de la Fecha Probable de Alta (FPA). La aplicación está construida para un entorno multi-clínica, permitiendo que cada clínica gestione sus propios datos y pacientes de forma independiente.

### Características Principales

*   **Gestión Multi-Clínica:** Soporte para múltiples clínicas.
*   **Autenticación de Usuarios:** Sistema de login con roles (Administrador, Clínico, Visualizador).
*   **Creación y Seguimiento de Tickets:** Generación de "tickets" para pacientes, con cálculo y modificación de FPA.
*   **Dashboard y Reportes:** Visualización de tickets con filtros y exportación de datos.
*   **Panel de Administración:** Módulo para la gestión de datos maestros por clínica.

## Tecnología

La aplicación está construida con las siguientes tecnologías:

*   **Backend:** Python con el framework Flask.
*   **Base de Datos:** PostgreSQL, gestionada en Supabase.
*   **Frontend:** HTML, CSS (posiblemente con un framework como Tailwind CSS, mencionado en `gemini.md`), y JavaScript.
*   **ORM:** Flask-SQLAlchemy.
*   **Autenticación:** Flask-Login.
*   **Despliegue:** Google Cloud Run con Gunicorn como servidor WSGI.

Las dependencias de Python se gestionan a través de un archivo `requirements.txt`.

## Flujo de Trabajo

### Desarrollo Local

1.  **Entorno Virtual:** Se utiliza un entorno virtual de Python para aislar las dependencias.
2.  **Instalación de Dependencias:** Se instalan las dependencias desde `requirements.txt` con `pip install -r requirements.txt`.
3.  **Base de Datos:** La aplicación se conecta a una base de datos de desarrollo en Supabase (PostgreSQL). El comando `flask reset-db` permite inicializar o resetear la base de datos remota con datos de prueba.
4.  **Ejecución:** La aplicación se ejecuta localmente con `flask run`.

### Flujo de Trabajo con Git

Se utiliza un flujo de trabajo simple centrado en la rama `master`:

1.  **Revisar Cambios:** `git status`
2.  **Añadir Cambios:** `git add .`
3.  **Hacer Commit:** `git commit -m "mensaje descriptivo"`
4.  **Etiquetar Versiones (Opcional):** `git tag -a "v1.2.0" -m "descripción"`
5.  **Subir Cambios:** `git push origin master --tags`

### Despliegue a Google Cloud Run

El despliegue se realiza a través de un único comando de `gcloud`:

```bash
gcloud run deploy tickethome-demo --source . --region us-central1 --allow-unauthenticated --set-env-vars="DATABASE_URL=[TU_DATABASE_URL_DE_SUPABASE]"
```

Este comando empaqueta el código fuente y lo despliega en Google Cloud Run. La aplicación en producción se conecta a la base de datos de demo empaquetada en la imagen.


## Estado Actual

El proyecto ha alcanzado un hito importante con la migración de su base de datos de SQLite a PostgreSQL en Supabase y la posterior refactorización del código para mejorar la consistencia y legibilidad. La aplicación es completamente funcional y el backlog de tareas críticas de desarrollo está completo.


## Próximos Pasos

Los próximos pasos se centrarán en la mejora continua de la aplicación, incluyendo:

*   **Añadir pruebas unitarias:** Implementar pruebas para asegurar la calidad y estabilidad del código.
*   **Documentación:** Mejorar la documentación del código y de la API.
*   **Nuevas funcionalidades:** Implementar nuevas características según las necesidades del cliente.