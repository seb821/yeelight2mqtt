# yeelight2mqtt

simple currently one way set yeelight bulbs.
Run with docker.

## Why?

My yeelights are in a seperate network without internet access. 
Controlling them via node-red doesn't work correctly.
Found out the python library 'Yeelight' works!

## mqtt messages

yeelight2mqtt/bulb/[ip]/[action]

actions can be:
* turn_on
* turn_off
* toggle
* set_default
* set_brightness (payload: percentage as string)
* set_rgb (payload: [r, g, b] as json)
* set_hsv (payload: [hue, sat, brightness] as json)
* set_color_temp (payload: temperature as string)

examples:
* yeelight2mqtt/bulb/192.168.55.19/turn_on
* yeelight2mqtt/bulb/192.168.55.19/set_color_temp , 4700
* yeelight2mqtt/bulb/192.168.55.19/set_rgb, [255, 80, 80]

## Run in docker
docker build . -t yeelight2mqtt

docker run --name yeelight2mqtt -e MQTT_HOST='192.168.0.210' -e MQTT_PORT='1883' yeelight2mqtt

## Resources

https://yeelight.readthedocs.io/en/latest/
