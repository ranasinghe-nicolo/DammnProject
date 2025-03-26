FROM python:3.9-slim

WORKDIR /app

# Installiamo dipendenze di sistema necessarie per la compilazione
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py ./

EXPOSE 5000

CMD ["python3", "server.py"]
