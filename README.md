linkedin_health_bot/
│
├── main.py                 # Application entry point & APScheduler startup
├── config.py               # Env vars, GoLogin port, standard timeouts
├── requirements.txt
│
├── core/                   # The automation engine
│   ├── gologin.py          # HTTP requests to start/stop GoLogin profiles
│   ├── browser.py          # Playwright CDP connection & teardown
│   ├── health_gate.py      # Logic to detect Captchas, Logouts, Restrictions
│   └── actions.py          # Functions for scrolling, idling, reacting
│
├── jobs/                   # Scheduler logic
│   ├── dispatcher.py       # Decides which accounts run at what time
│   └── worker.py           # The main execution loop for a single account
│
├── db/                     # Database layer
│   ├── database.py         # SQLite connection and table initialization
│   └── queries.py          # Helper functions to log sessions and update status
│
└── reports/                # Output generation
    └── daily_summary.py    # Generates the daily CSV/JSON report