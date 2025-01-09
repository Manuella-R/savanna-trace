# Savanna Trace - MQTT IP Address Tracker

Savanna Trace is an application that facilitates the remote tracking of a LoRa gateway's IP address using the MQTT protocol. The gateway is connected to a Raspberry Pi and utilizes the MQTT protocol to publish its dynamically assigned IP address to a subscribed topic. This ensures the user can always retrieve the latest IP address even when network configurations change.

## Project Overview

### Problem:
We remotely access our LoRa gateway deployed on campus via a static IP. However, due to network upgrades, the gateway loses its static IP, making it inaccessible. The goal of this project is to build an application that uses MQTT to request and update the IP address of the gateway, ensuring the user can always access it.

### Solution:
- **MQTT Protocol**: Used for communication between the backend (Python) and frontend (Vue.js).
- **Frontend**: Vue.js application to display the IP address and allow real-time updates.
- **Backend**: Python application to retrieve the IP address from the Raspberry Pi and publish it to the MQTT broker.

## Features

- **Connects to MQTT Broker**: Establishes a connection to the MQTT broker (broker.emqx.io) and subscribes to a topic to receive the latest IP address.
- **Retrieves IP Address**: The Raspberry Pi retrieves its dynamic IP address from the network.
- **Publishes IP Address**: The IP address is published to an MQTT topic (`gateway/ip`).
- **Real-Time Updates**: Displays the latest IP address in real time as it is published.
- **Resilient**: The application automatically retries to connect to the MQTT broker in case of failure.

## Technologies Used

- **Frontend**: Vue.js (with TypeScript) for real-time user interface
- **Backend**: Python (using `paho-mqtt` library for MQTT communication)
- **MQTT Broker**: EMQX (broker.emqx.io), a public MQTT broker
- **Version Control**: Git, GitHub for source code management

## Requirements

- Node.js (for the frontend)
- Python 3.x (for the backend)
- MQTT Broker (broker.emqx.io or any MQTT broker)
- Vue.js (for frontend development)

## Installation Guide

### 1. Setting Up the Backend (Python)

#### 1.1. Clone the repository
Clone the repository to your local machine to start working on the project:

```bash
git clone https://github.com/Manuella-R/savanna-trace.git
cd savanna-trace
```

#### 1.2. Install the required Python dependencies
The backend relies on the `paho-mqtt` library to interact with the MQTT broker. Install it via `pip`:

```bash
pip install paho-mqtt
```

#### 1.3. Configure the Python application
The Python script `app.py` is responsible for:
- Retrieving the Raspberry Pi's IP address.
- Connecting to the MQTT broker.
- Publishing the IP address to a subscribed topic.

Run the `app.py` script:

```bash
python app.py
```

Ensure the Python script is connected to the MQTT broker (`broker.emqx.io`), retrieves the IP address, and publishes it to the topic `gateway/ip`.

### 2. Setting Up the Frontend (Vue.js)

#### 2.1. Install Node.js and Vue.js

Install Node.js (if not already installed) from [here](https://nodejs.org/). Afterward, install Vue CLI globally:

```bash
npm install -g @vue/cli
```

#### 2.2. Clone the repository
Clone the repository as described above.

#### 2.3. Install the frontend dependencies
Navigate to the frontend directory and install the necessary dependencies using `npm`:

```bash
cd frontend
npm install
```

#### 2.4. Modify the MQTT configuration
In the `app.vue` file, update the MQTT broker URL (assuming you're using `broker.emqx.io`):

```js
const brokerUrl = 'ws://broker.emqx.io:8083/mqtt'; // WebSocket URL for the broker
```

This is crucial because the broker will communicate with the frontend through WebSockets (not TCP/IP). The port `8083` is the default WebSocket port for EMQX brokers.

#### 2.5. Run the frontend application
After installing dependencies and configuring MQTT settings, run the Vue.js frontend:

```bash
npm run serve
```

This will start the Vue.js app on a local development server (typically at `http://localhost:8080`).

### 3. Testing the Application

#### 3.1. Start the backend
Make sure the Python `app.py` is running on the Raspberry Pi (or your local machine) and is correctly publishing the IP address to the MQTT broker.

#### 3.2. Start the frontend
The frontend should display the latest IP address in real-time. If the backend publishes a new IP, it will be automatically reflected in the Vue.js interface.


## Screenshots

### Frontend
![Screenshot 2025-01-09 230849](https://github.com/user-attachments/assets/1ba4377b-e293-4adc-920f-c1d65efa8068)

![Screenshot 2025-01-09 231208](https://github.com/user-attachments/assets/7bd88254-1b63-4c1a-91ac-6242e89a48ff)


### Backend
![Screenshot 2025-01-09 194711](https://github.com/user-attachments/assets/e635c9c3-1ab3-4adf-b81b-415854b3d986)

## Video Demo

https://github.com/user-attachments/assets/b1aea6a3-08c5-43cd-9f6a-dac82a737a5a


https://github.com/user-attachments/assets/37f7c0ab-a4ba-42ba-b126-1889a2bee3f6

## Acknowledgments

- Special thanks to the creators of the MQTT protocol and the libraries used in this project.
- Thanks to the Vue.js and Python communities for the frameworks and tools used in the development of this project.
