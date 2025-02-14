from typing import Optional, Tuple
from math import radians, sin, cos, sqrt, atan2
import logging
import requests
from ..core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_coordinates_from_zip(zip_code: str) -> Optional[Tuple[float, float]]:
    """Get latitude and longitude from a ZIP code using Google Geocoding API."""
    try:
        logger.info(f"Looking up ZIP: {zip_code}")
        
        # Build the Google Geocoding API URL
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": zip_code,
            "components": "country:US|postal_code:" + zip_code,
            "key": settings.GOOGLE_MAPS_API_KEY
        }
        
        # Make the API request
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data["status"] == "OK" and data["results"]:
            location = data["results"][0]["geometry"]["location"]
            lat, lon = location["lat"], location["lng"]
            logger.info(f"Found coordinates for ZIP {zip_code}: ({lat}, {lon})")
            return (float(lat), float(lon))
        
        logger.error(f"No location found for ZIP code: {zip_code}")
        return None
        
    except Exception as e:
        logger.error(f"Error looking up ZIP {zip_code}: {str(e)}")
        return None

def get_coordinates_from_address(address: str) -> Optional[Tuple[float, float]]:
    """Get latitude and longitude from an address string using Google Geocoding API."""
    try:
        logger.info(f"Looking up address: {address}")
        
        # Verify API key is not empty
        if not settings.GOOGLE_MAPS_API_KEY:
            logger.error("Google Maps API key is not set")
            return None
        
        # Build the Google Geocoding API URL
        base_url = "https://maps.googleapis.com/maps/api/geocode/json"
        params = {
            "address": address,
            "components": "country:US",
            "key": settings.GOOGLE_MAPS_API_KEY
        }
        
        # Debug info
        logger.info(f"Using Google Maps API Key: {settings.GOOGLE_MAPS_API_KEY[:10]}...")
        
        # Make the API request
        response = requests.get(base_url, params=params)
        
        # Log the full URL for debugging (with key partially redacted)
        debug_url = response.url.replace(settings.GOOGLE_MAPS_API_KEY, settings.GOOGLE_MAPS_API_KEY[:10] + "...")
        logger.info(f"Request URL: {debug_url}")
        
        response.raise_for_status()
        data = response.json()
        
        # Debug response
        logger.info(f"Google API Response Status: {data.get('status')}")
        if data.get('error_message'):
            logger.error(f"Google API Error: {data.get('error_message')}")
        logger.info(f"Full Response: {data}")
        
        if data["status"] == "OK" and data["results"]:
            location = data["results"][0]["geometry"]["location"]
            lat, lon = location["lat"], location["lng"]
            logger.info(f"Found coordinates for address {address}: ({lat}, {lon})")
            return (float(lat), float(lon))
        
        logger.error(f"No location found for address: {address}")
        return None
        
    except Exception as e:
        logger.error(f"Error looking up address {address}: {str(e)}")
        return None

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two points in miles using Haversine formula"""
    R = 3959.87433  # Earth's radius in miles

    lat1, lon1 = radians(lat1), radians(lon1)
    lat2, lon2 = radians(lat2), radians(lon2)
    
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    distance = R * c
    return distance

def is_within_radius(job_zip: str, search_zip: str, radius_miles: float = 150.0) -> bool:
    """Check if a job's location is within the specified radius of the search location."""
    distance = calculate_distance(job_zip, search_zip)
    if distance is None:
        return False
    return distance <= radius_miles 