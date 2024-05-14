from classes.EnvironmentalSensor import EnvironmentalSensor
from classes.InfluxDBManager import InfluxDBManager
from classes.SensorManager import SensorManager
from sense_hat import SenseHat
from dotenv import load_dotenv
import os

import time
import logging
import signal
import sys

#TODO
# add error handling for the InfluxDBManager class
# add error handling for loading the .env file
# Move os.environ.get() calls to better places

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
SENSOR_CONFIG_FILENAME = os.environ.get("SENSOR_CONFIG_FILENAME")
SAMPLE_PERIOD = os.environ.get("SAMPLE_PERIOD")
RECONNECT_INTERVAL = os.environ.get("RECONNECT_INTERVAL")
URL = os.environ.get("URL")
TOKEN = os.environ.get("TOKEN")
ORG = os.environ.get("ORG")
BUCKET = os.environ.get("BUCKET")

def graceful_exit(signum, frame):
    logging.info("Quitting....")
    sys.exit(0)

if __name__ == '__main__':
    validateSensor = EnvironmentalSensor()
    senseHat = SenseHat()
    sensor_manager = SensorManager(senseHat)

    print(f"DOTENV INFLUX CONFIG: {URL}, {TOKEN}, {ORG}, {BUCKET}")

    influx_manager = InfluxDBManager(URL, TOKEN, ORG)
    client = influx_manager.initialize_client()
    

    # Set up signal handling
    signal.signal(signal.SIGTERM, graceful_exit)
    signal.signal(signal.SIGINT, graceful_exit)

    try:
        while True:
            if client is None:
                client = influx_manager.initialize_client()
                if client is None:
                    logging.error("Unable to connect. Retrying in {} seconds...".format(RECONNECT_INTERVAL))
                    time.sleep(RECONNECT_INTERVAL)
                    continue

            # Prepare your data points
            w_data = SensorManager.get_1w_data(senseHat)
            sensehat_data = SensorManager.get_sensehat_data(senseHat)
            data_points = w_data + sensehat_data

            if len(data_points) == 0:
                logging.error("No data points to write.")
                time.sleep(SAMPLE_PERIOD)
                continue

            # Attempt to write data
            if not influx_manager.write_data(client, BUCKET, data_points):
                logging.error("Write failed, attempting to reinitialize client.")
                client.close()
                client = None
            
            time.sleep(SAMPLE_PERIOD)  

    except KeyboardInterrupt:
        print ("Program stopped by keyboard interrupt [CTRL_C] by user. ")

    finally:
        influx_manager.close()
        graceful_exit() 