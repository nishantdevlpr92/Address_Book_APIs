import math
import requests
from typing import Optional, Tuple

from app.core.config import settings


class LocationService:
    """
    Service class for handling location-related operations including geocoding and distance calculations.
    """

    @staticmethod
    def geocode_address(address_string: str) -> Optional[Tuple[float, float]]:
        """
        Convert a human-readable address to latitude and longitude using OpenStreetMap Nominatim.

        Returns a tuple (latitude, longitude) if found, otherwise None.
        """
        if not address_string or not address_string.strip():
            return None
            
        geocoding_url = settings.geocode_url
        request_params = {
            "q": address_string,
            "format": "json",
            "limit": 1,
            "addressdetails": 1
        }
        request_headers = {"User-Agent": "address-book-app"}

        try:
            api_response = requests.get(geocoding_url, params=request_params, headers=request_headers, timeout=10)
            if api_response.status_code != 200:
                return None

            response_data = api_response.json()
            if not response_data:
                return None

            return float(response_data[0]["lat"]), float(response_data[0]["lon"])
        except (requests.RequestException, KeyError, ValueError, IndexError):
            return None

    @staticmethod
    def calculate_distance(
        latitude_1: float, 
        longitude_1: float, 
        latitude_2: float, 
        longitude_2: float
    ) -> float:
        """
        Calculate the great-circle distance in kilometers between two geographic coordinates.
        """
        earth_radius_km = 6371.0

        lat1_rad = math.radians(latitude_1)
        lat2_rad = math.radians(latitude_2)
        delta_lat_rad = math.radians(latitude_2 - latitude_1)
        delta_lon_rad = math.radians(longitude_2 - longitude_1)

        central_angle = (
            math.sin(delta_lat_rad / 2) ** 2
            + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon_rad / 2) ** 2
        )
        
        distance = 2 * math.atan2(math.sqrt(central_angle), math.sqrt(1 - central_angle))

        return earth_radius_km * distance
