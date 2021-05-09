# SmartBoocha
## Micropython / MQTT ESP32 Sensor
A script for taking temperature & humidity sensor readings using an ESP32 board, Micropython, DHT-22 sensor, and logging information via MQTT

## Required Software & Components
- Linux PC for development with Python 3.6+
    - Required software: 
        - ESPTools, <code>python3 -m pip install esptool</code>
        - Adafruit-Ampy, <code>sudo python3 -m pip install adafruit-ampy</code>
        - Picocom, <code>sudo apt-get install -y picocom</code>
- DHT-22 Temperature / Humidity Sensor
- ESP32 Development Board running Micropython
    - ESP32 Micropython Documentation: https://docs.micropython.org/en/latest/esp32/tutorial/intro.html#deploying-the-firmware
    - MicroPython image for ESP32 board: https://micropython.org/download/esp32/
- MQTT Broker
    - Home Assistant was used as a local broker for SmartBoocha project
    - http://test.mosquitto.org/ is a public MQTT available for experimenting with the platform 
- _Recommended: MQTT Client_
    - NodeRED MQTT Dashboard for Android & IOT allows for subscribing to MQTT topics via a local broker 

## Example Installation
- Connect ESP Board to Linux PC via USB
    - USB connection below is denoted by "/dev/ttyUSB0", exact address may differ on your device
- Micropython Installation Instructions
    - Download latest [Micropython image for ESP32](https://micropython.org/download/esp32/)
    - Run command <code>python3 -m pip install esptool</code>
    - Run command <code>esptool.py --port /dev/ttyUSB0 erase_flash</code>
    - From download location, run command <code>esptool.py -c esp32 -p /dev/ttyUSB0 write_flash -z 0x1000 esp32-idf3-20210202-v1.14.bin</code>
- Navigate to cloned repository location containing SmartBoocha boot.py and config.py files
- Set your user variables in config.py
    - <code>wifi_id</code>, your local wifi network name
    - <code>wifi_pw</code>, your local wifi network password
    - <code>mqtt_server</code>, IP of your local MQTT broker
    - <code>mqtt_auth, user</code>, username of your local MQTT broker
    - <code>mqtt_auth, pw</code>, pw of your local MQTT broker
    - <code>webrepl_pw</code>, set password to WebREPL client here
- Flash __boot__ script to ESP Board with command <code>ampy -p /dev/ttyUSB0 put boot.py</code>
    - If unable to connect, check your boards USB connection and replace "ttyUSB0" accordingly
- Flash __config__ script to ESP Board with command <code>ampy -p /dev/ttyUSB0 put config.py</code>
- Connect to <code>picocom /dev/ttyUSB0 -b115200</code> to view feed
- After disconnecting from USB, while powered, connect to ESP over WiFi with WebREPL client: http://micropython.org/webrepl/
    - Requires local ESP IP and WebREPL password, set in config.py (default: _smartboocha_)
- Connect to your MQTT topics from your MQTT client
    - Topic: home-assistant/env/kombucha/[sensor], eg home-assistant/env/kombucha/scoby
    