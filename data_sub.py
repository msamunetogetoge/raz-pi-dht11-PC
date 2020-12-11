"""
パソコン側に置くファイル
topic が等しいpublisher からメッセージを受け取り、fileNameにcsvを保存する
"""

import paho.mqtt.client as mqtt

import json
import os

host = '127.0.0.1'
port = 1883
keepalive = 60
topic = 'mqtt/test'
fileName = "path_to_csvfile"

def on_connect(client, userdata, flags, rc):
    print('Connected with result code ' + str(rc))
    client.subscribe(topic)

#message はjson型で送られてくる
#json.loads で辞書型にして扱う
def on_message(client, userdata, msg):
    sub_msg = json.loads(msg.payload)
    print("Subscribed! "+ msg.topic + ' ' + str(msg.payload))
    if not os.path.exists(fileName):
        Data = open(fileName, "w")
        Data.write("date_time,hmdt,temp\n")
        Data.close()
        print("csv file is created to " + fileName)
    #データの保存
    data = sub_msg.values()
    Data = open(fileName,"a")
    Data.write(",".join(map(str, data))+"\n")
    Data.close()
    print("data is saved!")


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(host, port, keepalive)

client.loop_forever()