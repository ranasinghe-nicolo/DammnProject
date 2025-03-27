# Usa un'immagine ufficiale di Python come base. 
# Questo significa che stiamo partendo da un'immagine già pronta con Python installato.
FROM python:3

# Imposta la cartella di lavoro all'interno del container su "/app".
# Tutti i comandi successivi verranno eseguiti in questa cartella.
WORKDIR /app

# Copia tutti i file e le cartelle dalla cartella corrente del tuo computer
# all'interno del container nella cartella /app.
COPY . /app

# Dice a Docker di esporre la porta 8080.
# Questo permette ad altri dispositivi di connettersi al container attraverso questa porta.
EXPOSE 8080

# Esegue il server HTTP di Python.
# Il comando avvia il modulo http.server che serve i file nella directory corrente.
# La porta 8080 è quella su cui il server ascolta le richieste.
CMD ["python3", "-m", "http.server", "8080"]
