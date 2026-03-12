"""
========================================================
  VTU Internyet - Internship Diary Automation v5.0
  Android Development Sessions Auto-Filler
========================================================

SETUP:
  1. Copy config.example.py to config.py
  2. Fill in your email and password in config.py
  3. Run: python internship_diary_automation.py

REQUIREMENTS:
    pip install selenium webdriver-manager
"""

import time
import random
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# ── Load credentials from config.py ──────────────────────
try:
    import config
    ACCOUNTS = {
        "1": {"email": config.ACCOUNT1_EMAIL, "password": config.ACCOUNT1_PASSWORD, "name": "Account 1"},
        "2": {"email": config.ACCOUNT2_EMAIL, "password": config.ACCOUNT2_PASSWORD, "name": "Account 2"},
    }
except ImportError:
    print("⚠️  config.py not found! Please create it from config.example.py")
    print("   Copy config.example.py → config.py and fill in your credentials.\n")
    exit(1)

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WEBDRIVER_MANAGER = True
except ImportError:
    USE_WEBDRIVER_MANAGER = False

SCREENSHOT_DIR = "E:\\files\\"

# ─────────────────────────────────────────────
#   SESSION CONTENT
# ─────────────────────────────────────────────

SESSIONS = [
    {"id":1,  "title":"Introduction to Programming in Kotlin",   "phase":["intro","practice"],
     "concepts":["Kotlin syntax","variables","data types","basic functions","control flow"],
     "skills":["Kotlin"]},
    {"id":2,  "title":"Set up Android Studio",                   "phase":["setup","configuration"],
     "concepts":["Android Studio IDE","SDK installation","AVD Manager","Gradle build system","project structure"],
     "skills":["Kotlin","Android Studio"]},
    {"id":3,  "title":"Build a Basic Layout 1",                  "phase":["design","implementation"],
     "concepts":["Jetpack Compose","composable functions","Column layout","Text components","UI hierarchy"],
     "skills":["Kotlin","Jetpack Compose"]},
    {"id":4,  "title":"Build a Basic Layout 2",                  "phase":["advanced design","testing"],
     "concepts":["Row layout","Box composable","padding and spacing","alignment modifiers","preview annotations"],
     "skills":["Kotlin","Jetpack Compose"]},
    {"id":5,  "title":"Kotlin Fundamentals",                     "phase":["concepts","exercises"],
     "concepts":["null safety","lambda expressions","higher-order functions","classes and objects","when expressions"],
     "skills":["Kotlin"]},
    {"id":6,  "title":"Add a button to an App",                  "phase":["implementation","testing"],
     "concepts":["Button composable","onClick handlers","event listeners","state triggering","recomposition"],
     "skills":["Kotlin","Jetpack Compose"]},
    {"id":7,  "title":"Interact with UI and State - Part 1",     "phase":["state management","practice"],
     "concepts":["remember API","mutableStateOf","state hoisting","unidirectional data flow","composable lifecycle"],
     "skills":["Kotlin","Jetpack Compose"]},
    {"id":8,  "title":"Interact with UI and State - Part 2",     "phase":["advanced state","implementation"],
     "concepts":["ViewModel basics","LiveData","observable state","side effects","LaunchedEffect"],
     "skills":["Kotlin","Jetpack Compose"]},
    {"id":9,  "title":"More Kotlin Fundamentals - Part 1",       "phase":["deep dive","practice"],
     "concepts":["generics","extension functions","data classes","sealed classes","companion objects"],
     "skills":["Kotlin"]},
    {"id":10, "title":"More Kotlin Fundamentals - Part 2",       "phase":["advanced concepts","application"],
     "concepts":["coroutines basics","suspend functions","Kotlin collections","scope functions","delegation"],
     "skills":["Kotlin"]},
    {"id":11, "title":"Build a Scrollable List",                 "phase":["implementation","optimization"],
     "concepts":["LazyColumn","LazyRow","item keys","scroll state","list performance"],
     "skills":["Kotlin","Jetpack Compose"]},
    {"id":12, "title":"Build Beautiful Apps - Part 1",           "phase":["theming","styling"],
     "concepts":["Material Design 3","color schemes","typography system","shape theming","dark mode support"],
     "skills":["Kotlin","Jetpack Compose"]},
    {"id":13, "title":"Build Beautiful Apps - Part 2",           "phase":["polish","finalization"],
     "concepts":["animations","transitions","accessibility","adaptive layouts","final app review"],
     "skills":["Kotlin","Jetpack Compose"]},
]

