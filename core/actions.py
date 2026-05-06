import asyncio
import random
import logging
from playwright.async_api import Page

logger = logging.getLogger(__name__)

async def simulate_human_scroll(page: Page):
    """
    Simulates a human slowly scrolling down the feed using Javascript window.scrollBy.
    This guarantees scrolling even if the page doesn't have focus.
    """
    scrolls = random.randint(3, 7)
    logger.info(f"Simulating {scrolls} scroll actions using JS window.scrollBy.")
    
    for i in range(scrolls):
        scroll_amount = random.randint(400, 800)
        
        # We use JS scrollBy which bypasses any focus or mouse interception issues
        await page.evaluate(f"window.scrollBy({{top: {scroll_amount}, left: 0, behavior: 'smooth'}});")
        
        # Random human pause to "read"
        pause = random.uniform(2.0, 7.0)
        logger.info(f"Scroll {i+1}/{scrolls} complete. Pausing for {pause:.1f} seconds...")
        await asyncio.sleep(pause)

async def perform_random_action(page: Page):
    """
    Picks a random passive action (mostly scrolling).
    """
    action_weights = {
        "scroll_feed": 80,
        "visit_network": 10,
        "idle": 10
    }
    
    action = random.choices(
        list(action_weights.keys()), 
        weights=list(action_weights.values()), 
        k=1
    )[0]
    
    logger.info(f"Selected action: {action}")
    
    if action == "scroll_feed":
        await simulate_human_scroll(page)
        
    elif action == "visit_network":
        logger.info("Navigating to My Network...")
        try:
            # wait_until="domcontentloaded" prevents timeouts from slow proxy ads
            await page.goto("https://www.linkedin.com/mynetwork/", timeout=30000, wait_until="domcontentloaded")
        except Exception as e:
            logger.warning(f"Network page took too long, but proceeding anyway: {e}")
            
        await asyncio.sleep(random.uniform(3.0, 5.0))
        await simulate_human_scroll(page)
        
    elif action == "idle":
        idle_time = random.uniform(10.0, 20.0)
        logger.info(f"Idling for {idle_time:.2f} seconds...")
        await asyncio.sleep(idle_time)