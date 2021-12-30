import atomic_store
import paho.mqtt.client as mqtt
import json
import time


def publishDT():
    with atomic_store.open('src/resources/digital_twin.json', default=dict()) as store:
        dt = store.value
        return json.dumps(dt)


if __name__ == '__main__':
    client = mqtt.Client("MIA")
    client.connect("mqtt.localhost", 1883)
    while True:
        client.publish("house/mia", publishDT())
        time.sleep(1)
