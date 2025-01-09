<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import mqtt, { MqttClient } from 'mqtt'; // Ensure MqttClient is imported
import HelloWorld from './components/HelloWorld.vue';

// Define MQTT configuration
const mqttOptions = {
  clientId: `Vue_Client_${Math.random().toString(16).slice(3)}`, // Unique ID for the client
  clean: true,
  reconnectPeriod: 1000,
};

// MQTT Broker URL (Update with the broker's URL from your Python backend)
const brokerUrl = 'ws://broker.emqx.io:8083/mqtt'; // Use WebSocket URL for browser connections
const topic = 'gateway/ip'; // Topic to subscribe to

// Reactive variables
const messageList = ref<string[]>([]); // Array to store all received messages

// Create MQTT client instance
let client: MqttClient | null = null;

// Connect to MQTT broker and subscribe
onMounted(() => {
  client = mqtt.connect(brokerUrl, mqttOptions);

  client.on('connect', () => {
    console.log('Connected to MQTT broker');
    client?.subscribe(topic, (err) => {
      if (!err) {
        console.log(`Subscribed to topic: ${topic}`);
      } else {
        console.error('Failed to subscribe:', err);
      }
    });
  });

  client.on('message', (topic, message) => {
    console.log(`Received message on ${topic}: ${message.toString()}`);
    messageList.value.push(message.toString()); // Append the new message to the list
  });

  client.on('error', (err) => {
    console.error('MQTT Error:', err);
  });
});

// Cleanup when the component is unmounted
onBeforeUnmount(() => {
  client?.end(); // Close the connection
});
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" />

    <div class="wrapper">
      <HelloWorld msg="Welcome to Savanna Trace!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <main>
    <h2>Received MQTT Messages</h2>
    <div v-if="messageList.length">
      <p v-for="(msg, index) in messageList" :key="index">
        <strong>Message {{ index + 1 }}:</strong> {{ msg }}
      </p>
    </div>
    <p v-else>No messages received yet...</p>
  </main>

  <RouterView />
</template>

<style scoped>
/* Styles remain the same as the original */
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
