import asyncio
import logging
import random
import time
from typing import Literal

from playwright.async_api import Error, Page, TimeoutError as PlaywrightTimeoutError

logger = logging.getLogger(__name__)

v1-stable-bot
async def simulate_human_scroll(page: Page):
    """
    Simulates a human slowly scrolling down the feed.
    Uses window.scrollBy for more reliable scrolling across different layouts.
    """
    scrolls = random.randint(3, 7)
    logger.info(f"Simulating {scrolls} scroll actions.")
    
    for i in range(scrolls):
        try:
            # Ensure page is focused
            await page.evaluate("window.focus()")
            
            # Use smooth scrolling via window.scrollBy
            scroll_amount = random.randint(400, 800)
            await page.evaluate(f"window.scrollBy({{top: {scroll_amount}, behavior: 'smooth'}});")
            
        except Exception as e:
            logger.debug(f"Smooth scroll failed, trying fallback: {e}")
            # Fallback to keyboard PageDown
            await page.keyboard.press("PageDown")
            
        # Random human pause to "read"
        pause = random.uniform(2.0, 7.0)
        logger.info(f"Scroll {i+1}/{scrolls} complete. Pausing for {pause:.1f} seconds...")
        await asyncio.sleep(pause)
=======
ScrollMode = Literal["keyboard", "wheel", "javascript"]


async def detect_linkedin_state(page: Page) -> str:
    """Returns FEED, LOGIN, CAPTCHA, CHECKPOINT, or UNKNOWN."""
    current_url = page.url.lower()

    if "linkedin.com/login" in current_url or "linkedin.com/checkpoint/lg/sign-in" in current_url:
        return "LOGIN"

    # Broad selectors used by LinkedIn for challenge pages
    captcha_or_checkpoint_selectors = [
        "#captcha-internal",
        ".checkpoint-challenge",
        "form#captcha-challenge",
        "[action*='checkpoint/challenge']",
    ]

    for selector in captcha_or_checkpoint_selectors:
        if await page.locator(selector).count() > 0:
            return "CAPTCHA"

    if "checkpoint" in current_url:
        return "CHECKPOINT"

    if "linkedin.com/feed" in current_url and await page.locator("#global-nav").count() > 0:
        return "FEED"

    return "UNKNOWN"


async def wait_for_feed_ready(page: Page, timeout_ms: int = 45000) -> bool:
    """Wait for feed navigation + essential UI and stabilize load state."""
    logger.info("Waiting for LinkedIn feed to become ready...")

    try:
        await page.wait_for_url("**linkedin.com/feed/**", timeout=timeout_ms)
    except PlaywrightTimeoutError:
        logger.warning("Timed out waiting for feed URL. Current URL: %s", page.url)
        return False

    try:
        # networkidle can be noisy on social apps, so we do best-effort and continue.
        await page.wait_for_load_state("domcontentloaded", timeout=15000)
        try:
            await page.wait_for_load_state("networkidle", timeout=10000)
        except PlaywrightTimeoutError:
            logger.info("networkidle timeout; continuing with DOM-ready state.")

        await page.locator("#global-nav").wait_for(state="visible", timeout=15000)
    except PlaywrightTimeoutError:
        logger.warning("Feed shell did not fully load in time.")
        return False

    # Set focus so keyboard events land where expected.
    try:
        await page.locator("body").click(position={"x": 300, "y": 300}, timeout=5000)
    except Error:
        # fallback if body is blocked by overlay
        await page.mouse.click(300, 300)

    await asyncio.sleep(random.uniform(1.0, 2.0))
    logger.info("Feed ready and focused for passive scrolling.")
    return True


async def perform_scroll_step(page: Page, step: int, total: int) -> ScrollMode:
    """One human-like scroll step with fallbacks."""
    mode: ScrollMode = "keyboard"

    try:
        presses = random.choice([1, 1, 1, 2])
        for _ in range(presses):
            await page.keyboard.press("PageDown")
            await asyncio.sleep(random.uniform(0.2, 0.6))
    except Error:
        mode = "wheel"
        try:
            await page.mouse.wheel(0, random.randint(450, 800))
        except Error:
            mode = "javascript"
            await page.evaluate(
                "window.scrollBy({top: arguments[0], left: 0, behavior: 'smooth'})",
                random.randint(400, 750),
            )

    pause = random.uniform(2.5, 7.5)
    logger.info("Scroll step %s/%s via %s; pause %.1fs", step, total, mode, pause)
    await asyncio.sleep(pause)
    return mode


async def simulate_human_feed_browsing(page: Page, duration_seconds: int | None = None):
    """Stable, low-intensity passive browsing loop for feed pages."""
    if duration_seconds is None:
        duration_seconds = random.randint(140, 260)  # ~2.3 to 4.3 minutes

    if not await wait_for_feed_ready(page):
        raise RuntimeError("FEED_NOT_READY")

    state = await detect_linkedin_state(page)
    if state != "FEED":
        raise RuntimeError(f"UNHEALTHY_PAGE_STATE:{state}")

    start = time.monotonic()
    step = 1
    logger.info("Starting passive feed browsing for ~%ss", duration_seconds)

    while time.monotonic() - start < duration_seconds:
        state = await detect_linkedin_state(page)
        if state != "FEED":
            raise RuntimeError(f"STATE_CHANGED_DURING_BROWSE:{state}")

        await perform_scroll_step(page, step, max(1, duration_seconds // 5))
        step += 1

        # occasional long reading pause
        if random.random() < 0.18:
            long_pause = random.uniform(8.0, 18.0)
            logger.info("Taking longer read pause: %.1fs", long_pause)
            await asyncio.sleep(long_pause)
main

async def perform_random_action(page: Page):
    """Passive behavior entrypoint with robust state checks."""
    action_weights = {
        "scroll_feed": 88,
        "visit_network": 7,
        "idle": 5,
    }

    action = random.choices(
        list(action_weights.keys()),
        weights=list(action_weights.values()),
        k=1,
    )[0]

    logger.info("Selected action: %s", action)

    if action == "scroll_feed":
        await simulate_human_feed_browsing(page)

    elif action == "visit_network":
        logger.info("Navigating to My Network...")
        await page.goto("https://www.linkedin.com/mynetwork/", timeout=30000, wait_until="domcontentloaded")
        await asyncio.sleep(random.uniform(3.0, 6.0))
        await page.goto("https://www.linkedin.com/feed/", timeout=30000, wait_until="domcontentloaded")
        await simulate_human_feed_browsing(page, duration_seconds=random.randint(90, 180))

    else:
        idle_time = random.uniform(10.0, 20.0)
        logger.info("Idling for %.1fs", idle_time)
        await asyncio.sleep(idle_time)
