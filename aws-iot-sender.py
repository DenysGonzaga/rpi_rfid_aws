#!/usr/bin/env python

import paho.mqtt.client as paho
import RPi.GPIO as GPIO
import SimpleMFRC522
import os
import socket
import logging
import ssl
from time import sleep
from random import uniform

connflag = False

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - line %(lineno)s - function %(funcName)s - '
                                  '%(message)s'))

logger.addHandler(sh)

def on_connect(client, userdata, flags, rc):
    global connflag
    connflag = True
    print("Connection returned result: " + str(rc) )

mqttc = paho.Client()
mqttc.on_connect = on_connect

awshost = "xxxxxxxxxxx.iot.us-west-2.amazonaws.com"
awsport = 8883
clientId = "RPI-Home-Client"
thingName = "RPI-Home"
caPath = "/home/pi/iot/keys/aws-iot-rootCA.crt"
certPath = "/home/pi/iot/keys/0dba10a353-certificate.pem.crt"
keyPath = "/home/pi/iot/keys/0dba10a353-private.pem.key"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
mqttc.connect(awshost, awsport, keepalive=60)
mqttc.loop_start()


def get_rfid_id():
    try:
        reader = SimpleMFRC522.SimpleMFRC522()
        id = str(reader.read()[0])
    except Exception as e:
        logger.error("Erro on RFID read : %s." % str(e))
    finally:
        GPIO.cleanup()

    return id

while True:
    logger.info("SENDER - Waiting a RFID interaction.")
    rfid_value = get_rfid_id()
    logger.info("SENDER - Waiting for a new interaction.")
    sleep(5)
    mqttc.publish("rfid", rfid_value, qos=1)
    logger.info("SENDER - Package sent to aws iot.")