WORK_SUMMARIES = [
    "Continued working on {session_title} as part of the Android development internship. Focused on {concept1} and {concept2}, applying concepts through hands-on exercises and reviewing documentation.",
    "Dedicated today's session to {session_title}. Explored {concept1} and practical applications of {concept2}. Reviewed code examples to solidify understanding.",
    "Today's work centred around {session_title}. Studied {concept1} and practised {concept2} in small sample projects, cross-referencing materials for a well-rounded understanding.",
    "Focused the day on {session_title}. Worked through {concept1} and observed how {concept2} fits into the broader Android development workflow.",
    "Made progress on {session_title}. Investigated {concept1} and experimented with {concept2} through guided exercises, noting areas for further review.",
    "Spent the session advancing through {session_title}. Studied {concept1} and explored how {concept2} contributes to building functional Android applications.",
    "Worked on {session_title} as planned. Practised {concept1} and examined {concept2} by building small examples using a structured approach.",
]
LEARNINGS = [
    "Gained a better understanding of {concept1} and its integration with Android. Learned that {concept2} plays a key role in building efficient UI components.",
    "Strengthened knowledge of {concept1} and developed clearer insight into {concept2}. These concepts contribute to robust Kotlin-based Android apps.",
    "Improved familiarity with {concept1} and learned practical approaches to {concept2}. Understood how Jetpack Compose simplifies UI compared to XML layouts.",
    "Learned how {concept1} is applied in real Android projects and developed a working understanding of {concept2} and its effect on performance.",
    "Key learning was the practical application of {concept1}. Also developed a clearer grasp of {concept2} in the Android curriculum.",
    "Enhanced understanding of {concept1} and gained hands-on exposure to {concept2}. Recognised how these build on previous sessions.",
    "Deeper understanding of {concept1} and practical knowledge of {concept2}. Connected new learnings with earlier sessions for a complete picture.",
]
BLOCKERS = [
    "No significant blockers today. Progress was smooth and tasks completed as planned.",
    "Faced a minor challenge with {concept1} initially, resolved after reviewing documentation and session notes.",
    "No major issues. Spent a little extra time on {concept1} to ensure full understanding before moving on.",
    "Encountered a brief delay with environment setup, resolved quickly without impacting overall progress.",
    "No blockers to report. Content was clear and well-structured, allowing steady progress throughout.",
    "Small confusion regarding {concept2}, resolved by reviewing code examples effectively.",
    "No major blockers. Some additional time spent revisiting {concept1} from earlier sessions to reinforce understanding.",
]

