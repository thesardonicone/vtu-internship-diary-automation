# VTU Internyet – Internship Diary Automation
## Android Development Sessions Auto-Filler

---

## 📦 REQUIRED PACKAGES

Install everything with one command:

```bash
pip install selenium webdriver-manager
```

| Package | Purpose |
|---|---|
| `selenium` | Browser automation |
| `webdriver-manager` | Auto-downloads ChromeDriver |

---

## 🌐 HOW TO INSTALL CHROMEDRIVER

### Option A — Automatic (Recommended)
The script uses `webdriver-manager` which auto-downloads the correct ChromeDriver version for your installed Chrome. **No manual installation needed.**

### Option B — Manual
1. Find your Chrome version: Open Chrome → `chrome://settings/help`
2. Download matching ChromeDriver from: https://chromedriver.chromium.org/downloads
3. Place `chromedriver.exe` (Windows) or `chromedriver` (Mac/Linux) in your project folder or add it to your system `PATH`.

---

## 🚀 HOW TO RUN

```bash
python internship_diary_automation.py
```

The script will ask:
1. **Which account?** → Type `1` or `2`
2. **How many past days?** → Type `0` for today only, or a number like `10` for 10 past days
3. **Headless mode?** → Type `y` to run without browser window, `n` to see the browser

---

## 📅 POST-DATED ENTRIES EXAMPLE

If you type **10** for past days, the script fills:
- Day 1 (10 days ago) → Session 1: Intro to Kotlin
- Day 2 (9 days ago) → Session 1: Practice
- Day 3 (8 days ago) → Session 2: Android Studio Setup
- ...and so on, progressing through the 13 sessions
- Final Day (today) → Current session

---

## 🗓️ SCHEDULING DAILY AUTOMATION

### Windows (Task Scheduler)
1. Open **Task Scheduler** → Create Basic Task
2. Trigger: **Daily** at your preferred time
3. Action: **Start a program**
4. Program: `python`
5. Arguments: `C:\path\to\internship_diary_automation.py`
6. Add environment variable for auto-answering prompts:

For fully unattended scheduling, create a `run_daily.bat` file:
```bat
@echo off
echo 1 | echo 0 | python C:\path\to\internship_diary_automation.py
```
Or modify the script to skip input prompts (see "How to Modify" below).

### Mac/Linux (Cron Job)
Open crontab:
```bash
crontab -e
```
Add a line to run daily at 9 AM:
```
0 9 * * * /usr/bin/python3 /path/to/internship_diary_automation.py
```

---

## 🔧 HOW TO MODIFY SESSIONS LATER

The `SESSIONS` list in the script contains all 13 sessions. To add or edit sessions:

```python
SESSIONS = [
    {
        "id": 14,                           # New session number
        "title": "Navigation in Compose",   # Session title
        "phase": ["intro", "practice"],     # Phase labels (used in entry text)
        "concepts": [                        # Key concepts (randomly picked for entries)
            "NavHost",
            "NavController",
            "composable routes",
            "back stack management"
        ],
        "skills": "Kotlin, Jetpack Compose, Navigation"
    },
    # ... existing sessions
]
```

---

## 🛡️ ERROR HANDLING

| Situation | What Happens |
|---|---|
| Wrong credentials | Prints error, exits cleanly |
| Can't find diary link | Prints warning, skips entry |
| Can't find form field | Prints warning, continues with other fields |
| Network error | Saves screenshot as `error_screenshot.png` |
| Script interrupted | Gracefully closes browser |

If login fails, check:
- Credentials are correct
- Site is accessible at https://vtu.internyet.in/
- Run with headless=`n` to see what the browser sees

---

## ⚙️ RUNNING WITHOUT PROMPTS (Automated / Scheduled Mode)

To skip interactive prompts for scheduled runs, edit the bottom of the script:

```python
# Replace:
account_choice = input("Which account should be used? (1 or 2): ").strip()
past_days_input = input("How many past days need entries? ...").strip()

# With hardcoded values:
account_choice = "1"    # Always use Account 1
past_days_input = "0"   # Always fill today only
headless = True         # Always run headless
```

---

## 📁 FILES

| File | Purpose |
|---|---|
| `internship_diary_automation.py` | Main automation script |
| `error_screenshot.png` | Auto-saved on errors (for debugging) |

---

## ⚠️ NOTES

- The script uses **random delays** between keystrokes and actions to simulate human behaviour
- Entry content **varies every day** — no two entries are identical
- Sessions progress **gradually** through the 13-session curriculum
- All 13 Android development sessions are fully covered
