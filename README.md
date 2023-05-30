# plant-health
Publish Plant health monitoring from Arduino to Mqtt

## Arduino Code

The code in my MoistureSensor project is responsible for reading the sensor data and sending it to the connected computer via serial communication. It uses a resistive moisture sensor and a DHT11 temperature and humidity sensor to collect the necessary data. Make sure to upload this code to your Arduino board and connect it via USB to the computer running this code.

## Python Script

The Python script (`planthealth-mqtt.py`) is responsible for receiving the sensor data from the Arduino via serial communication, parsing the data, and publishing it over MQTT. Follow the steps below to set up and use the Python script:

### Installation
I made this to work on a Raspberry Pi. You might have success with other platforms, but YMMV.

1. Make sure you have Python 3.x installed on your computer. If not, you can download it from the official Python website: https://www.python.org/downloads/

2. Install the required Python libraries by running the following commands:
pip install pyserial
pip install paho-mqtt


### Configuration

1. Open the `planthealth-mqtt.py` script in a text editor.

2. Modify the following variables at the beginning of the script according to your setup:
- `serial_port`: The serial port to which your Arduino is connected (e.g., '/dev/ttyACM0' for Linux or 'COM3' for Windows).
- `baud_rate`: The baud rate at which the Arduino is communicating (must match the Arduino code).
- `mqtt_broker`: The address of your MQTT broker (e.g., IP address or hostname).
- `mqtt_port`: The MQTT broker port (default is 1883).
- `mqtt_topic`: The MQTT topic to which the plant health data will be published.
- `username`: (Optional) Username for MQTT broker authentication.
- `password`: (Optional) Password for MQTT broker authentication.

### Usage

1. Connect your Arduino board to your computer using a USB cable.

2. Upload the Arduino code (`plant_health.ino`) to your Arduino board.

3. Open a terminal or command prompt and navigate to the directory where the `planthealth-mqtt.py` script is located.

4. Run the Python script by executing the following command:
`python planthealth-mqtt.py`

5. The script will start listening for data from the Arduino. It will parse the data and publish it over MQTT to the specified topic.

6. Verify that the plant health data is being published to your MQTT broker. You can use MQTT client tools or libraries to subscribe to the specified topic and receive the data.

### Example: Connecting to an MQTT Broker on Raspberry Pi

1. Install an MQTT broker (such as Mosquitto) on your Raspberry Pi by running the following command:
`sudo apt-get install mosquitto`

2. Start the Mosquitto MQTT broker service:
`sudo systemctl start mosquitto`

3. In the `planthealth-mqtt.py` script, set the `mqtt_broker` variable to the IP address or hostname of your Raspberry Pi.

4. Run the Python script as mentioned in the "Usage" section.

5. On your Raspberry Pi or any other device connected to the same network, install an MQTT client library or tool (e.g., `paho-mqtt` library for Python or `mosquitto_sub` command-line tool).

6. Use the MQTT client to subscribe to the specified topic (`mqtt_topic`) and receive the plant health data being published by the Python script.

## Troubleshooting

- Ensure that the Arduino board is properly connected to your computer via USB.
- Verify that the correct serial port is configured in the Python script (`serial_port` variable).
- Make sure the required Python libraries (`pyserial` and `paho-mqtt`) are installed.
- Check the configuration of the MQTT broker and ensure that it is accessible from your computer.


