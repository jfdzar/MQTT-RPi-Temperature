import paho.mqtt.client as mqtt
import logging
import json
import os
import re
import time


def temperature_of_raspberry_pi():
    try:
        cpu_temp = os.popen("vcgencmd measure_temp").readline()
        cpu_temp = float(re.findall(r'\d+\.\d+', cpu_temp)[0])
    except Exception as e:
        cpu_temp = -1
        logging.error("Error Reading Temperature")
    return cpu_temp


def read_credentials():
    with open('include/credentials.json', 'r') as f:
        credentials = json.load(f)
    return credentials


if __name__ == '__main__':

    logging.basicConfig(
        format="%(asctime)s: %(message)s",
        # filemode='a',
        # filename='HA-Watch.log',
        level=logging.INFO,
        datefmt="%H:%M:%S")

    logging.info('Reading Credentials File')
    credentials = read_credentials()

    broker_address = credentials["broker_address"]
    port = credentials["port"]
    user = credentials["user"]
    password = credentials["password"]

    logging.info('Connecting with following parameters')
    logging.info(broker_address)
    logging.info(port)
    logging.info(user)

    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(
        user, password=password)  # set username and password
    mqtt_client.connect(broker_address, port=port)

    while(1):
        credentials = read_credentials()
        time.sleep(int(credentials['sleep_time']))
        temp_pi = temperature_of_raspberry_pi()
        logging.info('Temperature: '+str(temp_pi))
        if temp_pi > 0:
            mqtt_client.publish(
                topic=credentials['feed_topic'], payload=temp_pi)

    # deepcode ignore replace~exit~sys.exit: <please specify a reason of ignoring this>
    exit()
