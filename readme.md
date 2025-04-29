# What
This project validates environmental data from a raspberry pi sense hat and one wire temperature sensors then writes them into influxDB version 3. This uses the newer flux query language and doesn't support InfluxDB version 2.

Data is validated to be in a sensible range and implausible rapid changes are rejected. This results in nice clean grafana plots.

# Why
I use the sense hat LED matrix to display the current humidity and temperature. Due to the proximity of the sense hat temperature sensor to the LED matrix this affects accuracy. The one wire sensors are more accurate and precise than the sense hat and allow logging from multiple sensors.

# To Do
This project has been working for eight months at this point so I'm unlikely to make further improvements until they become required.

add error handling for the InfluxDBManager class<br />
add error handling for loading the .env file<br />
Move os.environ.get() calls to better places<br />
Remove value in normal range messages from the validateSensor class<br />
add print for sample wait time<br />
move to venv with requirements.txt<br />

# Packages
sudo /usr/bin/python -m pip install influxdb-client<br />
sudo /usr/bin/python -m pip install w1thermsensor<br />
sudo /usr/bin/python -m pip install python-dotenv<br />