FROM python:3.13-alpine

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements.txt e instalar dependencias
COPY requirements.txt .
RUN pip install --default-timeout=100 --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

EXPOSE 5000

CMD ["python", "run.py"]
# Si luego usas Gunicorn en producción, descomenta:
# CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
