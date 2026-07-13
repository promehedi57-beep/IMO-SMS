#!/usr/bin/env python
# -*- coding: utf-8 -*-
# FB Creator Pro - Python 2.7/3 Compatible

import os, sys, json, time, random, string, threading, re
from datetime import datetime
from queue import Queue

# Python 2/3 compatibility
if sys.version_info[0] < 3:
    input = raw_input
    string.ascii_lowercase = string.ascii_lowercase.decode('ascii') if hasattr(string.ascii_lowercase, 'decode') else string.ascii_lowercase

# Try imports
try:
    import requests
except ImportError:
    print("\033[1;31m[!] Install requests: pip install requests\033[0m")
    sys.exit(1)

try:
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
except:
    pass

# ═══════════════════════════════════════════════════════
# COLORS
# ═══════════════════════════════════════════════════════
class C:
    R = '\033[0;31m'
    G = '\033[0;32m'
    Y = '\033[1;33m'
    B = '\033[0;34m'
    M = '\033[0;35m'
    CY = '\033[0;36m'
    W = '\033[0;37m'
    D = '\033[2m'
    N = '\033[0m'
    BD = '\033[1m'
    UN = '\033[4m'

# ═══════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════
CONFIG = {
    "method": "automail",
    "count": 5,
    "threads": 3,
    "delay": 2.0,
    "timeout": 20,
    "country": "Bangladesh",
    "gender": "male",
    "password": "",
    "custom_name": "",
    "birth_day": 15,
    "birth_month": 6,
    "birth_year": 1998,
    "use_proxy": False,
    "proxy_file": "proxies.txt",
    "email_file": "emails.txt",
    "number_file": "numbers.txt",
    "created": 0,
    "success": 0,
    "failed": 0,
    "running": False
}

ACCOUNTS_DIR = "created_accounts"
if not os.path.exists(ACCOUNTS_DIR):
    os.makedirs(ACCOUNTS_DIR)

# ═══════════════════════════════════════════════════════
# NAMES
# ═══════════════════════════════════════════════════════
NAMES = {
    "Bangladesh": {
        "male": ["MD Rakib Hasan", "Shahidul Islam", "Abdur Rahman", "Minhaz Hossain", 
                 "Tanvir Ahmed", "Fahim Hasan", "Nazmul Islam", "Rabiul Hasan",
                 "Jahid Hasan", "Sohel Rana", "Kawsar Ahmed", "Milon Hossain"],
        "female": ["Fatima Begum", "Ayesha Khatun", "Nasrin Akter", "Shahnaz Parvin",
                   "Rina Begum", "Jamila Khatun", "Hosneara Begum", "Shamima Akter"]
    },
    "India": {
        "male": ["Rajesh Kumar", "Amit Sharma", "Vikram Singh", "Suresh Patel", "Deepak Verma"],
        "female": ["Priya Sharma", "Suman Devi", "Neha Gupta", "Pooja Singh", "Anita Verma"]
    },
    "Pakistan": {
        "male": ["Muhammad Ali", "Ahmed Khan", "Hassan Raza", "Bilal Ahmed", "Usman Malik"],
        "female": ["Sana Khan", "Ayesha Malik", "Fatima Ali", "Zainab Ahmed", "Hira Butt"]
    },
    "USA": {
        "male": ["James Smith", "John Johnson", "Robert Williams", "Michael Brown", "David Jones"],
        "female": ["Mary Smith", "Jennifer Johnson", "Linda Williams", "Patricia Brown", "Elizabeth Jones"]
    },
    "UAE": {
        "male": ["Mohammed Al-Rashid", "Ahmed Al-Maktoum", "Ali Al-Nahyan", "Omar Al-Sayed", "Khalid Hassan"],
        "female": ["Mariam Al-Mansoori", "Fatima Al-Suwaidi", "Aisha Al-Nuaimi", "Noora Al-Kaabi", "Sara Al-Hashimi"]
    }
}

COUNTRIES = {
    "1": "Bangladesh", "2": "India", "3": "Pakistan", "4": "USA", "5": "UAE"
}

# ═══════════════════════════════════════════════════════
# USER AGENTS
# ═══════════════════════════════════════════════════════
UAS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-A515F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.81 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 13_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 9; SM-J730F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.93 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 8.0.0; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.109 Mobile Safari/537.36"
]