def generate_entry(day_index, total_days):
    days_per_session = max(1, total_days // len(SESSIONS))
    session_index = min(day_index // max(1, days_per_session), len(SESSIONS) - 1)
    s = SESSIONS[session_index]
    c = s["concepts"]
    c1 = random.choice(c)
    c2 = random.choice([x for x in c if x != c1] or c)
    ctx = {"session_title": s["title"], "concept1": c1, "concept2": c2}
    return {
        "work_summary": random.choice(WORK_SUMMARIES).format(**ctx),
        "learnings":    random.choice(LEARNINGS).format(**ctx),
        "blockers":     random.choice(BLOCKERS).format(**ctx),
        "skills":       s["skills"],
        "hours":        "8",
        "session":      s["title"],
        "phase":        s["phase"][day_index % len(s["phase"])]
    }

# ─────────────────────────────────────────────
#   HELPERS
# ─────────────────────────────────────────────

def human_type(el, text, lo=0.04, hi=0.10):
    for ch in text:
        el.send_keys(ch)
        time.sleep(random.uniform(lo, hi))

def human_pause(lo=0.6, hi=1.5):
    time.sleep(random.uniform(lo, hi))

def screenshot(driver, name):
    path = SCREENSHOT_DIR + name + ".png"
    try:
        driver.save_screenshot(path)
        print(f"   📸 {path}")
    except Exception:
        pass

def create_driver(headless=False):
    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_argument("--window-size=1400,900")
    opts.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    svc = Service(ChromeDriverManager().install()) if USE_WEBDRIVER_MANAGER else Service()
    driver = webdriver.Chrome(service=svc, options=opts)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

# ─────────────────────────────────────────────
#   LOGIN
# ─────────────────────────────────────────────

def login(driver, email, password):
    print(f"\n🔐 Logging in: {email}")
    driver.get("https://vtu.internyet.in/sign-in")
    wait = WebDriverWait(driver, 20)
    time.sleep(3)

    try:
        ef = wait.until(EC.presence_of_element_located((By.XPATH,
            "//input[@type='email' or @name='email' or @id='email' or contains(@placeholder,'mail')]")))
        ef.click(); ef.clear(); human_type(ef, email); human_pause()

        pf = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
        pf.click(); pf.clear(); human_type(pf, password); human_pause()

        btn = wait.until(EC.element_to_be_clickable((By.XPATH,
            "//button[@type='submit'] | //button[contains(translate(text(),"
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'sign')]")))
        btn.click()
        time.sleep(4)

        if "sign-in" not in driver.current_url:
            print(f"   ✅ Logged in → {driver.current_url}")
            return True
        print("   ❌ Still on sign-in page")
        screenshot(driver, "login_failed")
        return False
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        screenshot(driver, "login_error")
        return False

# ─────────────────────────────────────────────
#   CALENDAR PICKER
#   From screenshot: calendar has
#     ◄ button  |  "Mar" <select>  |  "2026" <select>  |  ► button
#     then day number buttons in a grid
# ─────────────────────────────────────────────

MONTH_NAMES = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
MONTH_SHORT  = ["Jan","Feb","Mar","Apr","May","Jun",
                "Jul","Aug","Sep","Oct","Nov","Dec"]

def navigate_calendar(driver, wait, target_date):
    """
    Navigate the calendar (which is already open) to the correct
    month/year using the dropdowns, then click the day.
    Calendar structure from screenshot:
      ◄   [Mar ▾]  [2026 ▾]   ►
      Su Mo Tu We Th Fr Sa
       1  2  3  4  5  6  7 ...
    """
    print(f"   🗓  Navigating calendar to {target_date.strftime('%d %B %Y')}")
    time.sleep(0.5)

    try:
        # ── Set Year via <select> dropdown ──
        target_year  = str(target_date.year)
        target_month = str(target_date.month)  # 1-based

        # Try to find year select (shows "2026")
        try:
            year_select_el = driver.find_element(By.XPATH,
                "//select[option[contains(.,'2026') or contains(.,'2025') or contains(.,'2024')]]")
            Select(year_select_el).select_by_value(target_year)
            print(f"   ✅ Year set to {target_year} via <select>")
            time.sleep(0.4)
        except Exception:
            print("   ℹ️  Year <select> not found, will use arrow navigation")

        # ── Set Month via <select> dropdown ──
        try:
            month_select_el = driver.find_element(By.XPATH,
                "//select[option[contains(.,'Jan') or contains(.,'January') "
                "or contains(.,'Feb') or contains(.,'Mar')]]")
            # Try selecting by value (0-based index common in date pickers)
            try:
                Select(month_select_el).select_by_value(str(target_date.month - 1))
            except Exception:
                try:
                    Select(month_select_el).select_by_value(str(target_date.month))
                except Exception:
                    Select(month_select_el).select_by_visible_text(
                        MONTH_SHORT[target_date.month - 1])
            print(f"   ✅ Month set via <select>")
            time.sleep(0.4)
        except Exception:
            print("   ℹ️  Month <select> not found, will use arrow navigation")

        # ── Fallback: use ◄ ► arrow buttons to reach correct month ──
        for _ in range(36):   # max 3 years of navigation
            # Read current displayed month and year
            cur_month, cur_year = get_displayed_month_year(driver)
            if cur_month is None or cur_year is None:
                break

            if cur_year == target_date.year and cur_month == target_date.month:
                break

            # Decide direction
            cur_total  = cur_year  * 12 + cur_month
            tgt_total  = target_date.year * 12 + target_date.month

            if cur_total > tgt_total:
                click_calendar_arrow(driver, direction="prev")
            else:
                click_calendar_arrow(driver, direction="next")
            time.sleep(0.4)

        # ── Click the day ──
        day = str(target_date.day)
        # Day cells are plain buttons or td/span with just the number
        # Exclude "outside" days (greyed out from prev/next month)
        day_xpath = (
            f"//button[normalize-space(text())='{day}' and not(@disabled) "
            f"and not(contains(@class,'outside')) and not(contains(@class,'disabled'))]"
            f" | //td[normalize-space(text())='{day}' and not(contains(@class,'outside'))]"
            f" | //*[@role='gridcell'][normalize-space(.)='{day}' and not(@aria-disabled='true')]"
        )
        day_btn = wait.until(EC.element_to_be_clickable((By.XPATH, day_xpath)))
        day_btn.click()
        print(f"   ✅ Day {day} clicked")
        human_pause(0.4, 0.8)
        return True

    except Exception as e:
        print(f"   ❌ Calendar navigation failed: {e}")
        screenshot(driver, "calendar_error")
        import traceback; traceback.print_exc()
        return False


def get_displayed_month_year(driver):
    """Read current month and year shown in the open calendar."""
    try:
        # Try reading from select elements first
        selects = driver.find_elements(By.TAG_NAME, "select")
        month_val = year_val = None
        for sel in selects:
            opts = [o.text.strip() for o in sel.find_elements(By.TAG_NAME, "option")]
            # Month select has short month names
            if any(m in opts for m in MONTH_SHORT):
                selected = Select(sel).first_selected_option.text.strip()
                if selected in MONTH_SHORT:
                    month_val = MONTH_SHORT.index(selected) + 1
                elif selected in MONTH_NAMES:
                    month_val = MONTH_NAMES.index(selected) + 1
            # Year select has 4-digit years
            if any(len(o) == 4 and o.isdigit() for o in opts):
                selected = Select(sel).first_selected_option.text.strip()
                if selected.isdigit():
                    year_val = int(selected)
        if month_val and year_val:
            return month_val, year_val
    except Exception:
        pass

    # Fallback: read text from calendar header
    try:
        for m_idx, m_name in enumerate(MONTH_NAMES):
            els = driver.find_elements(By.XPATH,
                f"//*[contains(@class,'caption') or contains(@class,'header') or "
                f"contains(@class,'month-year') or contains(@class,'title')]"
                f"[contains(text(),'{m_name}') or contains(text(),'{MONTH_SHORT[m_idx]}')]")
            for el in els:
                txt = el.text
                for y in range(2020, 2030):
                    if str(y) in txt:
                        return m_idx + 1, y
    except Exception:
        pass

    return None, None


def click_calendar_arrow(driver, direction="prev"):
    """Click the previous or next month arrow in the calendar."""
    if direction == "prev":
        xpaths = [
            "//button[@aria-label='Go to previous month']",
            "//button[@aria-label='previous month']",
            "//button[@aria-label='Previous month']",
            "//button[contains(@class,'prev')]",
            "//button[./*[name()='svg' and contains(@class,'left')]]",
            "(//button[contains(@class,'nav')])[1]",
        ]
    else:
        xpaths = [
            "//button[@aria-label='Go to next month']",
            "//button[@aria-label='next month']",
            "//button[@aria-label='Next month']",
            "//button[contains(@class,'next')]",
            "//button[./*[name()='svg' and contains(@class,'right')]]",
            "(//button[contains(@class,'nav')])[2]",
        ]
    for xp in xpaths:
        try:
            btn = driver.find_element(By.XPATH, xp)
            if btn.is_displayed():
                btn.click()
                return
        except Exception:
            continue


# ─────────────────────────────────────────────
#   STEP 1: Select Internship & Date
# ─────────────────────────────────────────────

def step1_select_internship_and_date(driver, target_date):
    wait = WebDriverWait(driver, 20)
    print(f"\n📅 Step 1: {target_date.strftime('%d %B %Y')}")

    driver.get("https://vtu.internyet.in/dashboard/student/student-diary")
    time.sleep(3)
    screenshot(driver, "step1_loaded")

    try:
        # ── Open internship dropdown ──
        print("   Selecting internship...")
        for xpath in [
            "//*[@role='combobox']",
            "//div[contains(@class,'select__control')]",
            "//div[contains(@class,'Select__control')]",
            "//*[contains(text(),'Choose internship') or contains(text(),'Select Internship')]",
        ]:
            try:
                el = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath)))
                el.click()
                human_pause(0.6, 1.0)
                # Pick first available option
                for opt_xp in [
                    "//*[@role='option']",
                    "//div[contains(@class,'option')]",
                    "//div[contains(@class,'menu-list')]//div",
                ]:
                    try:
                        opt = WebDriverWait(driver, 4).until(
                            EC.element_to_be_clickable((By.XPATH, opt_xp)))
                        opt.click()
                        print("   ✅ Internship selected")
                        break
                    except Exception:
                        continue
                break
            except Exception:
                continue

        human_pause(0.5, 1.0)

        # ── Click the "Pick a Date" field to open the calendar ──
        print("   Opening date picker...")
        date_input_opened = False
        for xpath in [
            "//input[contains(@placeholder,'Pick a Date') or contains(@placeholder,'date') or contains(@placeholder,'Date')]",
            "//*[contains(@placeholder,'Pick a Date')]",
            "//button[contains(@aria-label,'date') or contains(@aria-label,'calendar')]",
            "//*[contains(@class,'date-input') or contains(@class,'DateInput')]",
        ]:
            try:
                el = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, xpath)))
                el.click()
                date_input_opened = True
                print("   ✅ Date field clicked")
                break
            except Exception:
                continue

        human_pause(0.6, 1.0)
        screenshot(driver, "step1_calendar_open")

        # ── Navigate calendar to target month/year, then click day ──
        navigate_calendar(driver, wait, target_date)

        human_pause(0.4, 0.8)

        # ── Click Continue ──
        continue_btn = wait.until(EC.element_to_be_clickable((By.XPATH,
            "//button[contains(text(),'Continue') or contains(text(),'Next') "
            "or contains(text(),'Proceed')]")))
        continue_btn.click()
        print("   ✅ Continue clicked")
        time.sleep(3)
        screenshot(driver, "step1_done")
        return True

    except Exception as e:
        print(f"   ❌ Step 1 failed: {e}")
        screenshot(driver, "step1_error")
        import traceback; traceback.print_exc()
        return False


