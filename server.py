from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask import render_template
import time
import threading
import RPi.GPIO as GPIO

broche = 17
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(broche, GPIO.IN)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template('index.html')


def message_loop():
    currentstate = 0
    previousstate = 0
    while True:
        currentstate = GPIO.input(broche)
        if currentstate == 1 and previousstate == 0:
            message = 'Mouvement détécté, ne bougez plus, les mains en l\'air'
            socketio.emit('alert', message, Broadcast=True)
            GPIO.output(18, GPIO.HIGH)
            GPIO.output(22, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(18, GPIO.LOW)
            GPIO.output(22, GPIO.LOW)
            previousstate = 1
        elif currentstate == 0 and previousstate == 1:
            message = 'Ready to move'
            socketio.emit('alert', message, Broadcast=True)
            previousstate = 0
        time.sleep(0.01)

# Vue que notre méthode pour lire nos message est une boucle infinie
# Elle bloquerait notre serveur. Qui ne pourrait répondre à aucune requête.
# Ici nous créons un Thread qui va permettre à notre fonction de se lancer 
# en parallèle du serveur.
read_messages = threading.Thread(target=message_loop)
read_messages.start()
