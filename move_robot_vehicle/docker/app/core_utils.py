import logging
import os
from wsgiref import headers
from mdurl import URL
import psutil
import socket
import requests
import json

URL_SPEAK = os.getenv('EXTERNAL_SERVICE_URL', 'http://192.168.4.6:5500/speak_local')

# The headers specify that you are sending JSON data
headers = {
    "Content-Type": "application/json"
}

class CoreUtils:
    def __init__(self):
        self.logger = self.getLogger()

    @staticmethod
    def getLogger(name):
        logger = logging.getLogger(name)
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

    @staticmethod
    def get_lan_ip():
        # Try to find LAN IP dynamically
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # This IP is never actually contacted; it's just to determine the local IP
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            return ip

    @staticmethod
    def get_cpu_temp():
        try:
            temps = psutil.sensors_temperatures()
            if 'cpu_thermal' in temps:
                return temps['cpu_thermal'][0].current
        except Exception:
            pass
        return 0.0

    @staticmethod
    def say_text(text, LENGTH_SCALE=1.5, VOLUME=3.0):
        logger = CoreUtils.getLogger("say_text")
        ## curl -X POST "http://<YOUR_PI_IP>:5500/speak_local" \
        ##     -H "Content-Type: application/json" \
        ##     -d '{"text": "Die Temperatur im Wohnzimmer beträgt 21 Grad.", "volume": 2.5}'
        try:
            # Create the data payload as a dictionary
            payload = {
                "text": text,
                "volume": str(VOLUME),
                "length_scale": str(LENGTH_SCALE)
            }

            # Send a POST request to the server with the JSON data
            logger.info(f"Sending request to {URL_SPEAK}...")
            response = requests.post(URL_SPEAK, data=json.dumps(payload), headers=headers, timeout=15)

            # Check if the request was successful
            if response.status_code == 200:
                logger.info("Success! The voice server received the request %s", response.status_code)
            else:
                logger.error(f"Voice Server Error! Status code: {response.status_code} - {response.text}")

        except requests.exceptions.ConnectionError as e:
            logger.error("Failed to connect to the Voice Server at %s.", URL_SPEAK)
            logger.error("Please ensure the voice Voice Server is running and accessible.")
            logger.error(f"Error details: {e}")  

    @staticmethod
    def get_cpu_percent():
        return psutil.cpu_percent()

    @staticmethod
    def get_ram_available():
        return psutil.virtual_memory().available

    @staticmethod
    def get_ram_percentage():
        return psutil.virtual_memory().percent


class RobotStopException(Exception):
    """Custom exception to break out of all control loops immediately."""
    pass  