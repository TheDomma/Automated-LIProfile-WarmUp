import logging
import random
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from jobs.worker import run_profile_warmup
from db.queries import get_active_profiles

logger = logging.getLogger(__name__)

def schedule_daily_jobs(scheduler: AsyncIOScheduler):
    """
    Pulls active profiles and schedules them at random times throughout the day.
    """
    logger.info("Running daily dispatcher to schedule profile jobs...")
    
    profiles = get_active_profiles()
    
    if not profiles:
        logger.warning("No active profiles found in DB.")
        # For testing, you might want to return a dummy list here:
        # profiles = ["test_profile_id_123"]
        return
        
    now = datetime.now()
    
    for profile_id in profiles:
        # Schedule between now + 5 mins and now + 8 hours
        # minutes_offset = random.randint(5, 480)
        # Schedule immediately for testing
        minutes_offset = 0
        run_time = now + timedelta(minutes=minutes_offset)
        
        scheduler.add_job(
            run_profile_warmup,
            'date',
            run_date=run_time,
            args=[profile_id]
        )
        logger.info(f"Scheduled profile {profile_id} to run at {run_time.strftime('%H:%M:%S')}")
