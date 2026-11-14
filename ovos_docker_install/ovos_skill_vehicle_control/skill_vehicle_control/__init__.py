import os
import requests
import logging
from ovos_workshop.skills import OVOSSkill
from ovos_workshop.decorators import intent_handler
# Use relative import if core_utils is local to your skill package, 
# or ensure core_utils is installed in your python environment.
from .core_utils import CoreUtils  # Change to 'from core_utils import CoreUtils' if it's a global package
from ovos_bus_client.message import Message
from ovos_utils.log import LOG
from ovos_utils import classproperty
from ovos_utils.process_utils import RuntimeRequirements

DEFAULT_SETTINGS = {
    "log_level": "INFO"
}

URL_BASE = os.getenv('EXTERNAL_SERVICE_URL', 'http://192.168.4.8:5001')
URL_SPEAK = os.getenv('VOICE_SERVICE_URL', 'http://192.168.4.6:5500/speak_local')
URL_TEXT = os.getenv('TEXT_SERVICE_URL', 'http://192.168.4.1:5000/displayText')

logger = logging.getLogger("VehicleControlSkill")
logger.setLevel(logging.INFO)

class VehicleControlSkill(OVOSSkill):
    def __init__(self, *args, **kwargs):
        logger.info("VehicleControlSkill initializing...")
        super().__init__(*args, **kwargs)

    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(
            internet_before_load=False,
            network_before_load=False,
            gui_before_load=False,
            requires_internet=False,
            requires_network=False,
            requires_gui=False,
            no_internet_fallback=True,
            no_network_fallback=True,
            no_gui_fallback=True,
        )

    def initialize(self):
        logger.info("VehicleControlSkill initialized and ready")

    def on_settings_changed(self):
        logger.info("VehicleControlSkill, Settings changed!")

    @property
    def log_level(self):
        return self.settings.get("log_level", "INFO")

    @intent_handler('vehicle.intent')
    def handle_vehicle_intent(self, message: Message):
        utterance = message.data.get('utterance', '').lower()
        CoreUtils.say_text(f"Vehicle: {utterance}")
        action = "start" if "start" in utterance else "stop"
        self.speak_dialog("vehicle.command.dialog", wait=True)
        LOG.info(f"Vehicle command: {utterance} / {action}")
        self.play_beep(message)

        try:
            LOG.info(f"Vehicle {action}: {utterance}")
            response = self.post_cmd(action)
            if response.status_code == 200:
                self.speak_dialog(f"vehicle.{action}ed.dialog")
            else:
                LOG.error(f"HTTP Error: {response.status_code} for action {action}")
                self.speak("The vehicle controller returned an error.")
        except Exception as e:
            LOG.error(f"HTTP Error: {e}")
            self.speak("I am unable to reach the vehicle controller.", wait=True)

    @intent_handler('vehicle_state.intent')
    def handle_vehicle_state_intent(self, message: Message):
        LOG.info("Enter Checking vehicle state...")
        self.play_beep(message)

        try:
            url = f"{URL_BASE}/state"
            LOG.info(f"Execute state request to {url}")
            CoreUtils.say_text("Intent status check")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                current_status = data.get("state", "unknown")
                self.speak_dialog("vehicle_state.dialog", data={"state": current_status})
            else:
                LOG.info(f"Error execute state request with error: {response.status_code}")
                self.speak("I couldn't get a valid state from the vehicle", wait=True)
        except Exception as e:
            LOG.error(f"State check failed: {e}")
            self.speak("The vehicle system is not responding to status requests.", wait=True)

    def play_beep(self, message):
        LOG.info("Enter play_beep...")
        if not self.bus:
            LOG.warning("Bus not ready, skipping beep")
            return

        sound_path = "/home/ovos/.config/mycroft/boing_x.wav"
        LOG.info(f"Sound path: {sound_path}")
        
        self.bus.emit(
            Message(
                "mycroft.audio.play_sound",
                {"uri": sound_path}, context=message.context
            )
        )

    def post_cmd(self, action):
        url = URL_BASE + f"/{action}"
        LOG.info(f"Post {action}: {url}")
        return requests.post(url)

    def post_command_json(self, action):
        url = URL_BASE + "/control"
        LOG.info(f"Vehicle {action}: {url}")
        payload = {"command": "set_stop", "speed": "80", "distance": "1200"}
        LOG.info(f"Send control request http post-> {url}")
        try:
            response = requests.post(url, json=payload, timeout=4)
            if response.status_code == 200:
                LOG.info(f"Vehicle control command sent successfully: {response.status_code}")
            else:
                # Fixed multiline string syntax error here
                LOG.error(f"Vehicle control command failed with status code: {response.status_code} - {response.text}")
        except Exception as e:
            LOG.error(f"Failed to send vehicle control command: {e}")

def create_skill():
    return VehicleControlSkill()