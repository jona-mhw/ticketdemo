# Tickethome - Gestión de Pacientes Quirúrgicos

Tickethome es una aplicación web desarrollada en Flask, diseñada para la gestión y seguimiento de pacientes en el proceso post-quirúrgico, con un enfoque en el cálculo y monitoreo de la Fecha Probable de Alta (FPA).

La aplicación está pensada para un entorno multi-clínica, donde cada clínica gestiona sus propios datos maestros (doctores, cirugías, etc.) y pacientes de forma aislada.

---

## Características Principales

*   **Gestión Multi-Clínica:** Soporte para múltiples clínicas, cada una con sus propios recursos y usuarios.
*   **Autenticación de Usuarios:** Sistema de login con roles (Administrador, Clínico, Visualizador).
*   **Creación de Tickets:** Generación de "tickets" para pacientes post-quirúrgicos, calculando automáticamente la FPA inicial basada en la cirugía, técnica y criterios de ajuste.
*   **Seguimiento de FPA:** Permite hasta 5 modificaciones de la FPA por ticket, guardando un historial de cada cambio.
*   **Dashboard de Tickets:** Visualización de todos los tickets con filtros por estado, paciente, cirugía, fecha y cumplimiento (si el alta fue dentro o fuera de la FPA).
*   **Panel de Administración:** Módulo para que los administradores gestionen los datos maestros de su clínica, incluyendo:
    *   Usuarios
    *   Clínicas (solo super-admin)
    *   Doctores
    *   Cirugías y Técnicas asociadas
    *   Criterios de ajuste de estancia
    *   Razones estandarizadas para modificaciones, anulaciones y cierres.
*   **Exportación de Datos:** Generación de reportes de tickets en formato PDF y Excel.

---

## Tecnologías Utilizadas

*   **Backend:** Python con Flask
*   **Base de Datos:** SQLAlchemy para el ORM (compatible con SQLite, PostgreSQL, etc.)
*   **Autenticación:** Flask-Login
*   **Frontend:** Jinja2 para las plantillas, con HTML, CSS y JavaScript.
*   **Dependencias:** Ver `requirements.txt` para la lista completa.

---

## Instalación y Ejecución Local

Sigue estos pasos para levantar el proyecto en tu máquina local.

1.  **Clonar el repositorio (si es necesario):**
    ```bash
    git clone https://github.com/jona-mhw/ticketdemo.git
    cd ticketdemo
    ```

2.  **Crear y activar un entorno virtual:**
    ```bash
    # En Windows
    python -m venv .venv
    .venv\Scripts\activate

    # En macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instalar las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar la base de datos:**
    *   La aplicación está configurada para usar una base de datos SQLite (`instance/tickethome.db`) por defecto.
    *   La primera vez que ejecutes la aplicación, necesitas crear las tablas. Abre una terminal y ejecuta los siguientes comandos de Flask:
    ```bash
    flask db-init
    ```

5.  **Crear un usuario administrador (si es la primera vez):**
    *   Usa el comando personalizado de Flask para crear el primer usuario y la primera clínica.
    ```bash
    flask create-admin --username tu_admin --password tu_clave --email tu_email@dominio.com --clinic "Nombre de la Clínica"
    ```

6.  **Ejecutar la aplicación:**
    ```bash
    flask run
    ```

7.  Abre tu navegador y ve a `http://127.0.0.1:5000` para ver la aplicación.
