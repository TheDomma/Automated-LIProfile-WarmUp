import asyncio
import logging
from core.gologin import start_profile, stop_profile
from core.browser import connect_to_browser, teardown_browser
from core.health_gate import check_page_health
from core.actions import perform_random_action
from db.queries import log_session

logger = logging.getLogger(__name__)

async def run_profile_warmup(profile_id: str):
    """
    The main execution loop for a single account.
    """
    logger.info(f"Starting warmup job for profile: {profile_id}")
    browser = None
    status = "FAILED"
    reason = "UNKNOWN"
    
    try:
        # 1. Start GoLogin Profile
        ws_url = start_profile(profile_id)
        
        # Wait slightly for browser to fully open
        await asyncio.sleep(5)
        
        # 2. Attach Playwright
        browser = await connect_to_browser(ws_url)
        contexts = browser.contexts
        page = contexts[0].pages[0] if contexts and contexts[0].pages else await browser.new_page()
        
        # 3. Navigate to LinkedIn
        logger.info("Navigating to LinkedIn...")
        await page.goto("https://www.linkedin.com/feed/", timeout=30000, wait_until="domcontentloaded")
        await asyncio.sleep(3) # Let UI settle
        
        # 4. Health Gate
        is_healthy, reason = await check_page_health(page)
        
        if not is_healthy:
            logger.warning(f"Profile {profile_id} failed Health Gate: {reason}. Aborting.")
            status = "FLAGGED"
        else:
            # 5. Perform Actions
            logger.info(f"Profile {profile_id} is healthy. Performing actions...")
            await perform_random_action(page)
            status = "SUCCESS"
            reason = "WARMUP_COMPLETE"
            
    except Exception as e:
        logger.error(f"Error during warmup for {profile_id}: {e}")
        status = "ERROR"
        reason = str(e)[:100]
        
    finally:
        # 6. Teardown
        if browser:
            await teardown_browser(browser)
            
        # Stop GoLogin Profile
        stop_profile(profile_id)
        
        # Log to DB
        log_session(profile_id, status, reason)
        logger.info(f"Finished job for profile: {profile_id}. Status: {status}")
