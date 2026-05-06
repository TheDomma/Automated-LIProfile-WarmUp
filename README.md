# LinkedIn Profile Maintenance Assistant - Design & Architecture Plan

This document outlines the proposed architecture and design for the V1 LinkedIn Profile Maintenance Assistant, addressing the 12 points requested.

## 1. Recommended V1 Architecture
- **Language:** Python 3.10+ (for strong `asyncio` support).
- **Automation Framework:** Playwright (Async version). Playwright is faster, more reliable, and better suited for attaching to existing browser instances than Selenium.
- **Profile Management:** GoLogin Local API. This allows starting/stopping profiles programmatically.
- **Task Scheduling:** `APScheduler` (AsyncIOScheduler). It runs purely in Python without needing external services like Redis/Celery for V1.
- **Database:** SQLite. It's built into Python, requires zero setup, and is perfect for storing session logs, account statuses, and generating daily reports. It can be easily migrated to PostgreSQL later.

## 2. Project Folder Structure
Your proposed structure in `README.md` is excellent. We will use exactly that. It strongly separates concerns (core automation, jobs/scheduling, database, reports).

## 3. Best Playwright + GoLogin Integration Method
The most reliable method is to use GoLogin's **Local API** (requires the GoLogin app to be running on the machine) to start the profile and retrieve the debugging URL, then attach Playwright to it.
1. Make a `GET` request to `http://localhost:35000/browser/start-profile?profileId=<ID>`
2. Parse the JSON response to get the `wsUrl`.
3. Use Playwright's `chromium.connect_over_cdp(endpoint_url=wsUrl)` to attach to the Orbita browser.
4. When finished, use Playwright to close the pages, and then `GET http://localhost:35000/browser/stop-profile?profileId=<ID>`.

## 4. Scheduler Design
We need a natural, randomized schedule.
- Run a **Dispatcher Job** every morning (e.g., 8:00 AM) using `cron` trigger in APScheduler.
- The Dispatcher pulls all active `profile_id`s from the DB.
- For each profile, it generates a random timestamp between 9:00 AM and 5:00 PM.
- It then schedules a one-off `date` job in APScheduler to execute the **Worker Job** for that specific profile at that exact random time.

## 5. Randomization Logic Ideas
To prevent detection, everything must be randomized within bounds:
- **Session Duration:** 3 to 8 minutes.
- **Scroll Behavior:** Scroll down between 300px and 800px. Wait a random interval (`random.uniform(2.0, 7.0)` seconds). Scroll again. Sometimes scroll up slightly to simulate human reading.
- **Action Selection:** Use weighted random choices. For example:
  - 70% chance to just scroll the Home Feed.
  - 15% chance to visit "My Network" and scroll.
  - 10% chance to visit a random connection's profile.
  - 5% chance to react (Like/Celebrate) to a post on the feed.

## 6. Health-State Detection Logic (Health Gate)
After attaching Playwright and navigating to `https://www.linkedin.com/feed/`, wait for the page to load and perform a rapid DOM check.
- **Normal State:** Check for `#global-nav` or `.feed-shared-update-v2`. If present, proceed.
- **Logged Out:** If the URL redirects to `/login` or the login form is present, mark as `LOGGED_OUT` and stop.
- **Captcha/Security:** Check for `#captcha-internal`, `.checkpoint-challenge`, or any `iframe` related to captchas. Mark as `CAPTCHA_DETECTED` and stop.
- **Restricted:** Look for `h1` tags containing "restricted" or "verify your identity". Mark as `RESTRICTED` and stop.
*Crucial:* If any bad state is detected, close the browser immediately and update the SQLite database so it's flagged for manual review.

## 7. Error Handling / Retry Strategy
- **Timeouts/Network Errors:** If Playwright fails to load the page (TimeoutError), close the profile, wait 5 minutes, and retry *once*. If it fails again, log as `PAGE_LOAD_ERROR`.
- **Unexpected DOM:** If LinkedIn changes its layout and the automation can't find selectors, fail gracefully, close the profile, and log `DOM_ERROR`.
- **Fatal States:** NEVER retry if a Captcha or Restriction is detected.

## 8. Logging & Report Generation
- **Logging:** Use Python's built-in `logging` module to output to both the console (for real-time monitoring) and a rotating file (`bot.log`).
- **Reports:** At 6:00 PM daily, a scheduled job runs `reports/daily_summary.py`. It queries the SQLite database for that day's sessions, counts Success/Failed/Flagged profiles, and generates a simple CSV or markdown report.

## 9. Recommended Scaling Strategy (for 100+ accounts)
- **V1 (Local):** 100 accounts over an 8-hour workday means roughly 12 accounts per hour, or 1 account every 5 minutes. You can run these **sequentially** (one at a time) on a single machine without any concurrency. This is incredibly stable and uses minimal RAM.
- **V2 (Future):** If you need them to run faster, you can use `asyncio.Semaphore(3)` to run a maximum of 3 browsers concurrently on a standard PC. For 100+ accounts, a single machine is perfectly fine as long as you limit concurrency.

## 10. Sample Python + Playwright Starter Structure
(I have scaffolded the actual boilerplate files in the workspace for you to review!)

## 11. MVP Roadmap (Week 1 → Week 4)
- **Week 1: Core Connectivity.** Set up GoLogin Local API calls. Connect Playwright via CDP. Successfully launch a profile, navigate to LinkedIn, and close it.
- **Week 2: Health Gate & Actions.** Implement the health detection logic (detecting Captchas, logged-out states). Implement randomized scrolling and idling.
- **Week 3: Database & Scheduling.** Integrate SQLite to log successes/failures. Implement the APScheduler dispatcher to randomize daily run times for all profiles.
- **Week 4: Reporting & Hardening.** Implement the daily CSV report generation. Add robust error handling (timeouts, retries). Test with 5-10 actual accounts before rolling out to all 100.

## 12. Recommended VS Code Setup
- **Extensions:**
  - `Python` (Microsoft)
  - `Pylance`
  - `Black Formatter` (for consistent code styling)
  - `SQLite Viewer` (to easily inspect the local database)
- **Settings:** I have added a `.vscode/settings.json` file to automatically format your code on save.
