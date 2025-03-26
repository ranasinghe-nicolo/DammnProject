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

# Inizializza coords e timestamp a None boh
coords = None

# Lista per le connessioni WebSocket attive
active_ws_connections = []

@sock.route('/coords')
def handle_ws(ws):
    """Gestisce una nuova connessione WebSocket."""
    active_ws_connections.append(ws)
    try:
        while True:
            if coords is not None:
                ws.send(json.dumps(coords))
            time.sleep(0.1)  # Evita di saturare la CPU (Resource Manager Approved)
    except Exception as e:
        print(f"Client disconnesso: {e}")
    finally:
        active_ws_connections.remove(ws)

def run_server():
    """Loop principale per lettura seriale e invio WebSocket."""
    global coords
    while True:
        try:
            riga = ser.readline().decode("utf-8").strip()
            if riga:
                match = re.search(
                    r'\$GPGGA,(\d{6}),(\d{2})(\d{2}\.\d+),([NS]),(\d{3})(\d{2}\.\d+),([EW])',
                    riga
                )
                if match:
                    # Estrai timestamp
                    timestamp = match.group(1)
                    ore, minuti, secondi = timestamp[:2], timestamp[2:4], timestamp[4:6]
                    tempo_formattato = f"{ore}:{minuti}:{secondi}"
                    
                    # Converte le coordinate
                    lat = float(match.group(2)) + (float(match.group(3)) / 60)
                    if match.group(4) == 'S':
                        lat = -lat
                    lon = float(match.group(5)) + (float(match.group(6)) / 60)
                    if match.group(7) == 'W':
                        lon = -lon
                    
                    new_coords = {"lat": lat, "lon": lon, "ora": tempo_formattato}
                    
                    if coords != new_coords:
                        coords = new_coords
                        print(f"📡 Nuove coordinate inviate: {coords}")
                        
                        for ws in active_ws_connections.copy():
                            try:
                                ws.send(json.dumps(coords))
                            except Exception as e:
                                print(f"Errore nell'invio a un client: {e}")
                                active_ws_connections.remove(ws)
                        # Scrive le cose sul coso del report.csv
                        with open('report.csv', 'a', newline='') as report_file:
                            # mand un timestamp, lat e lon
                            riga_csv = f"{tempo_formattato},{lat},{lon}"
                            report_file.write(riga_csv + "\n")
                            report_file.flush()  # lo sforza il coso a scrivere le robe 

            time.sleep(0.1)

        except serial.SerialException as e:
            print(f"Errore seriale: {e}")
            time.sleep(1)
        except Exception as e:
            print(f"Errore: {e}")
            time.sleep(1)

if __name__ == '__main__':
    flask_thread = threading.Thread(
        target=app.run,
        kwargs={"host": "0.0.0.0", "port": 5000, "debug": False, "use_reloader": False} # invia la stringa di stronzi alla porta 5000 per coso html
    )
    flask_thread.daemon = True
    flask_thread.start()

    run_server()
