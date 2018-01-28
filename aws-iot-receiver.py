#!/usr/bin/env python

import paho.mqtt.client as paho
import RPi.GPIO as GPIO
import os
import socket
import ssl
import json
import time


BluePin = 33
RedPin = 35
GreenPin = 37


def blink(seconds, pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(seconds)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


def on_connect(client, userdata, flags, rc):
    print("Connection returned result: " + str(rc))
    client.subscribe("#", 1)


def on_message(client, userdata, msg):
    if msg.topic == 'rfid-out':
        payload = json.loads(msg.payload)

        if payload["is_registered"]:
            print("RECEIVER = Access Granted !")
            blink(5, GreenPin)
        else:
            print("RECEIVER - Access Denied !")
            blink(5, RedPin)

mqttc = paho.Client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

awshost = "xxxxxxxxxxx.iot.us-west-2.amazonaws.com"
awsport = 8883
clientId = "RPI-Home-Client"
thingName = "RPI-Home"
caPath = "/home/pi/iot/keys/aws-iot-rootCA.crt"
certPath = "/home/pi/iot/keys/0dba10a353-certificate.pem.crt"
keyPath = "/home/pi/iot/keys/0dba10a353-private.pem.key"

mqttc.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2,
              ciphers=None)
mqttc.connect(awshost, awsport, keepalive=60)
mqttc.loop_forever()
