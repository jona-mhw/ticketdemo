# Flujo de Trabajo con Git para Tickethome App

Esta guía describe el paso a paso para guardar y subir tus cambios al repositorio de GitHub una vez que has finalizado una tarea o ajuste en el código.

## ¿Qué significan los colores y letras en Visual Studio Code?

Cuando trabajas con Git en VS Code, verás letras y colores junto a tus archivos. Esto te da información rápida sobre su estado:

*   **U (Verde):** **Untracked** (No rastreado). Es un archivo completamente nuevo que Git aún no conoce.
*   **M (Amarillo):** **Modified** (Modificado). Es un archivo que ya existía en Git y que has editado.
*   **D (Rojo):** **Deleted** (Eliminado). Es un archivo que has borrado.
*   **A (Verde):** **Added** (Añadido). Es un archivo nuevo que ya has añadido al "staging area" con `git add`.

---

## Pasos a seguir para guardar cambios

Sigue estos pasos en orden cada vez que termines de trabajar en una funcionalidad o corrección.

### 1. Revisa el estado de tus cambios

Antes de guardar, mira qué has modificado.

```bash
git status
```

### 2. Prepara los archivos para guardarlos (Staging)

Añade los cambios que quieres guardar en tu próxima "instantánea". Para añadir todo lo que has cambiado:

```bash
git add .
```

### 3. Guarda los cambios en tu historial local (Commit)

Crea la "instantánea" con un mensaje que describa **qué hiciste**. **Esto lo harás muchas veces.** Cada commit es un pequeño paso en tu proyecto.

```bash
git commit -m "Un mensaje descriptivo de tus cambios"
```

### 4. Sube tus cambios a GitHub (Push)

Sube tus cambios guardados a la nube (GitHub).

```bash
git push origin master
```

**Nota:** Desde la página de GitHub, puedes hacer clic en la sección de "Commits" y descargar un ZIP de **cualquier** commit que hayas subido, no necesitas un tag para eso.

---

## ¿Cómo crear y gestionar versiones (Tags)?

Un **Tag** es una etiqueta especial para un commit **muy importante**. No se crea un tag para cada cambio, sino para marcar un hito o una versión estable que estás listo para desplegar.

### Nombrando tus versiones

Usa un sistema llamado **Versionamiento Semántico (Semantic Versioning)**. El formato es `vMAJOR.MINOR.PATCH`.

*   **MAJOR (v1.0.0):** Para cambios grandes que rompen la compatibilidad.
*   **MINOR (v1.1.0):** Para nuevas funcionalidades compatibles.
*   **PATCH (v1.0.1):** Para correcciones de errores compatibles.

### Comando para crear una nueva versión

Para crear el tag:

```bash
# Plantilla: git tag -a vMAJOR.MINOR.PATCH -m "Descripción de la versión"
# Ejemplo práctico:
git tag -a v1.1.0 -m "v1.1.0 - Se añade la funcionalidad de multi-clínica"
```

Para subir el tag a GitHub (¡no se suben solos!):

```bash
# Plantilla: git push origin <nombre_del_tag>
# Ejemplo práctico:
git push origin v1.1.0
```

---

## ¿Cómo "viajar en el tiempo" a una versión anterior?

Puedes revisar el código de cualquier versión anterior que hayas guardado con un tag.

### 1. Ver una versión anterior

```bash
# Ejemplo para ver la versión 1.0.0:
git checkout v1.0.0
```

**¡Importante!** Al hacer esto, entras en un estado especial ("detached HEAD"). Es perfecto para mirar código, pero **no hagas cambios aquí**.

### 2. Volver al presente (a tu código más reciente)

Cuando termines, siempre debes volver a tu rama de trabajo principal.

```bash
git checkout master
```

Este comando te devuelve al estado más actual de tu proyecto para que puedas seguir trabajando.
