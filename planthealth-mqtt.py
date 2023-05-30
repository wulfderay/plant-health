import serial
import json
import paho.mqtt.client as mqtt
from time import sleep
import os
# Serial port settings
serial_port = '/dev/ttyACM0'
baud_rate = 9600

# MQTT settings
mqtt_broker = 'localhost'
mqtt_port = 1883
mqtt_topic = 'plant'
username = 'mqtt_user'
password = 'S4d13fr4'


def parse_json_status(json_string):
    try:
        data = json.loads(json_string)
        return data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    print("message qos= ", message.qos)
    print("message retain= ", message.retain)
    if message.topic == mqtt_topic+ "/soil/moisture/setMaxValue":
        ser.write(('set_max '+str(message.payload.decode("utf-8"))).encode('utf-8'))
    if message.topic == mqtt_topic+ "/soil/moisture/setMinValue":
        ser.write(('set_min '+str(message.payload.decode("utf-8"))).encode('utf-8'))

# Connect to MQTT broker
client = mqtt.Client()
client.username_pw_set(username=username, password=password)
client.connect(mqtt_broker, mqtt_port)
client.on_message=on_message
client.subscribe(mqtt_topic+ "/soil/moisture/setMaxValue");
client.subscribe(mqtt_topic+"/soil/moisture/setMinValue");
status = ''
need_to_reconnect = True
skips = 0 # only publish 1/5 the data
datarate_denominator = 5
# Loop to read and publish data
client.loop_start()
while True:
    try:
        if not os.path.exists(serial_port):
            print(f"Serial Port '{serial_port}' does not exist. Please plug in plant monitor device!")
            client.publish(mqtt_topic+ "/status", payload="Plant Monitor Unplugged", retain=True)
            sleep(5)
            continue
        if need_to_reconnect:
            # Create serial object
            ser = serial.Serial(serial_port, baud_rate)
            need_to_reconnect = False
        # Read data from serial port
        data = ser.readline().strip().decode()
        #client.publish('plant/debug' , payload=data, retain=True)
        parsed_data = parse_json_status(data)
        skips = skips + 1
        if skips > datarate_denominator:
            skips = 0
        if parsed_data and skips == 0:
            client.publish(mqtt_topic+ "/status", payload=parsed_data['statusMessage'], retain=True)
            client.publish(mqtt_topic+ "/humidity", payload=parsed_data['humidity'], retain=True)
            client.publish(mqtt_topic+ "/temperature", payload=parsed_data['temperature'], retain=True)
            client.publish(mqtt_topic+ "/soil/moisture", payload=parsed_data['moisturePercentage'], retain=True)
            client.publish(mqtt_topic+ "/soil/moisture/maxValue", payload=parsed_data['maxValue'], retain=True)
            client.publish(mqtt_topic+ "/soil/moisture/minValue", payload=parsed_data['minValue'], retain=True)
            client.publish(mqtt_topic+ "/soil/moisture/raw", payload=parsed_data['moistureValue'], retain=True)
        if not parsed_data:
            client.publish(mqtt_topic + '/status', payload="Failed to parse incoming data", retain=True)
        sleep(0.5)
    except serial.SerialException:
        #close the connection to release the port
        ser.close()
        need_to_reconnect = True
        print(f"Serial port '{serial_port}' not available, retrying...")
        client.publish(mqtt_topic + '/status', payload="Serial port '{serial_port}' not available, retrying...", retain=True)
        sleep(5) # wait 5 seconds before retrying
    except Exception:
        #close connection to release the port
        ser.close()
        need_to_reconnect = True
        print(f"Unable to parse output, retrying...")
        client.publish(mqtt_topic + '/status', payload="Unable to parse output, retrying...", retain=False)
        sleep(5)
client.loop_stop()
