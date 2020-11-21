import paho.mqtt.client as mqtt
# import subprocess  # skipcq: BAN-B404
import logging
import json
import os
import re


def temperature_of_raspberry_pi():
    try:
        cpu_temp = os.popen("vcgencmd measure_temp").readline()
        cpu_temp = float(re.findall(r'\d+\.\d+', cpu_temp)[0])
    except Exception as e:
        cpu_temp = -1
        logging.error("Error Reading Temperature\n" + e)
    return cpu_temp


if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s: %(message)',
        level=logging.INFO,
        datefmt="%H:%M:%S")

    with open('include/credentials.json', 'r') as f:
        credentials = json.load(f)

    broker_address = credentials["broker_address"]
    port = credentials["port"]
    user = credentials["user"]
    password = credentials["password"]

    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(
        user, password=password)  # set username and password
    mqtt_client.connect(broker_address, port=port)

    temp_pi = temperature_of_raspberry_pi()
    if temp_pi > 0:
        mqtt_client.publish(topic=credentials['feed_topic'], payload=temp_pi)

    # deepcode ignore replace~exit~sys.exit: <please specify a reason of ignoring this>
    exit()