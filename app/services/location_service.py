# app/services/location_service.py
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(level=logging.INFO)

class LocationService:
    def __init__(self):
        self.api_key = os.getenv("ABSTRACT_API_KEY")
        if not self.api_key:
            logging.warning("ABSTRACT_API_KEY not set. IP-based location lookup disabled.")
        self.base_url = "https://ipgeolocation.abstractapi.com/v1"

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def get_ip_location(self, ip_address):
        if not ip_address or not self.api_key:
            logging.warning(f"IP location lookup skipped: IP={ip_address}, API_KEY={'set' if self.api_key else 'not set'}")
            return None
        params = {
            "api_key": self.api_key,
            "ip_address": ip_address
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            logging.info(f"Location lookup for IP {ip_address}: {data}")
            return {
                'country': data.get('country'),
                'city': data.get('city'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'is_in_gaza': str(data.get('city', '')).strip().lower() == 'gaza'
            }
        except requests.RequestException as e:
            logging.error(f"Error fetching location for IP {ip_address}: {e}")
            return None

    @staticmethod
    def get_manual_location(city):
        if not city:
            logging.warning("No city provided for manual location lookup.")
            return None
        result = {
            'city': city,
            'country': 'Palestine',
            'latitude': None,
            'longitude': None,
            'is_in_gaza': city.strip().lower() == 'gaza'
        }
        logging.info(f"Manual location lookup for city '{city}': {result}")
        return result