import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.services.theirstack_api import sync_jobs

if __name__ == "__main__":
    try:
        # Modify the fetch_roofing_jobs function to get more jobs
        synced_count = sync_jobs()
        print(f"\nSuccessfully synced {synced_count} jobs")
    except Exception as e:
        print(f"Error syncing jobs: {str(e)}")
        sys.exit(1) 