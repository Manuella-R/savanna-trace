import socket
import time
import logging
import paho.mqtt.client as mqtt

# Configuration
BROKER = "broker.emqx.io"  # You can change this to your own broker if needed
PORT = 1883
TOPIC = "gateway/ip"
RETRY_INTERVAL = 5
PUBLISH_INTERVAL = 10  # Time interval between each IP address publish in seconds

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def get_ip():
    """Retrieve the device's IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Connected to MQTT broker")
    else:
        logging.error(f"Connection failed with code {rc}")

def on_publish(client, userdata, result):
    logging.info("IP address published successfully")

def main():
    """Main function to connect to MQTT broker and publish IP."""
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish

    # Connect to MQTT broker and handle retries
    while True:
        try:
            client.connect(BROKER, PORT)
            break
        except Exception as e:
            logging.error(f"Connection failed: {e}. Retrying in {RETRY_INTERVAL} seconds...")
            time.sleep(RETRY_INTERVAL)

    # Start the MQTT loop in a separate thread
    client.loop_start()

    try:
        while True:
            ip_address = get_ip()
            logging.info(f"Publishing IP address: {ip_address}")
            client.publish(TOPIC, ip_address)
            time.sleep(PUBLISH_INTERVAL)  # Wait before publishing again

    except KeyboardInterrupt:
        logging.info("Shutting down gracefully...")

    finally:
        client.loop_stop()
        client.disconnect()

if __name__ == "__main__":
    main()
