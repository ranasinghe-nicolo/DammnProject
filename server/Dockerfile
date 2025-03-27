# Questa riga indica a Docker di usare un'immagine di Python 3.9 "slim", cioè una versione leggera di Python.
FROM python:3.9-slim

# Impostiamo la cartella di lavoro dentro il container a "/app". È dove andrà a vivere il nostro codice.
WORKDIR /app

# Qui aggiorniamo il sistema e installiamo alcuni strumenti di sistema necessari per compilare alcuni pacchetti Python.
# - "build-essential" contiene strumenti di compilazione (come make) che servono per costruire software.
# - "gcc" è un compilatore per il linguaggio C.
# Dopo aver installato, puliamo la cache di apt per risparmiare spazio.
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiamo il file requirements.txt dal nostro computer nella cartella corrente del container.
COPY requirements.txt ./

# Installiamo tutte le librerie Python necessarie che sono elencate in requirements.txt.
# L'opzione "--no-cache-dir" serve per non salvare file temporanei e risparmiare spazio.
RUN pip install --no-cache-dir -r requirements.txt

# Copiamo il file server.py (il nostro script Python principale) nella cartella corrente del container.
COPY server.py ./

# Diciamo a Docker che il container ascolterà sulla porta 5000.
EXPOSE 5000

# Questa è la riga finale: quando il container parte, esegue il comando per far partire il server Python.
CMD ["python3", "server.py"]
