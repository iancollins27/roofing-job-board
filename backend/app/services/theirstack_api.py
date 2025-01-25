import requests
import bleach
import markdown
import time
from datetime import datetime
from typing import List, Dict, Any
from ..models.job_model import Job
from ..core.database import get_db_session
from ..core.config import settings
from ..utils.location_utils import get_coordinates_from_zip as get_coordinates
from ..utils.html_utils import sanitize_html
from ..utils.job_classifier import classify_job_function

# Use settings directly - remove load_dotenv() call
THEIRSTACK_API_URL = settings.THEIRSTACK_API_URL
THEIRSTACK_API_KEY = settings.THEIRSTACK_API_KEY

def fetch_roofing_jobs(page: int = 0, limit: int = 2) -> List[Dict[Any, Any]]:
    """Fetch jobs from TheirStack API"""
    print(f"\nAPI Key present: {bool(THEIRSTACK_API_KEY)}")
    print(f"API Key value: {THEIRSTACK_API_KEY[:5]}..." if THEIRSTACK_API_KEY else "No API Key")
    
    if not THEIRSTACK_API_KEY:
        print("TheirStack API key not found, skipping job fetch")
        return []
    
    print(f"\nFetching jobs from TheirStack (page {page}, limit {limit})")
    
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {THEIRSTACK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "page": page,
        "limit": limit,
        "posted_at_max_age_days": 30,
        "job_title_pattern_or": ["roofing", "roofer"],
        "job_country_code_or": ["US"],
        "include_total_results": False,
        "blur_company_data": False
    }
    
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            print(f"\nMaking API request to {THEIRSTACK_API_URL}")
            print(f"Headers: {headers}")
            print(f"Data: {data}")
            
            response = requests.post(
                THEIRSTACK_API_URL,
                headers=headers,
                json=data,
                timeout=30
            )
            
            print(f"\nResponse status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Raw API response: {data}")
                jobs = data.get('data', [])
                print(f"Received {len(jobs)} jobs")
                return jobs
            else:
                print(f"Error response: {response.text}")
                
        except requests.exceptions.Timeout:
            print("\nRequest timed out")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached")
                return []
                
        except requests.exceptions.RequestException as e:
            print(f"\nRequest failed: {str(e)}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                print("Max retries reached")
                return []
    
    return []

def map_job_data(job_data: Dict[str, Any]) -> Dict[str, Any]:
    """Map TheirStack job data to our schema"""
    try:
        print(f"\nMapping job: {job_data.get('title')}")
        
        # Get location details and handle postal code
        location = job_data.get("long_location", "")
        postal_code = None
        
        # Try to extract postal code from various location fields
        location_fields = [
            job_data.get("long_location", ""),
            job_data.get("location", ""),
            job_data.get("city", "")
        ]
        
        for field in location_fields:
            if field:
                # Look for 5-digit numbers
                import re
                zip_matches = re.findall(r'\b\d{5}\b', field)
                if zip_matches:
                    postal_code = zip_matches[0]
                    break
        
        # Get coordinates for the postal code
        latitude = None
        longitude = None
        if postal_code:
            print(f"Found postal code: {postal_code}")
            coords = get_coordinates(postal_code)
            if coords:
                latitude, longitude = coords
                print(f"Got coordinates: ({latitude}, {longitude})")
            else:
                print(f"Could not get coordinates for postal code: {postal_code}")
        else:
            print("No postal code found in location data")
        
        # Get the description and clean up the markdown
        description = job_data.get("description", "")
        description = description.replace("\\-", "-")
        description = description.replace("\\&", "&")
        description = description.replace("\\.", ".")
        
        # Convert markdown to HTML
        html_description = markdown.markdown(
            description,
            extensions=['extra', 'nl2br']
        )
        
        # Sanitize the HTML
        sanitized_description = sanitize_html(html_description)
        
        mapped_data = {
            "external_id": str(job_data.get("id")),
            "job_title": job_data.get("job_title"),
            "description": sanitized_description,
            "job_category": job_data.get("employment_type", ""),
            "location": location,
            "postal_code": postal_code,
            "latitude": latitude,
            "longitude": longitude,
            "employment_type": job_data.get("employment_type"),
            "remote_type": job_data.get("remote_type"),
            "company_url": job_data.get("company_url"),
            "source_url": job_data.get("source_url"),
            "application_link": job_data.get("apply_url") or job_data.get("source_url"),
            "application_email": job_data.get("apply_email"),
            "posted_date": datetime.fromisoformat(job_data.get("date_posted")),
            "is_active": True,
            "job_function": classify_job_function(job_data.get("job_title"))
        }
        
        print(f"Successfully mapped job data")
        return mapped_data
        
    except Exception as e:
        print(f"Error mapping job data: {str(e)}")
        raise e

def sync_jobs():
    """Fetch jobs from TheirStack and sync to our database"""
    session = next(get_db_session())
    try:
        print("\nStarting job sync...")
        jobs_data = fetch_roofing_jobs()
        print(f"\nFetched {len(jobs_data)} jobs from TheirStack")
        
        synced_count = 0
        for job_data in jobs_data:
            try:
                mapped_data = map_job_data(job_data)
                print(f"\nProcessing job: {mapped_data['job_title']}")
                
                existing_job = session.query(Job).filter_by(
                    external_id=mapped_data["external_id"]
                ).first()
                
                if not existing_job:
                    print(f"\nProcessing job: {mapped_data['job_title']}")
                    new_job = Job(**mapped_data)
                    session.add(new_job)
                    synced_count += 1
                else:
                    print(f"Job already exists: {mapped_data['job_title']}")
            except Exception as e:
                print(f"Error processing job: {str(e)}")
                continue
        
        print("\nCommitting changes to database...")
        session.commit()
        
        # Verify the jobs were saved
        final_count = session.query(Job).count()
        print(f"\nFinal job count in database: {final_count}")
        
        return synced_count
    except Exception as e:
        print(f"\nError during sync: {str(e)}")
        session.rollback()
        raise e
    finally:
        session.close() 