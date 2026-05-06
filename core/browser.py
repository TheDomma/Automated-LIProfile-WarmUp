import logging
from playwright.async_api import async_playwright, Browser

logger = logging.getLogger(__name__)

async def connect_to_browser(ws_url: str) -> Browser:
    """
    Connects to the Orbita browser via Playwright CDP.
    """
    logger.info("Connecting to Playwright via CDP...")
    playwright = await async_playwright().start()
    browser = await playwright.chromium.connect_over_cdp(endpoint_url=ws_url)
    return browser

async def teardown_browser(browser: Browser):
    """
    Safely closes the Playwright connection.
    """
    if browser:
        logger.info("Closing Playwright browser connection...")
        await browser.close()
