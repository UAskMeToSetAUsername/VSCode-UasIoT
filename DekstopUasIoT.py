import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque

# MQTT Broker settings
MQTT_SERVER = '192.168.41.73'
MQTT_PORT = 1883
DHT_TOPIC = '4173/dht'
POT_TOPIC = '4173/potensio'
DUMMY_TOPIC = '4173/dummy'

# Data storage
temperature_data = deque(maxlen=5)
potentio_data = deque(maxlen=5)
dummy_data = deque(maxlen=5)

# MQTT client callback functions
def on_connect(client, userdata, flags, rc):
    print('Connected to MQTT broker')
    client.subscribe(DHT_TOPIC)
    client.subscribe(POT_TOPIC)
    client.subscribe(DUMMY_TOPIC)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode('utf-8')

    if topic == DHT_TOPIC:
        try:
            temperature = float(payload)
            temperature_data.append(temperature)
            print('Received temperature:', temperature)
        except ValueError:
            print('Invalid temperature value received:', payload)

    elif topic == POT_TOPIC:
        try:
            potentio = int(payload)
            potentio_data.append(potentio)
            print('Received Potentio:', potentio)
        except ValueError:
            print('Invalid potentio value received:', payload)

    elif topic == DUMMY_TOPIC:
        try:
            dummy = int(payload)
            dummy_data.append(dummy)
            print('Received Dummy:', dummy)
        except ValueError:
            print('Invalid dummy value received:', payload)

def on_disconnect(client, userdata, rc):
    print('Disconnected from MQTT broker')

# Create MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

# Connect to MQTT broker
client.connect(MQTT_SERVER, MQTT_PORT, 60)

# Start the MQTT network loop
client.loop_start()

# Plot and update the graphs
fig, (ax1, ax2, ax3) = plt.subplots(3, 1)
line1, = ax1.plot([], [], 'r', label='Temperature')
line2, = ax2.plot([], [], 'b', label='Kecepatan')
line3, = ax3.plot([], [], 'g', label='Jumlah Penumpang')
ax1.set_ylabel('Temperature (Celsius)')
ax2.set_ylabel('Kecepatan (Km/h)')
ax3.set_ylabel('Jumlah Penumpang')
ax3.set_xlabel('Time')
ax1.legend()
ax2.legend()
ax3.legend()

def update_graph(frame):
    line1.set_data(range(len(temperature_data)), temperature_data)
    line2.set_data(range(len(potentio_data)), potentio_data)
    line3.set_data(range(len(dummy_data)), dummy_data)
    ax1.relim()
    ax1.autoscale_view(True, True, True)
    ax2.relim()
    ax2.autoscale_view(True, True, True)
    ax3.relim()
    ax3.autoscale_view(True, True, True)
    return line1, line2, line3

ani = animation.FuncAnimation(fig, update_graph, interval=1000)

plt.show()