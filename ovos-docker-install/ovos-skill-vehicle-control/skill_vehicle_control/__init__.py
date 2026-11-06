import requests
from ovos_workshop.skills import OVOSSkill
from ovos_workshop.decorators import intent_handler
from ovos_bus_client.message import Message
from ovos_utils.log import LOG
from ovos_utils import classproperty
from ovos_utils.process_utils import RuntimeRequirements

DEFAULT_SETTINGS = {
    "log_level": "INFO"
}

class VehicleControlSkill(OVOSSkill):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = "http://192.168.4.8:5000/"

    @classproperty
    def runtime_requirements(self):
        # if this isn't defined the skill will
        # only load if there is internet
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
        LOG.info("VehicleControlSkill initialized and ready")

    def on_settings_changed(self):
        """This method is called when the skill settings are changed."""
        LOG.info("Settings changed!")

    @property
    def log_level(self):
        """Dynamically get the 'log_level' value from the skill settings file.
        If it doesn't exist, return the default value.
        This will reflect live changes to settings.json files (local or from backend)
        """
        return self.settings.get("log_level", "INFO")


    @intent_handler('vehicle.intent')
    def handle_vehicle_intent(self, message):
        utterance = message.data.get('utterance', '').lower()
        action = "start" if "start" in utterance else "stop"
        self.speak_dialog("vehicle.command.dialog", wait=True)
        LOG.info(f"Vehicle command: {utterance} / {action}")
        self.play_beep(message)

        try:
            # LOG.info(f"Vehicle {action}: {url}")
            response = self.post_cmd(action)
            if response.status_code == 200:
                self.speak_dialog(f"vehicle.{action}ed.dialog")
            else:
                LOG.error(f"HTTP Error: {response.status_code} for action {action}")
                self.speak("The vehicle controller returned an error.")
        except Exception as e:
            LOG.error(f"HTTP Error: {e}")
            self.speak("I am unable to reach the vehicle controller.")

    @intent_handler('vehicle_state.intent')
    def handle_vehicle_state_intent(self, message):
        LOG.info("Enter Checking vehicle state...")
        self.play_beep(message)

        try:
            # Assuming your API returns JSON like {"state": "running"}
            url = f"{self.base_url}state"
            LOG.info(f"Execute state request to {url}")
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                current_status = data.get("state", "unknown")
                # Pass the variable 'state' to the .dialog file
                self.speak_dialog("vehicle_state.dialog", data={"state": current_status})
            else:
                LOG.info(f"Error execute state request with error: {response.status_code}")
                self.speak("I couldn't get a valid state from the vehicle")
        except Exception as e:
            LOG.error(f"State check failed: {e}")
            self.speak("The vehicle system is not responding to status requests.")

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
                {"uri": sound_path}
            )
        )

    def post_cmd(self, action):
        url = self.base_url + action
        LOG.info(f"Post {action}: {url}")
        return requests.post(url)

    ##   $.post('/control', {'command':'set_' + name, 'speed': speed, 'distance': distance });}
    def post_command_json(self, action):
        ## self.base_url
        url = self.base_url + "/control"
        LOG.info(f"Vehicle {action}: {url}")
        # payload = {f"command": set_{action}, speed: 0, distance: 0"}
        payload ={"command": "set_stop", "speed": "80", "distance": "1200"}
        LOG.info(f"Send control request http post-> {url}")
        response = requests.post(self.SERVER_MOVE_URL, data=payload, timeout=4)

def create_skill():
    return VehicleControlSkill()