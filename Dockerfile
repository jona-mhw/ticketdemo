# Usa una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requisitos e instala las dependencias
# Se hace por separado para aprovechar el caché de Docker si no cambian las dependencias
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia los archivos y directorios de la aplicación de forma explícita
COPY app.py .
COPY config.py .
COPY models.py .
COPY commands.py .
COPY routes ./routes
COPY templates ./templates
COPY static ./static

# Expone el puerto 8080 para Gunicorn
EXPOSE 8080

# Comando para ejecutar la aplicación con Gunicorn
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:app