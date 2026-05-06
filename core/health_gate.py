import logging
from playwright.async_api import Page
from typing import Tuple

logger = logging.getLogger(__name__)

async def check_page_health(page: Page) -> Tuple[bool, str]:
    """
    Validates if the LinkedIn page is in a healthy state (Feed loaded, no Captchas/Restrictions).
    Returns (is_healthy, reason).
    """
    logger.info("Executing Health Gate check...")
    
    try:
        # Check URL for obvious logged-out states
        current_url = page.url
        if "login" in current_url or "signup" in current_url:
            return False, "LOGGED_OUT"
            
        # Check for Captcha / Checkpoint
        if await page.locator("#captcha-internal").count() > 0 or await page.locator(".checkpoint-challenge").count() > 0:
            return False, "CAPTCHA_DETECTED"
            
        # Check for Restrictions
        restricted_texts = ["restricted", "verify your identity"]
        for text in restricted_texts:
            if await page.locator(f'h1:has-text("{text}")').count() > 0:
                return False, "RESTRICTED"
                
        # Check for healthy state indicator (Global Nav, Feed, or App Outlet)
        if (await page.locator("#global-nav").count() > 0 or 
            await page.locator(".feed-shared-update-v2").count() > 0 or 
            await page.locator(".scaffold-layout").count() > 0 or
            "feed" in current_url):
            return True, "HEALTHY"
            
        # If we reach here, we are in an unknown state.
        page_title = await page.title()
        logger.warning(f"Unknown DOM State. URL: {current_url} | Title: {page_title}")
        
        # Take a screenshot to help debug what LinkedIn is actually showing
        await page.screenshot(path="debug_unknown_state.png", full_page=True)
        logger.info("Saved screenshot to debug_unknown_state.png for manual review.")
        
        return False, "UNKNOWN_DOM_STATE"

    except Exception as e:
        logger.error(f"Error during Health Gate check: {e}")
        return False, "HEALTH_CHECK_ERROR"
