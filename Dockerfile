FROM python:3.12-slim

# Evita que Python escriba archivos .pyc en disco y asegura que los logs salgan inmediatamente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Instalar dependencias primero para aprovechar la cache de capas de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto, datos y archivos estáticos
COPY . .

EXPOSE 8000

# Usamos sh -c para que Render expanda la variable de entorno $PORT dinámicamente
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
