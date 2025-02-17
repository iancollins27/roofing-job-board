# backend/app/api/job_API.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..core.database import get_db_session
from ..models.job_model import Job
from ..schemas.job_schema import JobCreate, JobResponse, PaginatedJobResponse
from ..services.theirstack_api import sync_jobs
from ..utils.location_utils import get_coordinates_from_zip as get_coordinates, calculate_distance
import markdown
import bleach

router = APIRouter()

@router.post("/", response_model=JobResponse)
def create_job(job: JobCreate, db: Session = Depends(get_db_session)):
    """Create a new job listing"""
    try:
        # Convert the job model to a dictionary
        job_data = job.dict()
        
        # Get coordinates from postal code if provided
        if job_data.get('postal_code'):
            coords = get_coordinates(job_data['postal_code'])
            if coords:
                job_data['latitude'], job_data['longitude'] = coords
                print(f"Added coordinates ({coords[0]}, {coords[1]}) for ZIP {job_data['postal_code']}")
            else:
                print(f"Could not get coordinates for ZIP {job_data['postal_code']}")
        
        # Create the job
        db_job = Job(**job_data)
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{job_id}", response_model=JobResponse)
def read_job(job_id: int, db: Session = Depends(get_db_session)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.get("/", response_model=PaginatedJobResponse)
def read_jobs(
    skip: int = Query(0, description="Number of jobs to skip"),
    limit: int = Query(25, description="Number of jobs to return"),
    db: Session = Depends(get_db_session)
):
    try:
        print("\nAttempting to fetch jobs from database...")
        
        # Get total count for pagination
        total_count = db.query(Job).count()
        print(f"Total count: {total_count}")
        
        # Simplified query - just order by id
        jobs = db.query(Job).order_by(Job.id.desc()).offset(skip).limit(limit).all()
        
        print(f"Found {len(jobs)} jobs")
        
        # Debug information about jobs
        for job in jobs:
            print(f"Job ID: {job.id}")
            print(f"Title: {job.job_title}")
            print(f"Function: {job.job_function}")
            print("---")
        
        return {
            "items": jobs,
            "total": total_count,
            "skip": skip,
            "limit": limit
        }
    except Exception as e:
        print(f"\nDetailed error in read_jobs:")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {str(e)}")
        import traceback
        print(f"Traceback:\n{traceback.format_exc()}")
        
        # Try to get more information about the jobs that might be causing issues
        try:
            all_jobs = db.query(Job).all()
            print(f"\nTotal jobs in database: {len(all_jobs)}")
            for job in all_jobs:
                print(f"Job {job.id}: {job.job_title} (function: {job.job_function})")
        except Exception as inner_e:
            print(f"Error while trying to debug: {str(inner_e)}")
        
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.post("/sync")
async def sync_theirstack_jobs():
    try:
        jobs_synced = sync_jobs()
        return {"message": f"Successfully synced {jobs_synced} jobs from TheirStack"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/cleanup-theirstack")
async def cleanup_and_resync_theirstack(db: Session = Depends(get_db_session)):
    try:
        # Only delete jobs that have an external_id (TheirStack jobs)
        print("\nDeleting existing TheirStack jobs...")
        deleted_count = db.query(Job).filter(Job.external_id.isnot(None)).delete()
        db.commit()
        print(f"Deleted {deleted_count} TheirStack jobs")
        
        # Re-sync with TheirStack
        print("\nStarting sync...")
        jobs_synced = sync_jobs()
        
        # Verify jobs were added and are still there
        theirstack_count = db.query(Job).filter(Job.external_id.isnot(None)).count()
        manual_count = db.query(Job).filter(Job.external_id.is_(None)).count()
        
        print(f"\nVerification after sync:")
        print(f"TheirStack jobs: {theirstack_count}")
        print(f"Manually posted jobs: {manual_count}")
        print(f"Total jobs: {theirstack_count + manual_count}")
        
        return {
            "message": f"Successfully cleaned up TheirStack jobs and re-synced {jobs_synced} jobs",
            "theirstack_jobs_deleted": deleted_count,
            "theirstack_jobs_synced": jobs_synced,
            "manual_jobs_preserved": manual_count
        }
    except Exception as e:
        print(f"\nError during cleanup/sync: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Keep the original cleanup endpoint for full database wipes if needed
@router.post("/cleanup")
async def cleanup_and_resync(db: Session = Depends(get_db_session)):
    try:
        print("\nDeleting ALL jobs...")
        deleted_count = db.query(Job).delete()
        db.commit()
        print(f"Deleted {deleted_count} jobs")
        
        print("\nStarting sync...")
        jobs_synced = sync_jobs()
        
        final_count = db.query(Job).count()
        print(f"\nVerification after sync:")
        print(f"Jobs synced: {jobs_synced}")
        print(f"Final job count: {final_count}")
        
        return {
            "message": f"Successfully cleaned up ALL jobs and re-synced {jobs_synced} jobs from TheirStack",
            "jobs_deleted": deleted_count,
            "jobs_synced": jobs_synced
        }
    except Exception as e:
        print(f"\nError during cleanup/sync: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search/location")
def search_jobs_by_location(
    zip_code: str = Query(..., description="ZIP code to search around"),
    radius: float = Query(25, description="Search radius in miles"),
    db: Session = Depends(get_db_session)
):
    try:
        # Get coordinates for the search ZIP code
        search_coords = get_coordinates(zip_code)
        if not search_coords:
            raise HTTPException(status_code=400, detail="Invalid ZIP code")
        
        search_lat, search_lon = search_coords
        
        # Get all jobs
        jobs = db.query(Job).all()
        
        # Filter jobs by distance
        jobs_with_distance = []
        for job in jobs:
            if job.latitude and job.longitude:
                distance = calculate_distance(
                    search_lat, search_lon,
                    job.latitude, job.longitude
                )
                if distance <= radius:
                    jobs_with_distance.append(job)
        
        return jobs_with_distance
    except Exception as e:
        print(f"Error searching jobs by location: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/debug/coordinates")
def debug_job_coordinates(db: Session = Depends(get_db_session)):
    jobs = db.query(Job).all()
    job_info = []
    for job in jobs:
        job_info.append({
            "id": job.id,
            "title": job.job_title,
            "postal_code": job.postal_code,
            "latitude": job.latitude,
            "longitude": job.longitude
        })
    return {"jobs": job_info}