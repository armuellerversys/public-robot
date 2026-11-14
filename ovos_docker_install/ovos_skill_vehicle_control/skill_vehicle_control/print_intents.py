from ovos_bus_client import MessageBusClient, Message

# Initialize client connecting to local OVOS message bus
client = MessageBusClient()
client.run_in_thread()
client.connected_event.wait()

# Listen for Adapt intents manifest reply
def handle_adapt_manifest(message):
    print("--- REGISTERED ADAPT INTENTS ---")
    for intent in message.data.get("intents", []):
        print(intent)

client.on("intent.service.adapt.manifest", handle_adapt_manifest)

# Request the manifest
print("Requesting Adapt intents manifest...")
client.emit(Message("intent.service.adapt.manifest.get"))

# Keep alive briefly to catch response
import time
time.sleep(2)
client.close()