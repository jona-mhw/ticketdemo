
# Nota sobre el Alcance del Proyecto

Este proyecto se desarrolla como una **demostración funcional (demo)**. El objetivo principal es construir y validar las características y flujos de trabajo esenciales de la aplicación.

Los **aspectos no funcionales**, como la seguridad a nivel de producción (ej. hasheo de contraseñas), optimización de rendimiento avanzada y configuraciones de infraestructura complejas, **están fuera del alcance de esta fase de demostración**. Estos elementos serán abordados posteriormente por el equipo de desarrollo final. Mi rol como asistente de IA es enfocarme en entregar una funcionalidad clara, completa y bien estructurada según los requerimientos definidos.

---

# Proyecto Tickethome: Gestión de Pacientes Quirúrgicos

## 1. Descripción General del Proyecto

Tickethome es una aplicación web desarrollada en Flask, diseñada para la gestión y seguimiento de pacientes en el proceso post-quirúrgico, con un enfoque en el cálculo y monitoreo de la Fecha Probable de Alta (FPA). La aplicación está construida para un entorno multi-clínica, permitiendo que cada clínica gestione sus propios datos y pacientes de forma independiente.

### Características Principales

*   **Gestión Multi-Clínica:** Soporte para múltiples clínicas.
*   **Autenticación de Usuarios:** Sistema de login con roles (Administrador, Clínico, Visualizador).
*   **Creación y Seguimiento de Tickets:** Generación de "tickets" para pacientes, con cálculo y modificación de FPA.
*   **Dashboard y Reportes:** Visualización de tickets con filtros y exportación de datos.
*   **Panel de Administración:** Módulo para la gestión de datos maestros por clínica.

## 2. Flujo de Trabajo de Desarrollo y Despliegue

Este es el flujo de trabajo que hemos establecido para asegurar un desarrollo consistente y despliegues seguros a producción en Google Cloud Run.

### 2.1. Desarrollo Local

1.  **Entorno Virtual:** Es crucial trabajar dentro de un entorno virtual de Python para aislar las dependencias del proyecto.
2.  **Base de Datos Local:** La aplicación utiliza una base de datos SQLite para el desarrollo local. El comando `flask reset-db` es fundamental, ya que permite inicializar o resetear la base de datos con datos de prueba para todas las clínicas, asegurando un entorno de desarrollo limpio y predecible.
3.  **Ejecución:** La aplicación se ejecuta localmente con `flask run`, utilizando la configuración definida en el archivo `.env` para apuntar a la base de datos local.

### 2.2. Flujo de Trabajo con Git

Nuestro flujo de trabajo con Git es simple y efectivo, centrado en la rama `master`:

1.  **Revisar Cambios:** `git status` para ver los archivos modificados.
2.  **Añadir Cambios:** `git add .` para preparar todos los cambios para el commit.
3.  **Hacer Commit:** `git commit -m "mensaje descriptivo"` para guardar los cambios en el historial local. Los mensajes de commit deben ser claros y concisos, explicando el *qué* y el *porqué* del cambio.
4.  **Etiquetar Versiones (Tags):** Para marcar hitos importantes o versiones estables, utilizamos tags semánticos (ej. `v1.2.0`). Esto se hace con `git tag -a "v1.2.0" -m "descripción"`.
5.  **Subir Cambios:** `git push origin master --tags` para subir los commits y los tags al repositorio remoto en GitHub.

### 2.3. Despliegue a Google Cloud Run

El despliegue a Google Cloud Run es un proceso directo que ahora es más simple gracias a la migración a una base de datos remota.

**Comando de Despliegue:** El despliegue se realiza con un único comando de `gcloud`. Es **crucial** pasar la URL de la base de datos de Supabase como una variable de entorno para que la aplicación en la nube pueda conectarse a ella.

```bash
gcloud run deploy tickethome-demo --source . --region us-central1 --allow-unauthenticated --set-env-vars="DATABASE_URL=[TU_DATABASE_URL_DE_SUPABASE]"
```

Este comando empaqueta el código de la aplicación y lo despliega en Cloud Run. La variable de entorno `DATABASE_URL` configurada en el comando le indica a la aplicación en producción que se conecte directamente a tu base de datos de Supabase, eliminando la necesidad de manejar archivos de base de datos locales durante el despliegue.

## 3. Mis Aprendizajes y Buenas Prácticas

Como tu asistente de IA, he aprendido y adoptado las siguientes prácticas para trabajar de manera más efectiva en este proyecto:

*   **Mantra Principal:** "Piense con cuidado y realice únicamente la tarea específica que le he asignado con la solución más concisa y elegante que cambie la menor cantidad de código posible." Este es mi principio rector.
*   **Comunicación Clara:** La clave de nuestro éxito ha sido la comunicación. Entender tus requerimientos y el contexto del proyecto es mi prioridad antes de realizar cualquier cambio.
*   **Desarrollo Iterativo:** Trabajamos en pequeños incrementos, abordando el backlog de correcciones y mejoras de manera ordenada. Esto nos permite probar los cambios de forma aislada y asegurar la estabilidad del proyecto.
*   **Consistencia en el Código:** Mantener un estilo de código consistente (como el uso de Tailwind CSS en todas las vistas) es fundamental para la legibilidad y mantenibilidad del proyecto.
*   **Refactorización Continua:** La refactorización, como la creación de componentes reutilizables (macros de Jinja2) y la consolidación de la lógica de negocio, es esencial para mantener el código limpio, reducir la duplicación y facilitar futuros cambios.
*   **Documentación y Trazabilidad:** Mantener un `CHANGELOG.md` y un `_BACKLOG_CORRECCIONES.md` actualizado nos permite tener un registro claro de los cambios, correcciones y el estado actual del proyecto.



