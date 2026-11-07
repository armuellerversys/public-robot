from flask import Flask, Response, request
from ovos_bus_client.client import MessageBusClient
from ovos_bus_client.message import Message
import time
import logging

app = Flask(__name__)

class SoundServer():

    def __init__(self):
        self.client = MessageBusClient()
        self.client.run_in_thread()
        time.sleep(1)
        self.client.connected_event.wait()

    def play_sound(self, sound="boing_x.wav"):
        logger.info("Enter play_sound...")
        if not self.client:
            logger.warning("Client not ready, skipping sound")
            return

        sound_path = f"/home/ovos/.local/share/mycroft/sounds/{sound}"
        logger.info(f"Sound path: {sound_path}")
        self.client.emit(
            Message(
                "mycroft.audio.play_sound",
                {"uri": sound_path}
            )
        )

    @staticmethod
    def getLogger(name):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        # CHECK if logger already has handlers before adding a new one
        if not logger.handlers: 
            # create console handler with a higher log level
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            
            # create formatter and add it to the handlers
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
            ch.setFormatter(formatter)
            
            # add the handler to the logger
            logger.addHandler(ch)
            
        return logger

    @app.route("/play", methods=["GET", "POST"])
    def play():
        if request.method == "POST":
            data = request.get_json() or {}
            sound = data.get("sound", "boing_x.wav").strip()
        else:
            sound = request.args.get("sound", "boing_x.wav").strip()

        try:
            sound_server.play_sound(sound)
            return Response("Sound playback ok", status=200)
        except Exception as e:
            logger.error(f"Error occurred while playing sound: {e}")
            return Response("Sound playback failed", status=500)

sound_server = SoundServer()
logger = SoundServer.getLogger("SoundServer")

if __name__ == "__main__":
    logger.info("Starting Kokoro TTS Voice Server with Audio Queue on port 5800...")
    app.run(host="0.0.0.0", port=5800, use_reloader=False)