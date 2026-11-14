import time
from ovos_bus_client import MessageBusClient, Message

def inject_text(text: str, lang: str = "en-us"):
    # Initialize the message bus client (defaults to localhost:8181)
    client = MessageBusClient()
    
    print("Connecting to OVOS message bus...")
    client.run_in_thread()
    client.connected_event.wait(timeout=5)
    
    if not client.connected_event.is_set():
        print("Error: Could not connect to the OVOS message bus.")
        return

    # Construct the message payload expected by the intent service
    # The 'recognizer_loop:utterance' event expects a list of utterances
    msg = Message(
        "recognizer_loop:utterance",
        data={
            "utterances": [text],
            "lang": lang
        },
        context={
            "source": "python_script_injection",
            "session": {"session_id": "default"}
        }
    )

    print(f"Injecting utterance: '{text}'")
    client.emit(msg)
    
    # Give the bus a moment to transmit before closing
    time.sleep(1)
    client.close()
    print("Injection complete.")

if __name__ == "__main__":
    # Test your vehicle intent directly
    inject_text("check k9 state")