# ═══════════════════════════════════════════════════════
# UI HELPERS
# ═══════════════════════════════════════════════════════
def clear():
    os.system("clear" if os.name != "nt" else "cls")

def line(char="═", length=60, color=C.CY):
    sys.stdout.write(color + (char * length) + C.N + "\n")

def box(text, color=C.CY, width=60):
    print(color + "╔" + ("═" * (width-2)) + "╗" + C.N)
    for line_text in text.split("\n"):
        pad = max(0, width - 4 - len(line_text))
        sys.stdout.write(color + "║ " + C.N + line_text + " " * pad + color + " ║" + C.N + "\n")
    print(color + "╚" + ("═" * (width-2)) + "╝" + C.N)

def banner():
    clear()
    print(C.CY + """
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║          ███████╗██████╗      ██████╗██████╗ ███████╗   ║
    ║          ██╔════╝██╔══██╗   ██╔════╝██╔══██╗██╔════╝   ║
    ║          █████╗  ██████╔╝   ██║     ██████╔╝█████╗     ║
    ║          ██╔══╝  ██╔══██╗   ██║     ██╔══██╗██╔══╝     ║
    ║          ██║     ██████╔╝   ╚██████╗██║  ██║███████╗   ║
    ║          ╚═╝     ╚═════╝     ╚═════╝╚═╝  ╚═╝╚══════╝   ║
    ║                                                          ║
    ║         Facebook Account Creator Pro v2.5                 ║
    ║         Termux Compatible | Python 2.7/3                  ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """ + C.N)

def anim(text, duration=2):
    chars = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    end = time.time() + duration
    i = 0
    sys.stdout.write(C.CY + "  " + C.N)
    sys.stdout.flush()
    while time.time() < end:
        sys.stdout.write("\b" + chars[i % len(chars)])
        sys.stdout.write(C.CY + " " + text + C.N)
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print(C.G + " ✓" + C.N)

# ═══════════════════════════════════════════════════════
# CORE FUNCTIONS
# ═══════════════════════════════════════════════════════
def load_file(path):
    try:
        with open(path, "r") as f:
            return [l.strip() for l in f.readlines() if l.strip()]
    except:
        return []

def gen_password():
    if CONFIG["password"]:
        return CONFIG["password"]
    pwd = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    return pwd + "A1@"

def gen_temp_email():
    user = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(12))
    return user + "@1secmail.com"

def get_random_name():
    if CONFIG["custom_name"]:
        return CONFIG["custom_name"]
    country = CONFIG["country"]
    gender = CONFIG["gender"]
    if country not in NAMES:
        country = "Bangladesh"
    if gender not in NAMES[country]:
        gender = "male"
    return random.choice(NAMES[country][gender])

def get_proxy(proxies, idx=[0]):
    if not CONFIG["use_proxy"] or not proxies:
        return None
    with threading.Lock():
        p = proxies[idx[0] % len(proxies)]
        idx[0] += 1
    return {"http": "http://" + p, "https": "http://" + p}

def check_mail_code(email, session):
    """Check 1secmail inbox for Facebook code"""
    try:
        user, domain = email.split("@")
        url = "https://www.1secmail.com/api/v1/?action=getMessages&login={}&domain={}".format(user, domain)
        r = session.get(url, timeout=15)
        if r.status_code == 200:
            try:
                msgs = r.json()
            except:
                return None
            if msgs and len(msgs) > 0:
                msg_id = msgs[0].get("id")
                if msg_id:
                    url2 = "https://www.1secmail.com/api/v1/?action=readMessage&login={}&domain={}&id={}".format(user, domain, msg_id)
                    r2 = session.get(url2, timeout=15)
                    if r2.status_code == 200:
                        try:
                            data = r2.json()
                        except:
                            return None
                        body = str(data.get("body", "")) + " " + str(data.get("htmlBody", ""))
                        patterns = [
                            r'(\d{5,6})',
                            r'code[:\s]*(\d{5,6})',
                            r'FB[\s\-]?(\d{5,6})',
                            r'confirm[:\s]*(\d{5,6})'
                        ]
                        for p in patterns:
                            m = re.search(p, body, re.IGNORECASE)
                            if m:
                                return m.group(1)
    except:
        pass
    return None

