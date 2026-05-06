import asyncio
import random
import logging
from playwright.async_api import Page

logger = logging.getLogger(__name__)

async def simulate_human_scroll(page: Page):
    """
    Simulates a human slowly scrolling down the feed by hovering over posts and using the mouse wheel.
    This ensures the scroll events target the correct feed container.
    """
    scrolls = random.randint(3, 7)
    logger.info(f"Simulating {scrolls} scroll actions by hovering and wheeling.")
    
    for i in range(scrolls):
        try:
            # Find all feed posts currently loaded
            posts = page.locator(".feed-shared-update-v2")
            count = await posts.count()
            
            if count > 0:
                # Hover over the last visible post to ensure our mouse is over the feed container
                target_index = min((i + 1), count - 1)
                await posts.nth(target_index).hover(timeout=5000)
            
            # Now that the mouse is firmly over the feed, simulate the mouse wheel
            scroll_amount = random.randint(400, 800)
            await page.mouse.wheel(0, scroll_amount)
            
        except Exception as e:
            logger.debug(f"Hover/Wheel failed, trying fallback: {e}")
            # Fallback to center-screen wheel
            viewport = page.viewport_size
            if viewport:
                await page.mouse.move(viewport["width"] / 2, viewport["height"] / 2)
                await page.mouse.wheel(0, 600)
            
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