import time
from ovos_bus_client import MessageBusClient, Message

def on_connect():
    print("[Connected] Successfully connected to OVOS message bus.")

def handle_utterance(message: Message):
    """Fired whenever the listener recognizes speech or text input."""
    utterances = message.data.get("utterances", [])
    print(f"\n[SPEECH/TEXT RECOGNIZED] Utterances: {utterances}")
    print(f"  Context: {message.context}")

def handle_skill_start(message: Message):
    """Fired when an intent successfully triggers a skill handler."""
    intent_data = message.data.get("intent", {})
    skill_id = message.data.get("skill_id", "Unknown")
    print(f"\n[INTENT MATCHED!] Skill ID: {skill_id}")
    print(f"  Intent Data: {intent_data}")

def handle_fallback(message: Message):
    """Fired if no skill handles the utterance."""
    print(f"\n[FALLBACK TRIGGERED] Unhandled message: {message.msg_type}")

def main():
    # Initialize the bus client (defaults to localhost:8181)
    client = MessageBusClient()
    
    # Register event callbacks
    client.on("open", on_connect)
    client.on("recognizer_loop:utterance", handle_utterance)
    client.on("mycroft.skill.handler.start", handle_skill_start)
    
    # Connect and run in a background thread
    print("Starting OVOS Message Bus Monitor...")
    client.run_in_thread()
    
    try:
        # Keep the script running to listen for live events
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping bus monitor...")
        client.close()

if __name__ == "__main__":
    main()