def extract_form(html, form_name=None):
    """Extract form fields from HTML"""
    fields = {}
    pattern = r'<input[^>]+name="([^"]+)"[^>]+value="([^"]*)"'
    for m in re.finditer(pattern, html):
        name = m.group(1)
        val = m.group(2)
        if name not in fields:
            fields[name] = val
    return fields

def extract_between(text, start, end):
    try:
        s = text.index(start) + len(start)
        e = text.index(end, s)
        return text[s:e]
    except:
        return ""

def create_account(email, password, name, proxies, idx):
    """Create single Facebook account via mbasic"""
    try:
        parts = name.split(" ", 1)
        first = parts[0]
        last = parts[1] if len(parts) > 1 else "Khan"
        
        ua = random.choice(UAS)
        proxy = get_proxy(proxies)
        
        session = requests.Session()
        session.headers.update({
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate"
        })
        
        # Step 1: Get signup page
        r1 = session.get("https://mbasic.facebook.com/reg/?cid=102&refid=8", 
                         proxies=proxy, timeout=CONFIG["timeout"])
        
        if r1.status_code != 200:
            return {"ok": False, "error": "Page load failed: " + str(r1.status_code), "email": email, "password": password, "name": name}
        
        # Step 2: Fill form
        fields = extract_form(r1.text)
        
        form_data = {
            "firstname": first,
            "lastname": last,
            "reg_email__": email,
            "reg_email_confirmation__": email,
            "reg_passwd__": password,
            "birthday_day": str(CONFIG["birth_day"]),
            "birthday_month": str(CONFIG["birth_month"]),
            "birthday_year": str(CONFIG["birth_year"]),
            "sex": "2" if CONFIG["gender"] == "male" else "1",
            "referrer": "",
            "asked_to_login": "",
            "terms": "on",
            "ns": "0",
            "sk": "",
            "lsd": fields.get("lsd", ""),
            "jazoest": fields.get("jazoest", ""),
            "ccp": "",
            "reg_instance": fields.get("reg_instance", ""),
            "recaptcha_type": "password",
            "captcha_persist_data": "",
            "captcha_response": ""
        }
        
        # Update headers for POST
        headers_post = {
            "User-Agent": ua,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://mbasic.facebook.com/reg/?cid=102&refid=8"
        }
        
        r2 = session.post("https://mbasic.facebook.com/reg/", 
                          data=form_data, 
                          headers=headers_post,
                          proxies=proxy, 
                          timeout=CONFIG["timeout"],
                          allow_redirects=True)
        
        response_text = r2.text
        response_url = r2.url
        
        # Check for confirmation
        if "confirm" in response_url.lower() or "code" in response_url.lower() or "checkpoint" in response_url.lower() or "confirmemail" in response_url.lower():
            # Need confirmation code
            code = None
            for attempt in range(24):  # 2 minutes
                time.sleep(5)
                code = check_mail_code(email, session)
                if code:
                    break
            
            if code:
                # Submit code
                confirm_fields = extract_form(response_text)
                confirm_data = dict(confirm_fields)
                confirm_data["code"] = code
                confirm_data["submit"] = "Confirm"
                
                r3 = session.post(response_url, 
                                 data=confirm_data, 
                                 headers=headers_post,
                                 proxies=proxy, 
                                 timeout=CONFIG["timeout"],
                                 allow_redirects=True)
                
                if "home" in r3.url.lower() or "welcome" in r3.url.lower() or r3.status_code == 200:
                    return {
                        "ok": True, 
                        "name": name, 
                        "email": email, 
                        "password": password,
                        "code": code,
                        "cookies": session.cookies.get_dict(),
                        "ua": ua
                    }
            else:
                return {
                    "ok": False, 
                    "error": "Code timeout (2 min)", 
                    "email": email, 
                    "password": password, 
                    "name": name,
                    "url": response_url
                }
        
        if "home" in response_url.lower() or "welcome" in response_url.lower():
            return {
                "ok": True, 
                "name": name, 
                "email": email, 
                "password": password,
                "code": "AUTO-OK",
                "cookies": session.cookies.get_dict(),
                "ua": ua
            }
        
        # Detect errors
        if "error" in response_text.lower() or "invalid" in response_text.lower():
            err_msg = extract_between(response_text, '<div id="reg_error_inner" class="_52jb">', '<').strip()
            if not err_msg:
                err_msg = extract_between(response_text, 'class="error">', '<').strip()
            if not err_msg:
                err_msg = "Form rejected"
            return {"ok": False, "error": err_msg[:80], "email": email, "password": password, "name": name}
        
        return {
            "ok": True, 
            "name": name, 
            "email": email, 
            "password": password,
            "code": "AUTO-OK",
            "cookies": session.cookies.get_dict(),
            "ua": ua,
            "url": response_url
        }
        
    except Exception as e:
        return {"ok": False, "error": str(e)[:80], "email": email, "password": password, "name": name}

