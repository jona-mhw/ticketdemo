# Flujo de Trabajo con Git para Tickethome App

Esta guía describe el paso a paso para guardar y subir tus cambios al repositorio de GitHub una vez que has finalizado una tarea o ajuste en el código.

## ¿Qué significan los colores y letras en Visual Studio Code?

Cuando trabajas con Git en VS Code, verás letras y colores junto a tus archivos. Esto te da información rápida sobre su estado:

*   **U (Verde):** **Untracked** (No rastreado). Es un archivo completamente nuevo que Git aún no conoce.
*   **M (Amarillo):** **Modified** (Modificado). Es un archivo que ya existía en Git y que has editado.
*   **D (Rojo):** **Deleted** (Eliminado). Es un archivo que has borrado.
*   **A (Verde):** **Added** (Añadido). Es un archivo nuevo que ya has añadido al "staging area" con `git add`.
*   **C (Naranja):** **Conflict** (Conflicto). Ocurre en situaciones más avanzadas (fusiones de ramas). ¡No te preocupes por esto ahora!

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

Crea la "instantánea" con un mensaje que describa **qué hiciste**.

```bash
git commit -m "Un mensaje descriptivo de tus cambios"
```

**Ejemplos de buenos mensajes:**
*   `git commit -m "Feat: Agrega formulario de creación de clínicas"`
*   `git commit -m "Fix: Corrige error en el login que no permitía entrar"`
*   `git commit -m "Docs: Actualiza el flujo de trabajo de Git"`

### 4. Sube tus cambios a GitHub (Push)

Sube tus cambios guardados a la nube (GitHub).

```bash
git push origin master
```

---

## ¿Cómo crear y gestionar versiones (Tags)?

Si los cambios que hiciste son significativos (una nueva funcionalidad, una corrección importante), es una buena práctica crear una "versión" con un tag.

### Nombrando tus versiones

Usa un sistema llamado **Versionamiento Semántico (Semantic Versioning)**. El formato es `vMAJOR.MINOR.PATCH`.

*   **MAJOR (v1.0.0):** Se incrementa cuando haces cambios incompatibles con la versión anterior.
*   **MINOR (v1.1.0):** Se incrementa cuando añades una nueva funcionalidad que es compatible con lo anterior.
*   **PATCH (v1.0.1):** Se incrementa cuando haces correcciones de errores compatibles con lo anterior.

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

Para mover tu código a cómo estaba en una versión específica, usa `checkout`.

```bash
# Plantilla: git checkout <nombre_del_tag>
# Ejemplo práctico para ver la versión 1.0.0:
git checkout v1.0.0
```

**¡Importante!** Al hacer esto, entras en un estado especial llamado "detached HEAD". Es perfecto para mirar o copiar código, pero **no hagas cambios aquí**.

### 2. Volver al presente (a tu código más reciente)

Cuando hayas terminado de revisar el pasado, siempre debes volver a tu rama de trabajo principal.

```bash
git checkout master
```

Este comando te devuelve al estado más actual de tu proyecto para que puedas seguir trabajando.