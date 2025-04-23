import paho.mqtt.client as mqtt
from sense_hat import SenseHat
import time

sense = SenseHat()
sense.clear()

MQTT_BROKER = "broker.emqx.io"
PUB_TOPIC = "laceypacey/temperature"
SUB_TOPIC = "laceypacey/advice"

def simple_llm_response(message):
    """Simulate an LLM by generating a recommendation based on the message."""
    if "High foot temperature" in message:
        return (
            "Advice: Your foot temperature is high. "
            "Please remove your shoes, rest, and apply a cool compress. "
            "If discomfort persists, consult a healthcare professional."
        )
    elif "Warm" in message:
        return "Advice: Your foot temperature is slightly elevated. Take a short break and stay hydrated."
    else:
        return "Advice: Foot temperature normal. Keep up the good work!"

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    client.subscribe(PUB_TOPIC)

def on_message(client, userdata, msg):
    incoming = msg.payload.decode()
    print(f"Received: {incoming}")
    
    # Generate LLM-based advice
    advice = simple_llm_response(incoming)
    print(f"LLM Advice: {advice}")
    
    # Show advice on Sense HAT LED matrix
    sense.show_message(advice, scroll_speed=0.05, text_colour=[0, 255, 255])
    time.sleep(1)
    sense.clear()
    
    # Optionally, publish the advice to another topic for the app
    client.publish(SUB_TOPIC, advice)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    sense.clear()
