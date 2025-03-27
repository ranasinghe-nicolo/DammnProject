# Importa le librerie necessarie:
from flask import Flask                 # Flask è un modo semplice per creare un sito web.
from flask_sock import Sock             # flask_sock permette di usare WebSocket, cioè un modo per comunicare in tempo reale.
import serial                           # Per leggere dati da una porta seriale (come da un dispositivo collegato).
import re                               # Serve per usare le espressioni regolari, cioè trovare schemi in un testo.
import json                             # Permette di trasformare dati in formato JSON, un formato che i computer capiscono bene.
import time                             # Per gestire il tempo, come aspettare alcuni secondi.
import threading                        # Permette di eseguire più cose contemporaneamente (multitasking).

# Crea una nuova applicazione Flask, che sarà il nostro sito web.
app = Flask(__name__)
# Crea un nuovo oggetto Sock per gestire le connessioni WebSocket.
sock = Sock(app)
# Apre una connessione seriale sulla porta '/dev/ttyACM0' con velocità 9600 baud. 
# Il timeout serve per non bloccarsi troppo a lungo se non arriva niente.
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Inizializza la variabile 'coords' a None, significa che all'inizio non ci sono coordinate.
coords = None

# Lista per tenere traccia di tutte le connessioni WebSocket attive.
active_ws_connections = []

# Questa funzione gestisce le nuove connessioni WebSocket sul percorso '/coords'.
@sock.route('/coords')
def handle_ws(ws):
    """Gestisce una nuova connessione WebSocket."""
    # Aggiunge la connessione WebSocket alla lista delle connessioni attive.
    active_ws_connections.append(ws)
    try:
        # Avvia un ciclo infinito per inviare continuamente le coordinate aggiornate.
        while True:
            # Se ci sono coordinate lette dal dispositivo, le manda al client.
            if coords is not None:
                # Converte le coordinate in formato JSON e le invia tramite il WebSocket.
                ws.send(json.dumps(coords))
            # Attende 0.1 secondi per non sovraccaricare il processore.
            time.sleep(0.1)
    except Exception as e:
        # Se c'è un errore (ad esempio il client si disconnette), stampa un messaggio.
        print(f"Client disconnesso: {e}")
    finally:
        # Rimuove la connessione dalla lista delle connessioni attive, così non ci sono errori in futuro.
        active_ws_connections.remove(ws)

# Questa funzione è il "cuore" del programma: legge dalla porta seriale e invia dati tramite WebSocket.
def run_server():
    """Loop principale per lettura seriale e invio WebSocket."""
    global coords  # Serve per modificare la variabile globale 'coords'
    while True:
        try:
            # Legge una riga di testo dalla porta seriale e la decodifica da byte a stringa.
            riga = ser.readline().decode("utf-8").strip()
            # Se la riga non è vuota...
            if riga:
                # Cerca una riga che segua lo schema dei dati GPS (GPGGA) usando le espressioni regolari.
                match = re.search(
                    r'\$GPGGA,(\d{6}),(\d{2})(\d{2}\.\d+),([NS]),(\d{3})(\d{2}\.\d+),([EW])',
                    riga
                )
                if match:
                    # Estrae il timestamp (l'ora) dal dato GPS.
                    timestamp = match.group(1)
                    # Divide il timestamp in ore, minuti e secondi.
                    ore, minuti, secondi = timestamp[:2], timestamp[2:4], timestamp[4:6]
                    # Crea una stringa formattata per mostrare l'ora.
                    tempo_formattato = f"{ore}:{minuti}:{secondi}"
                    
                    # Converte le coordinate:
                    # La latitudine viene calcolata sommando i minuti (convertiti in frazione d'ora) al valore base.
                    lat = float(match.group(2)) + (float(match.group(3)) / 60)
                    # Se il valore è nel Sud, la latitudine diventa negativa.
                    if match.group(4) == 'S':
                        lat = -lat
                    # La longitudine viene calcolata in modo simile, sommando i minuti.
                    lon = float(match.group(5)) + (float(match.group(6)) / 60)
                    # Se il valore è nell'Ovest, la longitudine diventa negativa.
                    if match.group(7) == 'W':
                        lon = -lon
                    
                    # Crea un nuovo dizionario con le coordinate e l'ora.
                    new_coords = {"lat": lat, "lon": lon, "ora": tempo_formattato}
                    
                    # Se le coordinate sono cambiate, aggiorna la variabile 'coords'
                    if coords != new_coords:
                        coords = new_coords
                        print(f"📡 Nuove coordinate inviate: {coords}")
                        
                        # Invia le nuove coordinate a tutti i client connessi via WebSocket.
                        for ws in active_ws_connections.copy():
                            try:
                                ws.send(json.dumps(coords))
                            except Exception as e:
                                # Se c'è un errore durante l'invio, stampa un messaggio e rimuove quel client.
                                print(f"Errore nell'invio a un client: {e}")
                                active_ws_connections.remove(ws)
                        # Apre (o crea se non esiste) il file 'report.csv' per aggiungere una nuova riga con i dati.
                        with open('report.csv', 'a', newline='') as report_file:
                            # Prepara la riga da scrivere con l'ora, la latitudine e la longitudine.
                            riga_csv = f"{tempo_formattato},{lat},{lon}"
                            report_file.write(riga_csv + "\n")
                            # Forza il salvataggio immediato dei dati sul file.
                            report_file.flush()

            # Aspetta 0.1 secondi per evitare di sovraccaricare la CPU.
            time.sleep(0.1)

        except serial.SerialException as e:
            # Se c'è un errore specifico con la porta seriale, lo stampa e aspetta 1 secondo.
            print(f"Errore seriale: {e}")
            time.sleep(1)
        except Exception as e:
            # Per ogni altro tipo di errore, lo stampa e aspetta 1 secondo.
            print(f"Errore: {e}")
            time.sleep(1)

# Qui inizia il programma.
if __name__ == '__main__':
    # Crea un nuovo thread per far partire il server Flask in modo separato.
    flask_thread = threading.Thread(
        target=app.run,
        kwargs={
            "host": "0.0.0.0",      # Rende il server accessibile da qualsiasi IP.
            "port": 5000,           # Usa la porta 5000.
            "debug": False,         # Non mostra il debug per motivi di sicurezza.
            "use_reloader": False   # Non riavvia automaticamente il server se il codice cambia.
        }  # Avvia il server web che gestisce le richieste HTTP e WebSocket.
    )
    # Imposta il thread come "daemon", cioè terminerà quando il programma principale si ferma.
    flask_thread.daemon = True
    # Avvia il thread del server Flask.
    flask_thread.start()

    # Avvia il ciclo principale che legge i dati dalla porta seriale e gestisce gli invii WebSocket.
    run_server()
