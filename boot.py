import webrepl
import os
import dht
import machine
import time
import json
import network
import esp

from umqtt.robust import MQTTClient
import config

# Network setup
def connect():
    ''' Connect to WLAN '''
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config.wifi_id, config.wifi_pw)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

def reset():
    ''' Reboot wrapper for sanity '''
    machine.reset()

# DHT Sensor Loop
def DHT_loop():
    ''' Sensor & MQTT loop '''

    # Setup objects 
    # eg: client = MQTTClient(client_id, mqtt_server, user, password)
    client = MQTTClient(
        config.key, 
        config.mqtt_server, 
        user=config.auth['user'], 
        password=config.auth['pw']
    )

    client.connect()
    sta_if = network.WLAN(network.STA_IF)
    ip = sta_if.ifconfig()[0]
    
    LED_pin = machine.Pin(2, machine.Pin.OUT)

    # Name and connect sensors via pinout
    # Sensor names will reflect in MQTT topic
    sensor_dict = {
        'bottles':dht.DHT22(machine.Pin(4)),
        'scoby':dht.DHT22(machine.Pin(13)),
    }

    # Rolling average, filtering noise in sensors
    memory = {}
    r = 5
    error_count = 0

    while True:
        print('\n------ checking DHT22 ------')
        LED_pin.on()
        for sensor_name, sensor in sensor_dict.items():
            try:
                topic = '%s/%s'%(config.mqtt_path, sensor_name)

                # Take measurements
                sensor.measure()
                t_stamp = time.time()
                temp_F = sensor.temperature()*1.8+32
                humid = sensor.humidity()

                if not sensor_name in memory.keys():
                    w_temp = temp_F
                    w_humid = humid
                else:
                    w_temp = float(memory[sensor_name]['temperature'])
                    w_humid = float(memory[sensor_name]['humidity'])

                w_temp = (r*w_temp + temp_F) / (r+1)
                w_humid = (r*w_humid + humid) / (r+1)

                # Format information for MQTT
                env_dict = {
                    'timestamp':str(t_stamp),
                    'topic':topic,
                    'id':config.key,
                    'sensor':sensor_name,
                    'temperature':"%.2f"%w_temp,
                    'temperature_raw':"%.2f"%temp_F,
                    'humidity':"%.2f"%w_humid,
                    'humidity_raw':"%.2f"%humid,
                    'ip':ip,
                }
                print(env_dict)
                memory[sensor_name] = env_dict

                client.publish(topic, json.dumps(env_dict))
                print('------ complete, success ------\n')
                error_count = 0
                
            except Exception as e:
                print('Error on sensor %s - %s\n'%(sensor_name, e))
                print('------ complete, failed ------\n')
                error_count += 1

        # If cumulative errors, reset chip
        if error_count >= 10:
            print('Repetitive error detected, reseting chip')
            reset()

        time.sleep(0.5)
        LED_pin.off()
        time.sleep(config.refresh_delay)

# Connect to network
esp.osdebug(None)
connect()

# Start webrepl sever
webrepl.start(password=config.webrepl_pw)

# Start DHT Loop by default
DHT_loop()
