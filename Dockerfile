# Imagen base ligera
FROM python:3.10-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Instala dependencias de sistema necesarias para Pygame y nano
RUN apt-get update && apt-get install -y \
    python3-dev \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copia todo el proyecto
COPY . /app

# Instala dependencias de Python
RUN pip install --no-cache-dir pygame neat-python

# Comando por defecto
CMD ["bash"]
