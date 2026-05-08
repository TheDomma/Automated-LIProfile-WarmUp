# 🤖 LinkedIn Profile Maintenance Assistant

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-Async-green.svg)](https://playwright.dev/python/)

A lightweight, local automation tool that eliminates manual profile warm-ups. It seamlessly controls LinkedIn accounts launched via **GoLogin** to simulate passive, human-like behavior (like scrolling the feed and navigating to 'My Network').

---

## ✨ Key Features

*   **🔗 GoLogin Integration**: Effortlessly connects to running GoLogin profiles using their local API.
*   **👤 Human-like Behavior**: Uses randomized delays, smooth JavaScript scrolling, and varied actions to mimic real users.
*   **🛡️ Health Gates**: Automatically detects captchas, restrictions, or logged-out states and safely aborts *before* any actions are taken.
*   **📅 Background Scheduling**: Powered by `APScheduler` to run your daily warmup sessions completely hands-off.
*   **📊 SQLite Reporting**: Logs every session outcome and generates clean daily summaries.

---

## 🛠️ Setup & Installation

Follow these steps to get your assistant up and running!

### Step 1: Prerequisites
- [ ] Install **Python 3.10** or higher.
- [ ] Install the **GoLogin Desktop Application** (It must be running and logged into your account to use the Local API).

### Step 2: Install Dependencies
Open your terminal in the project folder and run:
```bash
# 1. Install python packages
pip install -r requirements.txt

# 2. Install Playwright browsers (chromium)
playwright install chromium
```

### Step 3: Configure Your API Key
- [ ] Open `config.py` in your editor.
- [ ] Update the `GOLOGIN_API_TOKEN` variable with your actual GoLogin API Token. 
*(You can generate this in your GoLogin account settings).*

### Step 4: Add Your Profiles & Initialize the Database
- [ ] Open `seed.py` and replace the placeholder `profile_id`s with your actual GoLogin Profile IDs.
- [ ] Run the setup script to create your local database:
```bash
python seed.py
```
> **🎉 Success!** Your database `linkedin_sessions.db` is now created and ready to track your profiles.

---

## 🚀 How to Use It

### 1️⃣ Start the Automation Scheduler
To kick off the background scheduler (which will randomize and queue up warm-up tasks for your profiles), run:

```bash
python main.py
```
*(Leave this terminal window open so the scheduler can run its background jobs!)*

### 2️⃣ Generate Daily Reports
Want to see how your profiles did today? Open a new terminal window and run:

```bash
python reports/daily_summary.py
```
This will print out exactly which accounts **Succeeded ✅**, **Failed ❌**, or got **Flagged ⚠️**.

---

## 📂 Project Structure

Here is a quick map of the codebase if you want to explore:

*   📁 **`core/`**: The brain! Contains browser connections, health gate checks, and automation actions (scrolling/clicks).
*   📁 **`db/`**: Handles the SQLite database and all queries.
*   📁 **`jobs/`**: Contains the worker script for individual profiles and the scheduler dispatcher.
*   📁 **`reports/`**: Scripts to analyze your database and generate summaries.
*   📄 **`config.py`**: Your central hub for API tokens and timeouts.
*   📄 **`seed.py`**: A quick script to populate the database with your initial profiles.

---

## 🛑 Troubleshooting & Error Handling

**What happens if LinkedIn flags an account?**
If the assistant encounters a Captcha, a "Restricted" notice, or is simply logged out, it triggers the **Health Gate**.
1. The browser immediately closes.
2. The account is marked as `FLAGGED` in your database.
3. The scheduler will **skip** this account in future runs until you manually log in, fix the issue, and reset its status in the DB.

Check your `bot.log` file or run the Daily Summary report to see exactly why an account was flagged!
