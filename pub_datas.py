#! /usr/bin/python3
"""
ラズベリーパイ側に置くコード
dht11 で取得したデータをjson形式にしてhost に送る
hust側とtopic を合わせる必要がある
"""
import json
import os
import time
import datetime

import paho.mqtt.client as mqtt

import RPi.GPIO as GPIO
import dht11

#MQTT Functions
def on_connect(client, userdata, flag, rc):
  print("Connected with result code " + str(rc))


def on_disconnect(client, userdata, flag, rc):
  if rc != 0:
     print("Unexpected disconnection.")

def on_publish(client, userdata, mid):
  print("publish: {0}".format(mid))

#get datas from dht11  
tempGpio = 4
GPIO.setmode(GPIO.BCM)
dhtstat = dht11.DHT11(pin = tempGpio)
while True:
    stat = dhtstat.read()
    now = str(datetime.datetime.now())[0:19]
    data = {"date_time":now, "temp":str(stat.temperature), "hdmt":str(stat.humidity)}
    if stat.temperature==0 and stat.humidity == 0:
        continue
    data = json.dumps(data)
    print("data is created"+ data )
    break
GPIO.cleanup()

#publish datas to host
host = 'PC IP adress'
port = 1883
keepalive = 60
topic = 'mqtt/test'

client = mqtt.Client()
client.connect(host, port, keepalive)
client.publish(topic, data)
print("data is published!")
time.sleep(3)

client.disconnect()
