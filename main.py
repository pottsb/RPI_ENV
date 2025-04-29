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

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()
SENSOR_CONFIG_FILENAME = os.environ.get("SENSOR_CONFIG_FILENAME")
SAMPLE_PERIOD = int(os.environ.get("SAMPLE_PERIOD"))
RECONNECT_INTERVAL = int(os.environ.get("RECONNECT_INTERVAL"))
URL = os.environ.get("URL")
TOKEN = os.environ.get("TOKEN")
ORG = os.environ.get("ORG")
BUCKET = os.environ.get("BUCKET")

def graceful_exit(signum, frame):
    logging.info("Quitting....")
    sys.exit(0)

def log_temperature():
    senseHat = SenseHat()
    sensor_manager = SensorManager(senseHat)

    influx_manager = InfluxDBManager(URL, TOKEN, ORG)
    
    # Set up signal handling
    signal.signal(signal.SIGTERM, graceful_exit)
    signal.signal(signal.SIGINT, graceful_exit)

    try:
        while True:
            # Prepare your data points
            w_data = sensor_manager.get_1w_data()
            sensehat_data = sensor_manager.get_sensehat_data()
            data_points = w_data + sensehat_data

            if len(data_points) == 0:
                logging.error("No data points to write.")
                time.sleep(SAMPLE_PERIOD)
                continue

            # Attempt to write data
            if not influx_manager.write_data(BUCKET, data_points):
                logging.error("Write failed.")
                time.sleep(RECONNECT_INTERVAL)
                continue

            time.sleep(SAMPLE_PERIOD)  

    except KeyboardInterrupt:
        print ("Program stopped by keyboard interrupt [CTRL_C] by user. ")
    except Exception as e:
        print (f"An error occurred: {e}")

    finally:
        sys.exit(0) 


if __name__ == '__main__':
    log_temperature()