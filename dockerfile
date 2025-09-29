FROM python:3.12-slim

# Evita buffer en logs
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala dependencias del sistema necesarias (ejemplo: WeasyPrint)
RUN apt-get update && apt-get install -y \
    gcc \
    libpango-1.0-0 \
    libcairo2 \
    libjpeg62-turbo-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el proyecto
COPY . .

# Comando por defecto: correr Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]