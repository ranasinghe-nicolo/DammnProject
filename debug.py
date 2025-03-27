import serial  # Importa la libreria "serial" che ci permette di comunicare con dispositivi collegati tramite porte seriali.

# Definisce la porta seriale e la velocità (baud rate)
SERIAL_PORT = "/dev/ttyACM0"  # La porta dove il dispositivo è collegato.
BAUD_RATE = 9600              # La velocità di comunicazione: 9600 baud.

try:
    # Prova ad aprire la connessione alla porta seriale con la velocità specificata.
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    # Stampa un messaggio per dire che il programma sta ascoltando sulla porta specificata.
    print(f"Listening on {SERIAL_PORT} at {BAUD_RATE} baud...\n")

    # Avvia un ciclo infinito per leggere continuamente i dati dalla porta seriale.
    while True:
        # Legge una riga di dati dalla porta seriale, la decodifica in formato testo (utf-8) e rimuove spazi extra.
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        # Se la riga non è vuota, la stampa a video.
        if line:
            print(line)  # Stampa i dati ricevuti.

except serial.SerialException as e:
    # Se c'è un errore specifico nella comunicazione seriale, stampa il messaggio di errore.
    print(f"Serial error: {e}")

except KeyboardInterrupt:
    # Se l'utente preme CTRL+C per interrompere il programma, stampa un messaggio.
    print("\nStopped by user.")

finally:
    # Infine, se la variabile "ser" esiste e la connessione è ancora aperta, la chiude.
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial connection closed.")
