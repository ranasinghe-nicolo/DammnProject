from flask import Flask
from flask_sock import Sock
import serial
import re
import json
import time
import threading

app = Flask(__name__)
sock = Sock(app)
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)

# Inizializza coords e timestamp a None
coords = None
timestamp = None

# Lista per le connessioni WebSocket attive
active_ws_connections = []

@sock.route('/coords')
def handle_ws(ws):
    """Gestisce una nuova connessione WebSocket."""
    active_ws_connections.append(ws)
    try:
        while True:
            # Se coords è ancora None, aspetta il primo dato valido
            if coords is not None:
                ws.send(json.dumps(coords))
            time.sleep(0.1)  # Evita di saturare la CPU
    except Exception as e:
        print(f"Client disconnesso: {e}")
    finally:
        active_ws_connections.remove(ws)

def run_server():
    """Loop principale per lettura seriale e invio WebSocket."""
    global coords
    global timestamp
    while True:
        try:
            # Leggi dati dalla porta seriale
            riga = ser.readline().decode("utf-8").strip()
            if riga:
                # Estrai coordinate e timestamp dal messaggio NMEA $GPGGA
                match = re.search(
                    r'\$GPGGA,(\d{6}\.\d{2}),(\d+\.\d+),([NS]),(\d+\.\d+),([EW])',
                    riga
                )
                if match:
                    # Estrai e formatta il timestamp
                    timestamp_raw = match.group(1)   # formato hhmmss.xx
                    timestamp = timestamp_raw[:6]      # prendiamo solo hhmmss
                    ore = timestamp[:2]
                    minuti = timestamp[2:4]
                    secondi = timestamp[4:6]
                    tempo_formattato = f"{ore}:{minuti}:{secondi}"
                    
                    # Converte le coordinate
                    lat = float(match.group(2)) / 100
                    if match.group(3) == 'S':
                        lat = -lat
                    lon = float(match.group(4)) / 100
                    if match.group(5) == 'W':
                        lon = -lon
                    
                    # Crea il nuovo dizionario per le coordinate
                    new_coords = {"lat": lat, "lon": lon}
                    
                    # Aggiorna coords solo se è il primo dato o se è cambiato
                    if coords != new_coords:
                        coords = new_coords
                        print(f"{coords}")
                        
                        # Invia le nuove coordinate a tutti i client WebSocket connessi
                        for ws in active_ws_connections.copy():
                            try:
                                ws.send(json.dumps(coords))
                            except Exception as e:
                                print(f"Errore nell'invio a un client: {e}")
                                active_ws_connections.remove(ws)
                        
                        # Scrive le coordinate e il timestamp nel file CSV
                        with open('report.csv', 'a', newline='') as report_file:
                            riga_csv = f"lat: {lat}, lon: {lon}, ora: {tempo_formattato}"
                            report_file.write(riga_csv + "\n")
            
            time.sleep(0.1)  # Pausa per ridurre l'uso della CPU

        except serial.SerialException as e:
            print(f"Errore seriale: {e}")
            time.sleep(1)
        except Exception as e:
            print(f"Errore: {e}")
            time.sleep(1)

if __name__ == '__main__':
    # Avvia Flask in un thread separato
    flask_thread = threading.Thread(
        target=app.run,
        kwargs={"host": "0.0.0.0", "port": 5000, "debug": False, "use_reloader": False}
    )
    flask_thread.daemon = True
    flask_thread.start()

    # Avvia il loop principale per la lettura seriale
    run_server()