# ═══════════════════════════════════════════════════════
# WORKER
# ═══════════════════════════════════════════════════════
def worker(q, proxies, lock):
    while CONFIG["running"]:
        try:
            job = q.get(timeout=1)
            if job is None:
                break
            
            idx, email, pwd, name = job
            
            with lock:
                CONFIG["created"] += 1
                cur = CONFIG["created"]
            
            print(C.CY + "  [" + str(cur).rjust(3) + "] " + C.N + "Trying: " + C.Y + email + C.N + " ... ", end="", flush=True)
            
            result = create_account(email, pwd, name, proxies, idx)
            
            with lock:
                if result.get("ok"):
                    CONFIG["success"] += 1
                    print(C.G + "✓ OK" + C.N)
                    save_account(result, "success")
                else:
                    CONFIG["failed"] += 1
                    print(C.R + "✗ FAIL: " + (result.get("error", "Unknown")[:40]) + C.N)
                    save_account(result, "failed")
            
            q.task_done()
            time.sleep(CONFIG["delay"])
        except:
            continue

def save_account(result, status):
    try:
        method = CONFIG["method"]
        if status == "success":
            fpath = os.path.join(ACCOUNTS_DIR, method + "_accounts.txt")
            with open(fpath, "a", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("Account #" + str(CONFIG["success"]) + "\n")
                f.write("Name     : " + str(result.get("name", "")) + "\n")
                f.write("Email    : " + str(result.get("email", "")) + "\n")
                f.write("Password : " + str(result.get("password", "")) + "\n")
                f.write("Code     : " + str(result.get("code", "")) + "\n")
                f.write("Country  : " + CONFIG["country"] + "\n")
                f.write("Gender   : " + CONFIG["gender"] + "\n")
                f.write("B-Date   : " + str(CONFIG["birth_day"]) + "/" + str(CONFIG["birth_month"]) + "/" + str(CONFIG["birth_year"]) + "\n")
                f.write("Method   : " + method + "\n")
                f.write("Date     : " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
                cookies = result.get("cookies", {})
                if cookies:
                    f.write("Cookies  : " + json.dumps(cookies) + "\n")
                f.write("=" * 60 + "\n\n")
        else:
            fpath = os.path.join(ACCOUNTS_DIR, "failed_accounts.txt")
            with open(fpath, "a", encoding="utf-8") as f:
                f.write(str(result.get("email", "")) + " | " + 
                        str(result.get("password", "")) + " | " + 
                        str(result.get("name", "")) + " | " + 
                        str(result.get("error", "")) + "\n")
    except:
        pass

# ═══════════════════════════════════════════════════════
# CONFIG PERSISTENCE
# ═══════════════════════════════════════════════════════
def load_config():
    if os.path.exists("fb_config.json"):
        try:
            with open("fb_config.json", "r") as f:
                data = json.load(f)
                for k in data:
                    if k in CONFIG:
                        CONFIG[k] = data[k]
        except:
            pass

def save_config():
    try:
        cfg = dict(CONFIG)
        cfg["running"] = False
        cfg["created"] = 0
        cfg["success"] = 0
        cfg["failed"] = 0
        with open("fb_config.json", "w") as f:
            json.dump(cfg, f, indent=2)
    except:
        pass

# ═══════════════════════════════════════════════════════
# MAIN CREATOR
# ═══════════════════════════════════════════════════════
def start_creator():
    if CONFIG["running"]:
        print(C.R + "\n[!] Already running! Press X first to stop.\n" + C.N)
        return
    
    method = CONFIG["method"]
    count = CONFIG["count"]
    proxies = load_file(CONFIG["proxy_file"]) if CONFIG["use_proxy"] else []
    
    accounts = []
    if method == "email":
        emails = load_file(CONFIG["email_file"])
        if not emails:
            print(C.R + "\n[!] No emails in " + CONFIG["email_file"] + C.N)
            print(C.Y + "    Add emails to file, or choose method 3 (Auto Mail)" + C.N)
            return
        if count > len(emails):
            count = len(emails)
        for i in range(count):
            accounts.append((emails[i], gen_password(), get_random_name()))
    elif method == "phone":
        nums = load_file(CONFIG["number_file"])
        if not nums:
            print(C.R + "\n[!] No numbers in " + CONFIG["number_file"] + C.N)
            return
        if count > len(nums):
            count = len(nums)
        for i in range(count):
            accounts.append((nums[i], gen_password(), get_random_name()))
    elif method == "automail":
        for i in range(count):
            accounts.append((gen_temp_email(), gen_password(), get_random_name()))
    
    if not accounts:
        print(C.R + "\n[!] No accounts to create!" + C.N)
        return
    
    CONFIG["running"] = True
    CONFIG["created"] = 0
    CONFIG["success"] = 0
    CONFIG["failed"] = 0
    
    # Banner
    box("  " + C.BD + C.G + "STARTING CREATION" + C.N + "  \n" +
        "  Method : " + C.G + method.upper() + C.N + "  \n" +
        "  Count  : " + C.G + str(count) + C.N + "  \n" +
        "  Threads: " + C.G + str(CONFIG["threads"]) + C.N + "  \n" +
        "  Proxy  : " + C.G + ("ON (" + str(len(proxies)) + " loaded)" if CONFIG["use_proxy"] and proxies else "OFF") + C.N + "  \n" +
        "  Output : " + C.Y + ACCOUNTS_DIR + "/" + method + "_accounts.txt" + C.N,
        C.CY, 56)
    
    print()
    line("─", 60, C.D)
    print()
    
    lock = threading.Lock()
    q = Queue()
    
    # Producer
    def producer():
        for i, item in enumerate(accounts):
            if not CONFIG["running"]:
                break
            q.put((i+1, item[0], item[1], item[2]))
            time.sleep(0.05)
        # Wait for completion
        q.join()
        CONFIG["running"] = False
    
    # Start workers
    for i in range(CONFIG["threads"]):
        t = threading.Thread(target=worker, args=(q, proxies, lock), daemon=True)
        t.start()
    
    prod_t = threading.Thread(target=producer, daemon=True)
    prod_t.start()
    
    # Wait
    try:
        while CONFIG["running"] and CONFIG["created"] < len(accounts):
            time.sleep(1)
    except KeyboardInterrupt:
        CONFIG["running"] = False
    
    print()
    line("─", 60, C.G)
    print()
    box("  " + C.BD + C.G + "✅ COMPLETED!" + C.N + "  \n" +
        "  Total  : " + C.Y + str(CONFIG["created"]) + C.N + "  \n" +
        "  " + C.G + "Success: " + str(CONFIG["success"]) + C.N + "  \n" +
        "  " + C.R + "Failed : " + str(CONFIG["failed"]) + C.N + "  \n" +
        "  Saved  : " + C.Y + ACCOUNTS_DIR + "/" + method + "_accounts.txt" + C.N,
        C.G, 56)
    print()
    
    CONFIG["running"] = False

# ═══════════════════════════════════════════════════════
# CONFIG DISPLAY
# ═══════════════════════════════════════════════════════
def show_config():
    print(C.CY + "┌─ Current Configuration ─" + "─" * 36 + "┐" + C.N)
    print("  Method    : " + C.G + CONFIG["method"].upper() + C.N)
    print("  Count     : " + C.G + str(CONFIG["count"]) + C.N)
    print("  Threads   : " + C.G + str(CONFIG["threads"]) + C.N)
    print("  Delay     : " + C.G + str(CONFIG["delay"]) + "s" + C.N)
    print("  Country   : " + C.G + CONFIG["country"] + C.N)
    print("  Gender    : " + C.G + CONFIG["gender"] + C.N)
    print("  Birthday  : " + C.G + str(CONFIG["birth_day"]) + "/" + str(CONFIG["birth_month"]) + "/" + str(CONFIG["birth_year"]) + C.N)
    pwd_disp = CONFIG["password"] if CONFIG["password"] else "(auto-generated)"
    print("  Password  : " + C.G + pwd_disp + C.N)
    name_disp = CONFIG["custom_name"] if CONFIG["custom_name"] else "(auto by country)"
    print("  Name      : " + C.G + name_disp + C.N)
    print("  Proxy     : " + (C.G + "ON" if CONFIG["use_proxy"] else C.R + "OFF") + C.N)
    print(C.CY + "└" + "─" * 58 + "┘" + C.N)

# ═══════════════════════════════════════════════════════
# MENU
# ═══════════════════════════════════════════════════════
def main():
    load_config()
    
    # Create default files
    for f in ["emails.txt", "numbers.txt", "proxies.txt"]:
        if not os.path.exists(f):
            open(f, "a").close()
    
    while True:
        banner()
        show_config()
        print()
        print(C.Y + "┌─ Menu ─" + "─" * 51 + "┐" + C.N)
        print(C.Y + "│" + C.N + "  " + C.CY + "[1]" + C.N + " Method: " + C.G + "EMAIL" + C.N + " (use your email list)             " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "  " + C.CY + "[2]" + C.N + " Method: " + C.G + "PHONE" + C.N + " (use your number list)           " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "  " + C.CY + "[3]" + C.N + " Method: " + C.G + "AUTO MAIL" + C.N + " (1secmail temp mail)         " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "  " + C.CY + "[4]" + C.N + " Set account count                                        " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "  " + C.CY + "[5]" + C.N + " Set threads & delay                                      " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "  " + C.CY + "[6]" + C.N + " Set country                                              " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "  " + C.CY + "[7]" + C.N + " Set gender                                                " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "  " + C.CY + "[8]" + C.N + " Set password (or auto)                                   " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "  " + C.CY + "[9]" + C.N + " Set birthday                                              " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "  " + C.CY + "[10]" + C.N + " Set custom name (or auto)                                " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "  " + C.CY + "[11]" + C.N + " Toggle proxy ON/OFF                                      " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "  " + C.CY + "[12]" + C.N + " Add email/number to list                                 " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "  " + C.CY + "[13]" + C.N + " View saved accounts                                      " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "  " + C.CY + "[14]" + C.N + " Save/Load config                                         " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "                                                            " + C.Y + "│" + C.N)
        print(C.Y + "│" + C.N + "  " + C.G + C.BD + "[S]" + C.N + " ▶ START CREATING    " + C.R + C.BD + "[X]" + C.N + " ■ STOP    " + C.W + C.BD + "[0]" + C.N + " EXIT     " + C.Y + "│" + C.N)
        print(C.Y + "└" + "─" * 58 + "┘" + C.N)
        
        try:
            ch = input(C.G + C.BD + "\n  ➤ Choose: " + C.N).strip().lower()
        except KeyboardInterrupt:
            ch = "0"
        
        if ch == "1":
            CONFIG["method"] = "email"
            save_config()
            print(C.G + "  ✓ Method set to EMAIL" + C.N)
        elif ch == "2":
            CONFIG["method"] = "phone"
            save_config()
            print(C.G + "  ✓ Method set to PHONE" + C.N)
        elif ch == "3":
            CONFIG["method"] = "automail"
            save_config()
            print(C.G + "  ✓ Method set to AUTO MAIL" + C.N)
        elif ch == "4":
            try:
                c = input(C.G + "  How many accounts? : " + C.N).strip()
                if c:
                    CONFIG["count"] = max(1, int(c))
                    save_config()
                    print(C.G + "  ✓ Count: " + str(CONFIG["count"]) + C.N)
            except:
                print(C.R + "  Invalid number" + C.N)
        elif ch == "5":
            try:
                t = input(C.G + "  Threads (1-15) [" + str(CONFIG["threads"]) + "]: " + C.N).strip()
                if t:
                    CONFIG["threads"] = max(1, min(15, int(t)))
                d = input(C.G + "  Delay seconds [" + str(CONFIG["delay"]) + "]: " + C.N).strip()
                if d:
                    CONFIG["delay"] = max(0.0, float(d))
                save_config()
                print(C.G + "  ✓ Threads: " + str(CONFIG["threads"]) + " | Delay: " + str(CONFIG["delay"]) + "s" + C.N)
            except:
                print(C.R + "  Invalid input" + C.N)
        elif ch == "6":
            print(C.CY + "\n  Countries:" + C.N)
            for k, v in sorted(COUNTRIES.items()):
                print("    " + k + ". " + v)
            sel = input(C.G + "  Choose: " + C.N).strip()
            if sel in COUNTRIES:
                CONFIG["country"] = COUNTRIES[sel]
                save_config()
                print(C.G + "  ✓ Country: " + CONFIG["country"] + C.N)
        elif ch == "7":
            g = input(C.G + "  Gender (male/female): " + C.N).strip().lower()
            if g in ("male", "female", "m", "f"):
                CONFIG["gender"] = "male" if g.startswith("m") else "female"
                save_config()
                print(C.G + "  ✓ Gender: " + CONFIG["gender"] + C.N)
        elif ch == "8":
            p = input(C.G + "  Password (or 'auto'): " + C.N).strip()
            CONFIG["password"] = "" if p.lower() == "auto" else p
            save_config()
            print(C.G + "  ✓ Password " + ("set" if CONFIG["password"] else "= auto") + C.N)
        elif ch == "9":
            try:
                d = input(C.G + "  Day [1-31, " + str(CONFIG["birth_day"]) + "]: " + C.N).strip()
                if d:
                    CONFIG["birth_day"] = max(1, min(31, int(d)))
                m = input(C.G + "  Month [1-12, " + str(CONFIG["birth_month"]) + "]: " + C.N).strip()
                if m:
                    CONFIG["birth_month"] = max(1, min(12, int(m)))
                y = input(C.G + "  Year [1950-2005, " + str(CONFIG["birth_year"]) + "]: " + C.N).strip()
                if y:
                    CONFIG["birth_year"] = max(1950, min(2005, int(y)))
                save_config()
                print(C.G + "  ✓ Birthday: " + str(CONFIG["birth_day"]) + "/" + str(CONFIG["birth_month"]) + "/" + str(CONFIG["birth_year"]) + C.N)
            except:
                print(C.R + "  Invalid" + C.N)
        elif ch == "10":
            n = input(C.G + "  Custom name (or 'auto'): " + C.N).strip()
            CONFIG["custom_name"] = "" if n.lower() == "auto" else n
            save_config()
            print(C.G + "  ✓ Name: " + (CONFIG["custom_name"] if CONFIG["custom_name"] else "auto") + C.N)
        elif ch == "11":
            CONFIG["use_proxy"] = not CONFIG["use_proxy"]
            save_config()
            status = "ON" if CONFIG["use_proxy"] else "OFF"
            color = C.G if CONFIG["use_proxy"] else C.R
            print(color + "  ✓ Proxy: " + status + C.N)
        elif ch == "12":
            val = input(C.G + "  Email or Phone: " + C.N).strip()
            if val:
                if val.replace("+", "").replace("-", "").isdigit():
                    f = CONFIG["number_file"]
                else:
                    f = CONFIG["email_file"]
                with open(f, "a") as fh:
                    fh.write(val + "\n")
                print(C.G + "  ✓ Added to " + f + C.N)
        elif ch == "13":
            print(C.CY + "\n  ── Saved Account Files ──" + C.N)
            files = [f for f in os.listdir(ACCOUNTS_DIR) if f.endswith(".txt")]
            if not files:
                print(C.Y + "  No accounts saved yet." + C.N)
            else:
                for fn in files:
                    fp = os.path.join(ACCOUNTS_DIR, fn)
                    with open(fp, "r") as fh:
                        content = fh.read()
                    count = content.count("=" * 60)
                    size = os.path.getsize(fp)
                    print(C.G + "  • " + fn + C.N + " — " + str(count) + " accounts | " + str(size) + " bytes")
            print()
        elif ch == "14":
            sd = input(C.G + "  Save or Load? (s/l): " + C.N).strip().lower()
            if sd == "s":
                save_config()
                print(C.G + "  ✓ Config saved" + C.N)
            elif sd == "l":
                load_config()
                print(C.G + "  ✓ Config loaded" + C.N)
        elif ch == "s":
            start_creator()
        elif ch == "x":
            CONFIG["running"] = False
            print(C.R + "  ■ Stop signal sent" + C.N)
            time.sleep(1)
        elif ch == "0":
            CONFIG["running"] = False
            print(C.Y + "\n  Goodbye! 👋" + C.N)
            time.sleep(0.5)
            break
        else:
            print(C.R + "  Invalid option" + C.N)
        
        if ch not in ("s", "x", "0"):
            try:
                input(C.D + "\n  Press Enter to
