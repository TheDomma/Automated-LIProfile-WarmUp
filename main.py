import asyncio
import logging
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db.database import init_db
from jobs.dispatcher import schedule_daily_jobs
from reports.daily_summary import generate_report

# Suppress the noisy "I/O operation on closed pipe" error on Windows with asyncio & Playwright
if sys.platform == 'win32':
    from asyncio.proactor_events import _ProactorBasePipeTransport
    from functools import wraps
    def silence_event_loop_closed(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except ValueError as e:
                if str(e) != 'I/O operation on closed pipe':
                    raise
        return wrapper
    _ProactorBasePipeTransport.__del__ = silence_event_loop_closed(_ProactorBasePipeTransport.__del__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def main():
    logger.info("Initializing Database...")
    init_db()

    logger.info("Starting LinkedIn Health Bot Scheduler...")
    scheduler = AsyncIOScheduler()
    
    # Schedule the dispatcher to run every morning at 8:00 AM
    scheduler.add_job(schedule_daily_jobs, 'cron', hour=8, minute=0, args=[scheduler])
    
    # Schedule the report generation to run every evening at 6:00 PM
    scheduler.add_job(generate_report, 'cron', hour=18, minute=0)
    
    # For testing: run dispatcher immediately
    schedule_daily_jobs(scheduler)
    
    scheduler.start()
    
    # Keep the main thread alive
    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down...")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