# ─────────────────────────────────────────────
#   STEP 2: Fill Entry Form
# ─────────────────────────────────────────────

def step2_fill_entry_form(driver, entry):
    wait = WebDriverWait(driver, 20)
    print(f"\n✍️  Step 2: {entry['session']}")
    time.sleep(2)

    if "create-diary-entry" not in driver.current_url:
        driver.get("https://vtu.internyet.in/dashboard/student/create-diary-entry")
        time.sleep(3)

    screenshot(driver, "step2_loaded")

    try:
        # Work Summary
        ws = wait.until(EC.presence_of_element_located((By.XPATH,
            "//textarea[contains(@placeholder,'Briefly') or contains(@placeholder,'work') "
            "or contains(@placeholder,'Work')]")))
        ws.click(); human_pause(0.3, 0.5)
        human_type(ws, entry["work_summary"])
        print("   ✅ Work Summary")
        human_pause()

        # Hours Worked
        hw = wait.until(EC.presence_of_element_located((By.XPATH,
            "//input[@type='number' or contains(@placeholder,'6.5') or contains(@placeholder,'ours')]")))
        hw.click(); hw.send_keys(Keys.CONTROL + "a"); hw.send_keys(Keys.DELETE)
        human_type(hw, entry["hours"])
        print("   ✅ Hours Worked (8)")
        human_pause()

        # Learnings / Outcomes
        lo = wait.until(EC.presence_of_element_located((By.XPATH,
            "//textarea[contains(@placeholder,'learn') or contains(@placeholder,'Learn') "
            "or contains(@placeholder,'ship')]")))
        lo.click(); human_pause(0.3, 0.5)
        human_type(lo, entry["learnings"])
        print("   ✅ Learnings / Outcomes")
        human_pause()

        # Blockers / Risks
        br = wait.until(EC.presence_of_element_located((By.XPATH,
            "//textarea[contains(@placeholder,'slow') or contains(@placeholder,'Block') "
            "or contains(@placeholder,'block') or contains(@placeholder,'Risk') "
            "or contains(@placeholder,'risk')]")))
        br.click(); human_pause(0.3, 0.5)
        human_type(br, entry["blockers"])
        print("   ✅ Blockers / Risks")
        human_pause()

        # Skills Used
        fill_skills(driver, wait, entry["skills"])

        screenshot(driver, "step2_filled")

        # Save
        save = wait.until(EC.element_to_be_clickable((By.XPATH,
            "//button[contains(text(),'Save') or contains(text(),'Submit') or @type='submit']")))
        human_pause(0.5, 1.0)
        save.click()
        print("   ✅ Saved!")
        time.sleep(3)
        screenshot(driver, "step2_saved")
        return True

    except Exception as e:
        print(f"   ❌ Step 2 failed: {e}")
        screenshot(driver, "step2_error")
        import traceback; traceback.print_exc()
        return False


