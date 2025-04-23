# -*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()

MQTT_BROKER = "broker.emqx.io"
PUB_TOPIC = "laceypacey/temperature"

TEMP_NORMAL = 25
TEMP_WARNING = 30

def get_calibrated_temp():
    cpu_temp = float(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1000
    ambient_temp = sense.get_temperature()
    return ambient_temp - (cpu_temp - ambient_temp)/1.5

client = mqtt.Client()
client.connect(MQTT_BROKER, 1883, 60)
client.loop_start()

try:
    while True:
        temp = get_calibrated_temp()
        print(f"Current foot temperature: {temp:.1f} degrees C")
        if temp > TEMP_WARNING:
            client.publish(PUB_TOPIC, f"High foot temperature: {temp:.1f} degrees C")
            sense.show_message("HOT!", text_colour=[255,0,0])
        elif temp > TEMP_NORMAL:
            sense.show_message("Warm", text_colour=[255,255,0])
        else:
            sense.show_message("OK", text_colour=[0,255,0])
        time.sleep(10)
except KeyboardInterrupt:
    client.loop_stop()
    sense.clear()
