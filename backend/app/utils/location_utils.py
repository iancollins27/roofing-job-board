from typing import Optional, Tuple
from math import radians, sin, cos, sqrt, atan2
import logging
import pgeocode

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the geocoder once (it loads a small database into memory)
nomi = pgeocode.Nominatim('us')

def get_coordinates_from_zip(zip_code: str) -> Optional[Tuple[float, float]]:
    """Get latitude and longitude from a ZIP code using local database."""
    try:
        logger.info(f"Looking up ZIP: {zip_code}")
        location = nomi.query_postal_code(zip_code)
        
        if location is not None and not (location.latitude != location.latitude):  # Check for NaN
            lat, lon = location.latitude, location.longitude
            logger.info(f"Found coordinates for ZIP {zip_code}: ({lat}, {lon})")
            return (float(lat), float(lon))
        
        logger.error(f"No location found for ZIP code: {zip_code}")
        return None
        
    except Exception as e:
        logger.error(f"Error looking up ZIP {zip_code}: {str(e)}")
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