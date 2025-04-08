from flask import Flask
from flask_sock import Sock
import random
import time
import threading
import json

app = Flask(__name__)
sock = Sock(app)

coords = {"lat": 45.4384, "lon": 10.9916}  # Posizione iniziale

def generate_coordinates():
    global coords
    while True:
        coords["lat"] += random.uniform(-0.001, 0.001)
        coords["lon"] += random.uniform(-0.001, 0.001)
        time.sleep(2)

threading.Thread(target=generate_coordinates, daemon=True).start()

@sock.route('/coords')
def send_coords(ws):
    while True:
        ws.send(json.dumps(coords))
        time.sleep(2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