def fill_skills(driver, wait, skills_list):
    try:
        skill_box = driver.find_element(By.XPATH,
            "//*[contains(@placeholder,'skill') or contains(@placeholder,'Skill') "
            "or contains(@placeholder,'Add skills')]"
            " | //div[contains(@class,'select') or contains(@class,'Select')][last()]")
        skill_box.click()
        human_pause(0.5, 1.0)

        for skill in skills_list:
            try:
                inp = driver.find_element(By.XPATH,
                    "//input[@role='combobox'] | "
                    "(//div[contains(@class,'select') or contains(@class,'Select')]//input)[last()]")
                inp.clear(); human_type(inp, skill, 0.05, 0.10); human_pause(0.6, 1.0)
                opt = wait.until(EC.element_to_be_clickable((By.XPATH,
                    f"//*[@role='option'][contains(.,'{skill}')] | "
                    f"//div[contains(@class,'option')][contains(.,'{skill}')] | "
                    f"//li[contains(.,'{skill}')]")))
                opt.click()
                print(f"   ✅ Skill: {skill}")
                human_pause(0.4, 0.8)
            except Exception as e:
                print(f"   ⚠️  Skill '{skill}': {e}")
    except Exception as e:
        print(f"   ⚠️  Skills dropdown: {e}")


