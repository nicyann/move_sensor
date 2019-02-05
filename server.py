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
currentstate = 0
previousstate = 0

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template('index.html')


def message_loop():
    while True:
    # Lecture du capteur
    currentstate = GPIO.input(broche)
		 # Si le capteur est déclenché
    if currentstate == 1 and previousstate == 0:
        message = 'Mouvement détécté, ne bougez plus, les mains en l\'air'
        socketio.emit('alert', message, Broadcast=True)
        GPIO.output(18, GPIO.HIGH)
        GPIO.output(22, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(18, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        # En enregistrer l'état
        previousstate = 1
    # Si le capteur est s'est stabilisé
    elif currentstate == 0 and previousstate == 1:
        print("    Prêt")
        previousstate = 0
    # On attends 10m
    time.sleep(0.01)

# Vue que notre méthode pour lire nos message est une boucle infinie
# Elle bloquerait notre serveur. Qui ne pourrait répondre à aucune requête.
# Ici nous créons un Thread qui va permettre à notre fonction de se lancer 
# en parallèle du serveur.
read_messages = threading.Thread(target=message_loop)
read_messages.start()
