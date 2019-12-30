import RPi.GPIO as GPIO
import json
import os
import time
from flask import Flask
from flask import request
from flask import make_response
import threading
import pygame

app = Flask(__name__)

#### PIN OUTPUT STUFF ####
#GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
litePIN=16 #light pin
dispPIN = 21 #dispense pin
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(dispPIN, GPIO.OUT)
GPIO.setup(litePIN, GPIO.OUT)

@app.route('/',methods=['POST'])
def index():
    req = request.get_json(silent=True, force=True)
    val = processRequest(req)
    #print(val)
    r = make_response(json.dumps(val))
    r.headers['Content-Type'] = 'application/json'
    return r

def dispenseTreat(secs):
        GPIO.output(litePIN, True)
        time.sleep(.5)  #wait for assistant to finish response
        GPIO.output(dispPIN, True)
        time.sleep(secs)  #time alotted for treat dispensing
        GPIO.output(dispPIN, False)
        time.sleep(5)
        GPIO.output(litePIN,False)

def waitHour():
        print('ifttt command received: 1hr treats')
        time.sleep(3600)
        dispenseTreat(.1)

def processRequest(req):
    device = req['device']
    state = json.loads(req['state'])
    print(state)
    
    if device=='few_treats':
        #GPIO.output(16, state) ## State is true/false
        print('ifttt command received: few treats')
        dispenseTreat(.1)

    elif device=='many_treats':
        print('ifttt command received: many treats')
        dispenseTreat(.4)
    
    elif device=='1hr_treats':
        t1=threading.Thread(target=waitHour)
        t1.start()
        #t1.join()
        #waitHour()
        
    elif device=='light':
        print('ifttt command received: light on')
        GPIO.output(litePIN, True)
        time.sleep(5)
        GPIO.output(litePIN, False)
    
    elif device =='ringtone':
        
        pygame.init()
        pygame.mixer.music.load("tron.wav")
        pygame.mixer.music.play()

    return {
    "speech": "it is done",
    "displayText": "it is done",
    "source": "apiai-weather-webhook-sample"
    }

if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5000)