# ─────────────────────────────────────────────
#   MAIN
# ─────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  VTU Internyet Diary Automation v5.0")
    print("=" * 60)

    for k, a in ACCOUNTS.items():
        print(f"  {k}) {a['name']} ({a['email']})")
    choice = input("\nWhich account? (1 or 2): ").strip()
    if choice not in ACCOUNTS:
        print("Invalid choice."); return
    acc = ACCOUNTS[choice]

    past = input("How many past days? (0 = today only): ").strip()
    try:
        past = int(past)
    except Exception:
        past = 0

    hl = input("Headless mode? (y/n) [n]: ").strip().lower() == "y"

    today = datetime.today()
    dates = [today - timedelta(days=i) for i in range(past, -1, -1)]
    total = len(dates)

    print(f"\n  Account : {acc['name']}")
    print(f"  Entries : {total}  ({dates[0].strftime('%Y-%m-%d')} → {dates[-1].strftime('%Y-%m-%d')})")
    print("\nStarting in 3s...")
    time.sleep(3)

    driver = create_driver(headless=hl)
    ok_count = fail_count = 0

    try:
        if not login(driver, acc["email"], acc["password"]):
            print("\n❌ Login failed.")
            input("Press Enter to close...")
            return

        human_pause(2, 3)

        for i, d in enumerate(dates):
            print(f"\n{'─'*55}")
            print(f"  Entry {i+1}/{total}  —  {d.strftime('%d %B %Y')}")
            print(f"{'─'*55}")
            entry = generate_entry(i, total)

            if step1_select_internship_and_date(driver, d):
                if step2_fill_entry_form(driver, entry):
                    ok_count += 1
                    print(f"  🎉 Entry done!")
                else:
                    fail_count += 1
            else:
                fail_count += 1

            if i < total - 1:
                p = random.uniform(3, 6)
                print(f"\n  ⏳ Waiting {p:.1f}s...")
                time.sleep(p)

        print(f"\n{'='*60}")
        print(f"  ✅ {ok_count} saved   ❌ {fail_count} failed")
        print(f"{'='*60}")

    except KeyboardInterrupt:
        print("\n⚠️  Stopped by user.")
    except Exception as e:
        print(f"\n❌ Crash: {e}")
        import traceback; traceback.print_exc()
        screenshot(driver, "crash")
    finally:
        input("\nPress Enter to close browser...")
        driver.quit()


if __name__ == "__main__":
    main()
