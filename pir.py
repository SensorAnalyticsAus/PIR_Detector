#!/usr/bin/python

###############################################################################
#         HC-SR501 PIR MOTION DETECTOR Sensor Code for RaspberryPi 
#                       ©Sensor Analytics Australia 2024
############################################################################### 

Mute = 1     # 0 - mute, 1 - enable pushover.net sound alert and alarm 
sound_alert='tugboat'
po_token='insert your pushover app token here'  # optional
po_user='insert your pushover user key here'    # optional
TolAlert = 3 # three successive md events
TolAlarm = 7 # seven successive md events
pin = 40     #physical pin 40 (not gpio no etc) connected to pir's signal wire
LOGFILE = '/mnt/32G/log/PIR.log' # change to your preferred location

import RPi.GPIO as GPIO
import time
from datetime import datetime
import signal,sys
import json,http.client, urllib #for po
import os

def po(msg,snd): #pushover PIR_MD to send msg to mobile, change token and user
 conn = http.client.HTTPSConnection("api.pushover.net:443")
 conn.request("POST", "/1/messages.json",
 urllib.parse.urlencode({
     "token": po_token,
     "user": po_user,
     "sound": snd,
     "message": msg,
     }), { "Content-type": "application/x-www-form-urlencoded" })
 resp=conn.getresponse()
 respobj = json.loads(resp.read())
 json_formatted_str = json.dumps(respobj, indent=4)
 return json_formatted_str
def signal_handler(signal, frame):
 print('\ngotta go...')
 sys.exit(0)
def makeDir(dirpath):
 if not os.path.exists(dirpath):
     os.makedirs(dirpath)
     print(dirpath," created")
 else:
     print(dirpath," exists all good")
def writeLog(msg,log_file):
 with open(log_file,'a') as logfile:
     logfile.write(msg+'\n')
 return

signal.signal(signal.SIGINT, signal_handler)
print(datetime.now().strftime('%H:%M:%S'),'PIR Motion Detector started...')
print('ctrl-C to exit')

log_dir = os.path.dirname(LOGFILE)
makeDir(log_dir)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.IN)    
knt=0    
while True:
    now = datetime.now().strftime("%H:%M:%S")
    i=GPIO.input(pin)
    if i==1:              
        knt+=1
        print (now,'Motion Detected',i)
        if LOGFILE: writeLog(now+' Motion Detected '+str(i),LOGFILE)
        if knt == TolAlert: 
            msg=now+' Motion Detect Alert'
            print(msg)
            if LOGFILE: writeLog(msg,LOGFILE)
            if Mute == 1: po(msg,sound_alert)
        if knt == TolAlarm: 
            msg=now+' Intruder Alarm Check Cameras!'
            print(msg)
            if LOGFILE: writeLog(msg,LOGFILE)
            if Mute == 1: po(msg,'alarm')
        time.sleep(0.1)
    else: knt=0 # reset counter
    time.sleep(.5)
