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
port = os.environ['MQTT_PORT']

def on_message(client, userdata, message):
    print("{0}, {1}".format(message.topic, message.payload))
    ip = message.topic.split("/")[2]
    action = message.topic.split("/")[3].lower()
    data = json.loads(message.payload)
    bulb = Bulb(ip)
    if ("turn_on" == action):
        print("{0} turn_on".format(ip))
        bulb.turn_on()
    if ("turn_off" == action):
        print("{0} turn_off".format(ip))
        bulb.turn_off()
    if ("set_brightness" == action):
        print("{0} set_brightness {1}".format(ip, data))
        bulb.set_brightness(data)
    if ("toggle" == action):
        print("{0} toggle".format(ip))
        bulb.toggle()
    if ("set_rgb" == action):
        return actions.set_rgb()
        print("{0} set_rgb {1}, {2}, {3}".format(ip, data[0], data[1], data[2]))
        bulb.set_rgb(data[0], data[1], data[2])
    if ("set_hsv" == action):
        return actions.set_hsv()
        print("{0} set_hsv hue {1}, sat {2}".format(ip, data['hue'], data['sat']))
        bulb.set_hsv(data['hue'], data['sat'])
    if ("set_color_temp" == action):
        print("{0} set_color_temp {1}".format(ip, data))
        bulb.set_color_temp(data)
    if ("set_default" == action):
        print("{0} setting this setting as default".format(ip))
        bulb.set_default()
    publish.single("yeelight2mqtt/properties/{0}".format(ip), payload=bulb.get_properties(), hostname=broker, port=port)

subscribe.callback(on_message, "yeelight2mqtt/bulb/#", hostname=broker, port=port)
