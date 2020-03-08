#!/usr/bin/env python

import os
import datetime
import json
import socket
import sys
import time
#import paho.mqtt.client as paho
import paho.mqtt.subscribe as subscribe
from yeelight import Bulb

broker = os.environ['MQTT_HOST']
port = os.environ['MQTT_PORT']
#print("{0}:{1}".format(broker, port))

#def on_publish(client, userdata, result):  # create function for callback
#    pass

class BulbActions(object):
    def __init__(self, ip):
        self.ip = ip
        self.bulb = Bulb(self.ip)

    def turn_on(self):
        print("{0} turn_on".format(self.ip))
        self.bulb.turn_on()

    def turn_off(self):
        print("{0} turn_off".format(self.ip))
        self.bulb.turn_off()

    def set_brightness(self, percent):
        print("{0} set_brightness {1}".format(self.ip, percent))
        self.bulb.set_brightness(percent)
        print(self.bulb.get_properties())

    def toggle(self):
        print("{0} toggle".format(self.ip))
        self.bulb.toggle()

    def set_rgb(self, r, g, b):
        print("{0} set_rgb {1}, {2}, {3}".format(self.ip, r, g, b))
        self.bulb.set_rgb(r, g, b)

    def set_hsv(self, hue, sat):
       print("{0} set_hsv hue {1}, sat {2}".format(self.ip, hue, sat))
       self.bulb.set_hsv(hue, sat)

    def set_color_temp(self, temp):
        print("{0} set_color_temp {1}".format(self.ip, temp))
        self.bulb.set_color_temp(temp)

    def set_default(self):
        print("{0} setting this setting as default".format(self.ip))
        self.bulb.set_default()

def on_message(client, userdata, message):
    print("{0}, {1}".format(message.topic, message.payload))
    bulbip = message.topic.split("/")[2]
    action = message.topic.split("/")[3].lower()
    data = json.loads(message.payload)
    actions = BulbActions(bulbip)
    if ("turn_on" == action):
	return actions.turn_on()
    if ("turn_off" == action):
        return actions.turn_off()
    if ("set_brightness" == action):
        return actions.set_brightness(data)
    if ("toggle" == action):
        return actions.toggle()
    if ("set_rgb" == action):
        return actions.set_rgb(data[0], data[1], data[2])
    if ("set_hsv" == action):
        return actions.set_hsv(data['hue'], data['sat'])
    if ("set_color_temp" == action):
        return actions.set_color_temp(data)
    if ("set_default" == action):
        return actions.set_default()

#mqttclient = paho.Client("yeelight2mqtt")  # create client object
#mqttclient.on_publish = on_publish  # assign function to callback
#mqttclient.connect(broker, port)  # establish connection
#mqttclient.publish('yeelight2mqtt/message', 'waiting for input')

subscribe.callback(on_message, "yeelight2mqtt/bulb/#", hostname=broker, port=port)



