# SmartBoocha
## Micropython / MQTT ESP32 Sensor

A script for taking temperature & humidity sensor readings using an ESP32 board, Micropython, DHT-22 sensor, and logging information via MQTT

## Components
- DHT-22 Temperature / Humidity Sensor
- ESP32 Development Board running Micropython
    - ESPTools for Micropython: https://docs.micropython.org/en/latest/esp32/tutorial/intro.html#deploying-the-firmware
- MQTT Broker
    - Home Assistant was used as a local broker for SmartBoocha project
    - http://test.mosquitto.org/ is a public MQTT available for experimenting with the platform 
- MQTT Client
    - NodeRED MQTT Dashboard for Android & IOT allows for subscribing to MQTT topics via a local broker 
    