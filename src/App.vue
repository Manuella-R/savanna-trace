<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from "vue";
import mqtt, { MqttClient } from "mqtt";

// MQTT Configuration
const mqttOptions = {
  clientId: `Vue_Client_${Math.random().toString(16).slice(3)}`,
  clean: true,
  reconnectPeriod: 1000,
};
const brokerUrl = "ws://broker.emqx.io:8083/mqtt"; // WebSocket URL
const topic = "gateway/ip"; // MQTT topic to subscribe to

// Reactive Variables
const connectionStatus = ref("Disconnected");
const loading = ref(false);
const receivedIp = ref<string | null>(null); // Latest IP
const ipList = ref<string[]>([]); // List of all received IPs

let client: MqttClient | null = null;

// Connect to the MQTT broker and set up event listeners
onMounted(() => {
  client = mqtt.connect(brokerUrl, mqttOptions);

  client.on("connect", () => {
    connectionStatus.value = "Connected";
    console.log("Connected to MQTT broker");
    client?.subscribe(topic, (err) => {
      if (!err) {
        console.log(`Subscribed to topic: ${topic}`);
      } else {
        console.error("Failed to subscribe:", err);
      }
    });
  });

  client.on("message", (topic, message) => {
    console.log(`Received message on ${topic}: ${message.toString()}`);
    const ip = message.toString();
    receivedIp.value = ip;

    // Add the IP to the list, avoiding duplicates
    if (!ipList.value.includes(ip)) {
      ipList.value.unshift(ip); // Add to the top of the list
    }

    loading.value = false; // Stop loading after receiving the message
  });

  client.on("error", (err) => {
    console.error("MQTT Error:", err);
    connectionStatus.value = "Error";
  });
});

onBeforeUnmount(() => {
  client?.end(); // Disconnect from the MQTT broker
});

// Manually fetch the latest IP address
const fetchIpAddress = () => {
  if (connectionStatus.value === "Connected") {
    loading.value = true; // Show loading while waiting for a message
    console.log("Fetching latest IP address...");
  } else {
    alert("MQTT broker is not connected. Please try again.");
  }
};
</script>

<template>
  <div class="app">
    <!-- Header -->
    <header>
      <img alt="Vue logo" class="logo" src="@/assets/logo.svg" />
      <h1>Gateway IP Viewer</h1>
      <p>View the latest and past IP addresses received via MQTT.</p>
    </header>

    <!-- Connection Status -->
    <div class="status">
      <strong>Connection Status:</strong>
      <span :class="connectionStatus.toLowerCase()">{{ connectionStatus }}</span>
    </div>

    <!-- Main Interface -->
    <main>
      <!-- List of IPs -->
      <div class="ip-list">
        <h2>IP Address History</h2>
        <ul>
          <li v-for="(ip, index) in ipList" :key="index">
            <strong>{{ index + 1 }}.</strong> {{ ip }}
          </li>
        </ul>
        <p v-if="!ipList.length">No IP addresses received yet.</p>
      </div>

      <!-- Latest IP Address -->
      <div class="latest-ip">
        <h2>Latest IP Address</h2>
        <p v-if="receivedIp" class="latest-ip-value">{{ receivedIp }}</p>
        <p v-else>No IP address received yet.</p>
      </div>

      <!-- Fetch IP Button -->
      <button @click="fetchIpAddress" :disabled="loading">
        {{ loading ? "Fetching..." : "Get Latest IP" }}
      </button>
    </main>
  </div>
</template>

<style scoped>
/* General Styles */
.app {
  font-family: Arial, sans-serif;
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

header {
  margin-bottom: 20px;
}

.logo {
  width: 100px;
  margin-bottom: 10px;
}

button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  cursor: pointer;
  border-radius: 5px;
  transition: background-color 0.3s;
}

button:disabled {
  background-color: #d3d3d3;
  cursor: not-allowed;
}

button:hover:not(:disabled) {
  background-color: #368c71;
}

/* Connection Status */
.status {
  margin: 20px 0;
  font-size: 1.2rem;
}

.status .connected {
  color: #42b983;
}

.status .disconnected {
  color: red;
}

.status .error {
  color: orange;
}

/* IP List */
.ip-list {
  margin: 20px 0;
}

.ip-list ul {
  list-style: none;
  padding: 0;
}

.ip-list li {
  background-color: #2e0202;
  margin: 5px 0;
  padding: 10px;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.latest-ip-value {
  font-weight: bold;
  font-size: 1.5rem;
  color: #42b983;
}
</style>
