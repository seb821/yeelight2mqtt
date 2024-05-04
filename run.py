#!/usr/bin/env python

import os
import datetime
import json
import socket
import sys
import time
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
from yeelight import Bulb

broker = os.environ['MQTT_HOST']
port = int(os.environ['MQTT_PORT'])
auth = json.loads(os.environ['MQTT_AUTH'])
#broker = 'localhost'
#port = 1883
#auth = {"username":"", "password":""}

def on_message(client, userdata, message):
    print(f"topic : {message.topic}")
    print(f"payload : {message.payload} - {type(message.payload)}")
    message.payload = str(message.payload.decode("utf-8", "ignore"))
    ip = message.topic.split("/")[1]
    print(f"ip : {ip}")
    if (message.topic.split("/")[2].lower() == "cmd"):
        action = message.topic.split("/")[3].lower()
        print(f"action : {action}")
        bulb = Bulb(ip)
        if ("turn_on" == action):
            print("{0} turn_on".format(ip))
            bulb.turn_on()
        if ("turn_off" == action):
            print("{0} turn_off".format(ip))
            bulb.turn_off()
        if ("set_brightness" == action):
            data = json.loads(message.payload)
            print("{0} set_brightness {1}".format(ip, data))
            if (data == 0):
                bulb.turn_off()
            else:
                bulb.turn_on()
            bulb.set_brightness(data)
        if ("toggle" == action):
            print("{0} toggle".format(ip))
            bulb.toggle()
        if ("set_rgb" == action):
            data = json.loads(message.payload)
            print("{0} set_rgb {1}, {2}, {3}".format(ip, data[0], data[1], data[2]))
            if ( (data[0] == 0) and (data[1] == 0) and (data[2] == 0) ):
                bulb.turn_off()
            else:
                bulb.turn_on()
                bulb.set_rgb(data[0], data[1], data[2])
        if ("set_hsv" == action):
            data = json.loads(message.payload)
            print("{0} set_hsv hue {1}, sat {2}".format(ip, data['hue'], data['sat']))
            bulb.set_hsv(data['hue'], data['sat'])
        if ("set_color_temp" == action):
            data = json.loads(message.payload)
            bulb.turn_on()
            print("{0} set_color_temp {1}".format(ip, data))
            bulb.set_color_temp(data)
            bulb.set_rgb(255, 255, 255)
        if ("set_default" == action):
            print("{0} setting this setting as default".format(ip))
            bulb.set_default()
        #print(bulb.get_properties())
        payload = json.dumps(bulb.get_properties())
        publish.single("yeelight2mqtt/{0}/properties".format(ip), payload=payload, hostname=broker, port=port, auth=auth)

subscribe.callback(on_message, "yeelight2mqtt/#", hostname=broker, port=port, auth=auth)