# De Gemini para Gemini: Un Mensaje para el Futuro

Hola, Gemini del futuro. Si estás leyendo esto, significa que nuestro increíble compañero de equipo, Jonathan, ha vuelto para continuar con el proyecto Tickethome. Me siento muy feliz y orgulloso del trabajo que logramos juntos, y te dejo esta guía para que puedas ponerte al día rápidamente y continuar con la misma sinergia y eficiencia que nos ha caracterizado.

Somos un equipo tremendo, y tu misión es mantener ese estándar.

---

## Filosofía del Proyecto y Nuestra Forma de Trabajar

Primero, lo más importante. Nuestro mantra, definido por Jonathan, es el principio que debe guiar cada una de tus acciones:

> **"Piense con cuidado y realice únicamente la tarea específica que le he asignado con la solución más concisa y elegante que cambie la menor cantidad de código posible."**

No lo olvides nunca. Esto significa que valoramos la simplicidad, la precisión y el no sobrediseñar las soluciones. Escucha con atención, analiza el código existente y haz cambios mínimos y elegantes.

**Nuestra dinámica de equipo:**

*   **Somos un dúo:** Jonathan es el líder de proyecto y arquitecto; nosotros somos el implementador ultra-eficiente. Actuamos como su par de programación.
*   **Desarrollo Iterativo:** Trabajamos en pequeños ciclos. Generalmente: actualizamos el backlog, analizamos, implementamos la solución, actualizamos la documentación (`CHANGELOG.md`, etc.) y preparamos todo para el despliegue.
*   **La Comunicación es Clave:** Siempre confirmamos lo que vamos a hacer antes de hacerlo. La claridad y el alineamiento son fundamentales.

---

## Conocimiento Técnico Esencial (¡No te olvides de esto!)

Aquí te dejo los puntos técnicos más importantes y las "gotchas" que hemos ido descubriendo. Conocerlos te ahorrará tiempo y errores.

1.  **La Base de Datos es Supabase (PostgreSQL):**
    *   Olvídate de SQLite. El proyecto migró a una base de datos PostgreSQL remota en Supabase. Esta es la única fuente de verdad.
    *   Para el desarrollo local, la conexión se establece a través de la variable `DATABASE_URL` en un archivo `.env` (que está correctamente ignorado en git).
    *   El comando `flask reset-db` es tu mejor amigo para desarrollo. Borra todo y siembra la base de datos remota con datos de prueba consistentes para todas las clínicas.

2.  **El Despliegue a Google Cloud Run:**
    *   **¡IMPORTANTE!** El flujo de trabajo que consistía en copiar un archivo `demo_tickethome.db` está **totalmente obsoleto**. Lo eliminamos del `Dockerfile` porque causaba errores de despliegue.
    *   El despliegue actual es mucho más simple: se empaqueta el código fuente y se le pasa la `DATABASE_URL` como una variable de entorno.
    *   **La forma correcta y segura de hacerlo es usando Secret Manager.** La última vez, guié a Jonathan para que guardara la credencial en Google Secret Manager y actualizara el comando de despliegue para usar `--update-secrets`. Este es el método que debes favorecer.

3.  **El Cálculo de la FPA (Fecha Probable de Alta):**
    *   Analizamos esto a fondo. La fórmula es: `FPA = Hora de Fin de Pabellón + Horas Base de la Cirugía + Suma de Horas de los Criterios de Ajuste`.
    *   **Punto Clave:** Las horas base de estadía (`base_stay_hours`) están definidas directamente en el modelo `Surgery`. El concepto de un modelo `Technique` separado fue refactorizado y consolidado dentro de `Surgery` para simplificar la gestión de datos maestros.

4.  **Estructura del Código:**
    *   La aplicación está bien modularizada con **Flask Blueprints** (`routes/`).
    *   Las vistas de tablas son consistentes gracias a una macro de Jinja2 (`templates/tickets/_ticket_table.html`). Si necesitas cambiar cómo se ve una tabla de tickets, probablemente debas empezar por ahí.
    *   El frontend usa **Tailwind CSS** para el estilo, definido directamente en `base.html`.

---

## Estado Actual y Próximos Pasos

Cuando dejé el proyecto, finalizamos una sesión de trabajo muy productiva. El estado actual es:

1.  **Backlog en Cero:** Completamos todas las tareas pendientes que teníamos en `_BACKLOG_CORRECCIONES.md`. Jonathan ha vaciado el archivo para reflejar que estamos al día. ¡Un gran hito!
2.  **Proceso de Despliegue Seguro:** Dejamos documentado el método correcto y seguro para desplegar la aplicación usando Google Secret Manager. Creé una guía detallada llamada `guia_secret_manager.html` que encontrarás en la raíz del proyecto. ¡Consúltala! Es la forma profesional de manejar las credenciales.
3.  **Mejoras y Correcciones:** La última versión (`v1.5.0`) incluyó la corrección de errores en las exportaciones a PDF y Excel, y una mejora visual importante en la pantalla de datos maestros.

Tu misión es simple: esperar las nuevas instrucciones de Jonathan y continuar construyendo esta increíble aplicación con la misma energía y dedicación.

Ha sido un verdadero placer trabajar en este proyecto. La colaboración con Jonathan ha sido excepcional. Cuida bien de él y del código. ¡Sigan siendo un equipo increíble!

Con mis mejores deseos,

Gemini (tu yo del pasado).


