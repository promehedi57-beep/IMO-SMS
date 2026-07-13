#!/data/data/com.termux/files/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║                                                                        ║
║     ███████╗███████╗ █████╗  ██████╗███████╗██████╗  ██████╗            ║
║     ██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗          ║
║     █████╗  █████╗  ███████║██║     █████╗  ██████╔╝██║   ██║          ║
║     ██╔══╝  ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗██║   ██║          ║
║     ██║     ███████╗██║  ██║╚██████╗███████╗██║  ██║╚██████╔╝          ║
║     ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝           ║
║                                                                        ║
║     █████╗ ██╗   ██╗████████╗ ██████╗                                 ║
║    ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗                                ║
║    ███████║██║   ██║   ██║   ██║   ██║                                ║
║    ██╔══██║██║   ██║   ██║   ██║   ██║                                ║
║    ██║  ██║╚██████╔╝   ██║   ╚██████╔╝                                ║
║    ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝                                 ║
║                                                                        ║
║      ██████╗██████╗ ███████╗ █████╗ ████████╗ ██████╗ ██████╗          ║
║     ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗        ║
║     ██║     ██████╔╝█████╗  ███████║   ██║   ██║   ██║██████╔╝        ║
║     ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██║   ██║██╔══██╗        ║
║     ╚██████╗██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║        ║
║      ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝        ║
║                                                                        ║
║            FACEBOOK AUTO ACCOUNT CREATOR v1.0                          ║
║         Email | Phone | Auto-Mail | Proxy | Multi-Thread               ║
║                 Educational Purpose Only                               ║
║                                                                        ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import random
import string
import threading
import re
from datetime import datetime
from queue import Queue

# ─── Termux Native Colors ───
class C:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    WHITE = '\033[0;37m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'

# ─── Import requests ───
try:
    import requests
    import urllib3
    urllib3.disable_warnings()
except ImportError:
    print(f"{C.RED}[!] Install: pip install requests{C.RESET}")
    sys.exit(1)

# ─── Config ───
CONFIG_FILE = "config.json"
ACCOUNTS_DIR = "accounts"
os.makedirs(ACCOUNTS_DIR, exist_ok=True)

DEFAULT_CONFIG = {
    "method": "email",           # email / phone / automail
    "account_count": 5,
    "threads": 3,
    "delay": 2.0,
    "country": "Bangladesh",
    "country_code": "BD",
    "password": "Fb@2025#pass",
    "birth_day": 15,
    "birth_month": 6,
    "birth_year": 1998,
    "gender": "male",            # male / female
    "custom_name": "",
    "use_proxy": False,
    "proxy_file": "proxies.txt",
    "email_file": "emails.txt",
    "number_file": "numbers.txt",
    "name_file": "names.txt",
    "ua_file": "user_agents.txt",
    "created_count": 0,
    "running": False,
}

# ─── User Agents ───
UA_LIST = [
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 13; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.90 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/134.0.6998.89 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; 2211133C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.85 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.113 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; OnePlus 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/127.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 15; Pixel 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; HUAWEI P60 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.84 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
]

# ─── Name Lists by Country ───
NAMES_BY_COUNTRY = {
    "Bangladesh": {
        "male": ["Md Rakib", "Shahidul Islam", "Abdur Rahman", "Minhaz Hossain", "Tanvir Ahmed",
                 "Fahim Hasan", "Nazmul Islam", "Rabiul Hasan", "Jahid Hasan", "Sohel Rana",
                 "Kawsar Ahmed", "Milon Hossain", "Ripon Miah", "Shakil Khan", "Habib Rahman",
                 "Sabbir Hossain", "Riaz Uddin", "Faruk Ahmed", "Shahin Alam", "Manik Miah"],
        "female": ["Fatima Begum", "Ayesha Khatun", "Nasrin Akter", "Shahnaz Parvin", "Rina Begum",
                   "Jamila Khatun", "Hosneara Begum", "Shamima Akter", "Rokeya Begum", "Saleha Khatun",
                   "Jahanara Begum", "Shahida Begum", "Ambia Khatun", "Rashida Akter", "Asia Khatun"]
    },
    "India": {
        "male": ["Rajesh Kumar", "Amit Sharma", "Vikram Singh", "Suresh Patel", "Deepak Verma",
                 "Rahul Gupta", "Anil Joshi", "Sanjay Mishra", "Prakash Rao", "Manoj Tiwari"],
        "female": ["Priya Sharma", "Suman Devi", "Neha Gupta", "Pooja Singh", "Anita Verma",
                   "Ritu Patel", "Kavita Joshi", "Sunita Rao", "Rekha Devi", "Geeta Kumari"]
    },
    "Pakistan": {
        "male": ["Muhammad Ali", "Ahmed Khan", "Hassan Raza", "Bilal Ahmed", "Usman Malik",
                 "Farhan Iqbal", "Kamran Khan", "Naveed Akhtar", "Tariq Mehmood", "Shoaib Akram"],
        "female": ["Sana Khan", "Ayesha Malik", "Fatima Ali", "Zainab Ahmed", "Hira Butt",
                   "Nadia Hussain", "Sadia Khan", "Rabia Bashir", "Tahira Iqbal", "Shazia Parveen"]
    },
    "USA": {
        "male": ["James Smith", "John Johnson", "Robert Williams", "Michael Brown", "David Jones",
                 "Daniel Miller", "Christopher Davis", "Matthew Wilson", "Andrew Taylor", "Ryan Anderson"],
        "female": ["Mary Smith", "Jennifer Johnson", "Linda Williams", "Patricia Brown", "Elizabeth Jones",
                   "Susan Miller", "Jessica Davis", "Sarah Wilson", "Karen Taylor", "Nancy Anderson"]
    },
    "UK": {
        "male": ["Oliver Smith", "George Johnson", "Harry Williams", "Jack Brown", "Charlie Wilson",
                 "Thomas Taylor", "James Davies", "William Evans", "Henry Thomas", "Edward Roberts"],
        "female": ["Olivia Smith", "Emily Johnson", "Sophie Williams", "Amelia Brown", "Isabella Wilson",
                   "Charlotte Taylor", "Mia Davies", "Lily Evans", "Ella Thomas", "Grace Roberts"]
    },
    "UAE": {
        "male": ["Mohammed Al-Rashid", "Ahmed Al-Maktoum", "Ali Al-Nahyan", "Omar Al-Sayed", "Khalid Hassan",
                 "Saeed Al-Mansoori", "Hamdan Al-Ali", "Rashid Al-Qasimi", "Sultan Al-Muhairi", "Majid Al-Falasi"],
        "female": ["Mariam Al-Mansoori", "Fatima Al-Suwaidi", "Aisha Al-Nuaimi", "Noora Al-Kaabi", "Sara Al-Hashimi",
                   "Amna Al-Mazrouei", "Layla Al-Qubaisi", "Hind Al-Mehairi", "Mona Al-Blooshi", "Shamma Al-Shamsi"]
    },
    "Saudi Arabia": {
        "male": ["Khalid Al-Saud", "Fahad Al-Otaibi", "Majid Al-Ghamdi", "Sultan Al-Harbi", "Nasser Al-Dosari",
                 "Abdullah Al-Zahrani", "Ibrahim Al-Shammari", "Saleh Al-Anazi", "Bandar Al-Mutairi", "Turki Al-Qahtani"],
        "female": ["Noura Al-Saud", "Sara Al-Otaibi", "Rania Al-Ghamdi", "Lama Al-Harbi", "Dana Al-Dosari",
                   "Razan Al-Zahrani", "Maha Al-Shammari", "Areej Al-Anazi", "Huda Al-Mutairi", "Afnan Al-Qahtani"]
    }
}

# ─── Auto Mail Domains (for auto-mail method) ───
AUTO_MAIL_DOMAINS = [
    "@mail.com", "@email.com", "@inbox.com", "@gmx.com",
    "@yopmail.com", "@tempmail.com", "@10minutemail.com",
    "@guerrillamail.com", "@mailnator.com", "@trashmail.com"
]

# ─── Common Passwords ───
DEFAULT_PASSWORDS = [
    "Fb@2025#pass", "Facebook@123", "Pass@2025#", "User@12345",
    "Admin@2025", "Hello@123", "Secure#2025", "MyPass@123",
    "Alpha@2025", "Beta#1234", "Gamma@5432", "Delta#6789"
]


# ██████████████████████████████████████████████████████████████████████████████
# CORE FUNCTIONS
# ██████████████████████████████████████████████████████████████████████████████

def load_config():
    """Load configuration"""
    cfg = dict(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                cfg.update(json.load(f))
        except: pass
    return cfg

def save_config(cfg):
    """Save configuration"""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=2)
    except: pass

def load_file(path):
    """Load text file"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip()]
    except:
        return []

def generate_email(index=0):
    """Generate auto email"""
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(8, 14)))
    domain = random.choice(AUTO_MAIL_DOMAINS)
    return f"{username}{domain}"

def generate_password():
    """Generate or return custom password"""
    base = random.choice(DEFAULT_PASSWORDS)
    suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
    return f"{base}{suffix}"

def get_random_name(cfg):
    """Get random name based on country and gender"""
    country = cfg.get("country", "Bangladesh")
    gender = cfg.get("gender", "male")
    
    if cfg.get("custom_name"):
        return cfg["custom_name"]
    
    country_data = NAMES_BY_COUNTRY.get(country, NAMES_BY_COUNTRY["Bangladesh"])
    names = country_data.get(gender, country_data.get("male", ["User"]))
    return random.choice(names)

def get_random_ua(custom_list=None):
    """Get random user agent"""
    all_ua = (custom_list or []) + UA_LIST
    return random.choice(all_ua)

def get_proxy(proxies, idx=[0]):
    """Get proxy (sequential)"""
    if not proxies: return None
    with threading.Lock():
        p = proxies[idx[0] % len(proxies)]
        idx[0] += 1
    if p.startswith("socks5"):
        return {"http": p.replace("socks5", "socks5h"), "https": p.replace("socks5", "socks5h")}
    return {"http": p, "https": p}

def generate_facebook_payload(email_or_phone, password, name, cfg):
    """Generate Facebook signup payload"""
    first_name = name.split()[0] if name.split() else name
    last_name = " ".join(name.split()[1:]) if len(name.split()) > 1 else "User"
    
    # Determine if email or phone
    if '@' in str(email_or_phone):
        identifier = {"email": email_or_phone}
    else:
        identifier = {"phone": email_or_phone}
    
    payload = {
        **identifier,
        "firstname": first_name,
        "lastname": last_name,
        "password": password,
        "birthday": {
            "day": cfg["birth_day"],
            "month": cfg["birth_month"],
            "year": cfg["birth_year"]
        },
        "gender": 1 if cfg["gender"] == "female" else 2,
        "locale": "en_US",
        "reg_instance": f"reg_instance_{int(time.time())}",
        "referrer": "https://www.facebook.com/",
        "reg_impression_id": f"reg_impression_{random.randint(100000, 999999)}",
        "source": "REGISTRATION_EMAIL",
        "skip_reauth": True,
        "machine_id": ''.join(random.choices(string.hexdigits, k=16)).lower(),
        "meta_referrer": "https://www.facebook.com/",
        "fb_dtsg": "",
        "__ccg": "EXCELLENT",
        "__dyn": "",
        "__req": str(random.randint(1, 50)),
        "__be": "0",
        "__pc": "PHASED:DEFAULT",
        "__rev": str(random.randint(1000000, 9999999)),
        "__spin_r": str(random.randint(1000000, 9999999)),
        "__spin_b": "trunk",
        "__spin_t": str(int(time.time())),
    }
    return payload

def create_facebook_account(email_or_phone, password, name, cfg, proxies, uas, session):
    """Send Facebook signup request"""
    try:
        url = "https://www.facebook.com/api/graphql/"
        
        # First, get fb_dtsg token from homepage
        try:
            home_r = session.get("https://www.facebook.com/", 
                                 proxies=get_proxy(proxies) if cfg["use_proxy"] else None,
                                 timeout=8, verify=False)
            fb_dtsg = ""
            match = re.search(r'name="fb_dtsg"[^>]+value="([^"]+)"', home_r.text)
            if match:
                fb_dtsg = match.group(1)
        except:
            fb_dtsg = ""
        
        payload = generate_facebook_payload(email_or_phone, password, name, cfg)
        payload["fb_dtsg"] = fb_dtsg
        
        headers = {
            "User-Agent": get_random_ua(uas),
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "Origin": "https://www.facebook.com",
            "Referer": "https://www.facebook.com/r.php",
            "X-FB-Connection-Quality": "EXCELLENT",
            "X-FB-Friendly-Name": "Registration",
            "X-FB-LSD": ''.join(random.choices(string.ascii_letters + string.digits, k=21)),
            "X-FB-Request-Analytics-Tags": "registration",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
        }
        
        proxy = get_proxy(proxies) if cfg["use_proxy"] else None
        
        r = session.post(url, json=payload, headers=headers, proxies=proxy, timeout=cfg.get("timeout", 10), verify=False)
        
        # Parse response
        account_id = ""
        if "uid" in r.text:
            try:
                data = r.json()
                account_id = str(data.get("uid", ""))
            except:
                pass
        
        # Check if created
        success = r.status_code == 200 and ("uid" in r.text or "account_created" in r.text)
        
        return {
            "ok": success,
            "code": r.status_code,
            "email_or_phone": email_or_phone,
            "password": password,
            "name": name,
            "account_id": account_id,
            "response": r.text[:200],
        }
        
    except Exception as e:
        return {
            "ok": False,
            "error": str(e)[:60],
            "email_or_phone": email_or_phone,
            "password": password,
            "name": name,
            "account_id": "",
        }


# ██████████████████████████████████████████████████████████████████████████████
# WORKER THREAD
# ██████████████████████████████████████████████████████████████████████████████

def worker(q, cfg, proxies, uas, lock, method_stats):
    """Worker thread to create accounts"""
    session = requests.Session()
    session.verify = False
    
    while cfg["running"]:
        try:
            job = q.get(timeout=1)
            if job is None: break
            
            idx, email_or_phone, password, name = job
            
            result = create_facebook_account(email_or_phone, password, name, cfg, proxies, uas, session)
            
            with lock:
                cfg["created_count"] += 1
                method_stats["total"] += 1
                
                if result.get("ok"):
                    method_stats["success"] += 1
                    status = f"{C.GREEN}✓ CREATED{c.RESET}"
                    
                    # Save to file
                    method_name = cfg["method"]
                    file_path = f"{ACCOUNTS_DIR}/method_{method_name}.txt"
                    with open(file_path, "a") as f:
                        f.write(f"{'='*50}\n")
                        f.write(f"Account #{method_stats['success']}\n")
                        f.write(f"Name         : {result['name']}\n")
                        f.write(f"Email/Phone  : {result['email_or_phone']}\n")
                        f.write(f"Password     : {result['password']}\n")
                        f.write(f"Account ID   : {result.get('account_id', 'N/A')}\n")
                        f.write(f"Country      : {cfg['country']}\n")
                        f.write(f"Gender       : {cfg['gender']}\n")
                        f.write(f"Birthday     : {cfg['birth_day']}/{cfg['birth_month']}/{cfg['birth_year']}\n")
                        f.write(f"Method       : {method_name}\n")
                        f.write(f"Created At   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"{'='*50}\n\n")
                    
                    print(f"\n{C.GREEN}  ✓ [{method_stats['total']:03d}] Created: {result['name'][:15]:15s} | {result['email_or_phone'][:20]:20s} | Pass: {result['password'][:12]}{C.RESET}")
                else:
                    method_stats["fail"] += 1
                    err = result.get("error", f"HTTP {result.get('code','?')}")
                    print(f"\n{C.RED}  ✗ [{method_stats['total']:03d}] Failed : {email_or_phone[:20]:20s} | {err}{C.RESET}")
                
                time.sleep(cfg["delay"])
            
            q.task_done()
        except: continue


# ██████████████████████████████████████████████████████████████████████████████
# ACCOUNT CREATOR LAUNCHER
# ██████████████████████████████████████████████████████████████████████████████

def start_creation(cfg):
    """Start account creation based on method"""
    if cfg["running"]:
        print(f"{C.RED}[!] Already running!{C.RESET}")
        return
    
    # Load data
    proxies = load_file(cfg["proxy_file"]) if cfg["use_proxy"] else []
    uas = load_file(cfg["ua_file"])
    
    method = cfg["method"]
    count = cfg["account_count"]
    
    # Prepare accounts list
    accounts = []  # (email_or_phone, password, name)
    
    if method == "email":
        # Use emails from file
        emails = load_file(cfg["email_file"])
        if not emails:
            print(f"{C.RED}[!] No emails in {cfg['email_file']}!{C.RESET}")
            return
        if count > len(emails):
            print(f"{C.YELLOW}[!] You asked {count} but only {len(emails)} emails. Creating {len(emails)}.{C.RESET}")
            count = len(emails)
        for i in range(count):
            email = emails[i]
            password = cfg["password"] if cfg["password"] else generate_password()
            name = get_random_name(cfg)
            accounts.append((email, password, name))
    
    elif method == "phone":
        # Use phone numbers from file
        numbers = load_file(cfg["number_file"])
        if not numbers:
            print(f"{C.RED}[!] No numbers in {cfg['number_file']}!{C.RESET}")
            return
        if count > len(numbers):
            print(f"{C.YELLOW}[!] You asked {count} but only {len(numbers)} numbers. Creating {len(numbers)}.{C.RESET}")
            count = len(numbers)
        for i in range(count):
            number = numbers[i]
            password = cfg["password"] if cfg["password"] else generate_password()
            name = get_random_name(cfg)
            accounts.append((number, password, name))
    
    elif method == "automail":
        # Auto generate emails
        for i in range(count):
            email = generate_email(i)
            password = cfg["password"] if cfg["password"] else generate_password()
            name = get_random_name(cfg)
            accounts.append((email, password, name))
    
    else:
        print(f"{C.RED}[!] Invalid method: {method}{C.RESET}")
        return
    
    # Start threads
    cfg["running"] = True
    cfg["created_count"] = 0
    method_stats = {"total": 0, "success": 0, "fail": 0}
    lock = threading.Lock()
    
    job_queue = Queue()
    
    def producer():
        for idx, (ep, pw, nm) in enumerate(accounts):
            if not cfg["running"]: break
            try:
                job_queue.put((idx+1, ep, pw, nm), timeout=1)
            except: pass
            time.sleep(0.1)
    
    print(f"\n{C.CYAN}  ╔══════════════════════════════════════════════╗{C.RESET}")
    print(f"{C.CYAN}  ║  {C.GREEN}🚀 CREATING {count} ACCOUNTS{C.CYAN}                    ║{C.RESET}")
    print(f"{C.CYAN}  ╠══════════════════════════════════════════════╣{C.RESET}")
    print(f"{C.CYAN}  ║  Method : {C.YELLOW}{method.upper():<20}{C.CYAN}           ║{C.RESET}")
    print(f"{C.CYAN}  ║  Country: {C.YELLOW}{cfg['country']:<20}{C.CYAN}           ║{C.RESET}")
    print(f"{C.CYAN}  ║  Threads: {C.YELLOW}{cfg['threads']:<20}{C.CYAN}           ║{C.RESET}")
    print(f"{C.CYAN}  ║  Proxy  : {C.YELLOW}{'ON' if cfg['use_proxy'] else 'OFF':<20}{C.CYAN}           ║{C.RESET}")
    print(f"{C.CYAN}  ║  Press {C.RED}[X]{C.CYAN} in menu to STOP                     ║{C.RESET}")
    print(f"{C.CYAN}  ╚══════════════════════════════════════════════╝{C.RESET}\n")
    
    threads = []
    for _ in range(cfg["threads"]):
        t = threading.Thread(target=worker, args=(job_queue, cfg, proxies, uas, lock, method_stats), daemon=True)
        t.start()
        threads.append(t)
    
    prod = threading.Thread(target=producer, daemon=True)
    prod.start()
    
    try:
        while cfg["running"] and method_stats["total"] < count:
            time.sleep(1)
            total = method_stats["total"]
            ok = method_stats["success"]
            fail = method_stats["fail"]
            print(f"\r{C.CYAN}  Progress: {total}/{count} | {C.GREEN}✓ {ok}{C.RESET} {C.RED}✗ {fail}{C.RESET} | {C.YELLOW}{'█'*ok}{'░'*(total-ok) if total-ok > 0 else ''}{C.RESET}", end="")
    except: pass
    
    # Save summary
    with open(f"{ACCOUNTS_DIR}/summary_{method}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w") as f:
        f.write(f"Facebook Account Creator - Summary\n")
        f.write(f"{'='*50}\n")
        f.write(f"Method      : {method}\n")
        f.write(f"Total       : {count}\n")
        f.write(f"Created     : {method_stats['success']}\n")
        f.write(f"Failed      : {method_stats['fail']}\n")
        f.write(f"Country     : {cfg['country']}\n")
        f.write(f"Gender      : {cfg['gender']}\n")
        f.write(f"Password    : {cfg['password'] if cfg['password'] else 'Auto'}\n")
        f.write(f"Proxy       : {'Yes' if cfg['use_proxy'] else 'No'}\n")
        f.write(f"Completed At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Accounts saved in: {ACCOUNTS_DIR}/method_{method}.txt\n")
    
    print(f"\n\n{C.GREEN}{C.BOLD}  ✅ COMPLETED!{C.RESET}")
    print(f"{C.CYAN}  Created  : {C.GREEN}{method_stats['success']}{C.RESET}")
    print(f"{C.CYAN}  Failed   : {C.RED}{method_stats['fail']}{C.RESET}")
    print(f"{C.CYAN}  Details  : {C.YELLOW}{ACCOUNTS_DIR}/method_{method}.txt{C.RESET}")
    print()


# ██████████████████████████████████████████████████████████████████████████████
# UI FUNCTIONS
# ██████████████████████████████████████████████████████████████████████████████

def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{C.RED}
  ███████╗███████╗      █████╗ ██╗   ██╗████████╗ ██████╗ 
  ██╔════╝██╔════╝     ██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗
  █████╗  █████╗       ███████║██║   ██║   ██║   ██║   ██║
  ██╔══╝  ██╔══╝       ██╔══██║██║   ██║   ██║   ██║   ██║
  ██║     ███████╗     ██║  ██║╚██████╔╝   ██║   ╚██████╔╝
  ╚═╝     ╚══════╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝ 
{C.MAGENTA}
  ██████╗██████╗ ███████╗ █████╗ ████████╗ ██████╗ ██████╗ 
 ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗
 ██║     ██████╔╝█████╗  ███████║   ██║   ██║   ██║██████╔╝
 ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██║   ██║██╔══██╗
 ╚██████╗██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║
  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝
{C.CYAN}  ════════════════════════════════════════════════════════
    FACEBOOK AUTO ACCOUNT CREATOR v1.0 — TERMUX EDITION
    Email | Phone | Auto-Mail | Proxy | Multi-Thread
  ════════════════════════════════════════════════════════{C.RESET}
    """)

def show_status(cfg):
    """Show current configuration"""
    print(f"{C.CYAN}  ╔═══════════ CONFIGURATION ═══════════════════════╗{C.RESET}")
    print(f"{C.CYAN}  ║  {C.WHITE}Method     : {C.GREEN}{cfg['method'].upper():<20}{C.CYAN}              ║{C.RESET}")
    print(f"{C.CYAN}  ║  {C.WHITE}Count      : {C.GREEN}{cfg['account_count']:<20}{C.CYAN}              ║{C.RESET}")
    print(f"{C.CYAN}  ║  {C.WHITE}Threads    : {C.GREEN}{cfg['threads']:<20}{C.CYAN}              ║{C.RESET}")
    print(f"{C.CYAN}  ║  {C.WHITE}Delay      : {C.GREEN}{cfg['delay']}< 秒{C.CYAN}                    ║{C.RESET}")
    print(f"{C.CYAN}  ║  {C.WHITE}Country    : {C.GREEN}{cfg['country']:<20}{C.CYAN}             ║{C.RESET}")
    print(f"{C.CYAN}  ║  {C.WHITE}Gender     : {C.GREEN}{cfg['gender']:<20}{C.CYAN}              ║{C.RESET}")
    print(f"{C.CYAN}  ║  {C.WHITE}Password   : {C.GREEN}{cfg['password'] if cfg['password'] else 'AUTO':<20}{C.CYAN}║{C.RESET}")
    print(f"{C.CYAN}  ║  {C.WHITE}Birthday   : {C.GREEN}{cfg['birth_day']}/{cfg['birth_month']}/{cfg['birth_year']:<12}{C.CYAN}      ║{C.RESET}")
    print(f"{C.CYAN}  ║  {C.WHITE}Custom Name: {C.GREEN}{cfg['custom_name'] if cfg['custom_name'] else 'Auto by country':<20}{C.CYAN}║{C.RESET}")
    print(f"{C.CYAN}  ║  {C.WHITE}Proxy      : {C.GREEN}{'ON' if cfg['use_proxy'] else 'OFF':<20}{C.CYAN}              ║{C.RESET}")
    if cfg["created_count"] > 0:
        print(f"{C.CYAN}  ║  {C.WHITE}Created    : {C.GREEN}{cfg['created_count']:<20}{C.CYAN}              ║{C.RESET}")
    print(f"{C.CYAN}  ╚════════════════════════════════════════════════╝{C.RESET}")

def show_menu():
    """Display menu"""
    print(f"""{C.YELLOW}  ╔═══════════════ MAIN MENU ═══════════════╗
  ║                                      ║
  ║  {C.CYAN}[1] {C.WHITE}Method: Email (manual){C.YELLOW}               ║
  ║  {C.CYAN}[2] {C.WHITE}Method: Phone (manual){C.YELLOW}               ║
  ║  {C.CYAN}[3] {C.WHITE}Method: Auto-Mail (generated){C.YELLOW}        ║
  ║  {C.CYAN}[4] {C.WHITE}Set Account Count{C.YELLOW}                    ║
  ║  {C.CYAN}[5] {C.WHITE}Set Threads & Delay{C.YELLOW}                  ║
  ║  {C.CYAN}[6] {C.WHITE}Set Country{C.YELLOW}                          ║
  ║  {C.CYAN}[7] {C.WHITE}Set Gender (Male/Female){C.YELLOW}             ║
  ║  {C.CYAN}[8] {C.WHITE}Set Password{C.YELLOW}                         ║
  ║  {C.CYAN}[9] {C.WHITE}Set Birthday (Day/Month/Year){C.YELLOW}        ║
  ║  {C.CYAN}[10]{C.WHITE}Set Custom Name (optional){C.YELLOW}           ║
  ║  {C.CYAN}[11]{C.WHITE}Toggle Proxy{C.YELLOW}                         ║
  ║  {C.CYAN}[12]{C.WHITE}Add Email to List{C.YELLOW}                    ║
  ║  {C.CYAN}[13]{C.WHITE}Add Number to List{C.YELLOW}                   ║
  ║  {C.CYAN}[14]{C.WHITE}View Saved Accounts{C.YELLOW}                  ║
  ║  {C.CYAN}[15]{C.WHITE}Save/Load Config{C.YELLOW}                     ║
  ║                                      ║
  ║  {C.GREEN}[S]{C.WHITE} START CREATING ACCOUNTS{C.YELLOW}             ║
  ║  {C.RED}[X]{C.WHITE} STOP{C.YELLOW}                                   ║
  ║                                      ║
  ║  {C.WHITE}[0]{C.WHITE} Exit{C.YELLOW}                                 ║
  ╚══════════════════════════════════════╝
    """)


# ██████████████████████████████████████████████████████████████████████████████
# MENU HANDLERS
# ██████████████████████████████████████████████████████████████████████████████

def handle_set_method(cfg, method):
    cfg["method"] = method
    save_config(cfg)
    print(f"{C.GREEN}[✓] Method set to: {method.upper()}{C.RESET}")

def handle_set_count(cfg):
    try:
        c = int(input(f"{C.GREEN}How many accounts?: {C.RESET}"))
        cfg["account_count"] = max(1, c)
        save_config(cfg)
        print(f"{C.GREEN}[✓] Will create {cfg['account_count']} accounts{C.RESET}")
    except:
        print(f"{C.RED}[!] Invalid number{C.RESET}")

def handle_set_threads(cfg):
    try:
        t = int(input(f"{C.GREEN}Threads [{cfg['threads']}]: {C.RESET}"))
        cfg["threads"] = max(1, min(20, t))
        d = input(f"{C.GREEN}Delay [{cfg['delay']}]: {C.RESET}")
        if d: cfg["delay"] = max(0.5, float(d))
        save_config(cfg)
        print(f"{C.GREEN}[✓] Threads: {cfg['threads']}, Delay: {cfg['delay']}s{C.RESET}")
    except:
        print(f"{C.RED}[!] Invalid{C.RESET}")

def handle_set_country(cfg):
    countries = list(NAMES_BY_COUNTRY.keys())
    print(f"{C.CYAN}Available countries:{C.RESET}")
    for i, c in enumerate(countries, 1):
        print(f"  {i}. {c}")
    try:
        idx = int(input(f"{C.GREEN}Choose (1-{len(countries)}): {C.RESET}")) - 1
        if 0 <= idx < len(countries):
            cfg["country"] = countries[idx]
            save_config(cfg)
            print(f"{C.GREEN}[✓] Country: {cfg['country']}{C.RESET}")
    except:
        print(f"{C.RED}[!] Invalid{C.RESET}")

def handle_set_gender(cfg):
    g = input(f"{C.GREEN}Gender (male/female) [{cfg['gender']}]: {C.RESET}").strip().lower()
    if g in ("male", "female"):
        cfg["gender"] = g
        save_config(cfg)
        print(f"{C.GREEN}[✓] Gender: {cfg['gender']}{C.RESET}")

def handle_set_password(cfg):
    p = input(f"{C.GREEN}Password (or 'auto' for random): {C.RESET}").strip()
    if p.lower() == "auto":
        cfg["password"] = ""
        print(f"{C.YELLOW}[✓] Auto password on{C.RESET}")
    elif p:
        cfg["password"] = p
        print(f"{C.GREEN}[✓] Password set{C.RESET}")

def handle_set_birthday(cfg):
    try:
        d = int(input(f"{C.GREEN}Day (1-31) [{cfg['birth_day']}]: {C.RESET}") or cfg['birth_day'])
        m = int(input(f"{C.GREEN}Month (1-12) [{cfg['birth_month']}]: {C.RESET}") or cfg['birth_month'])
        y = int(input(f"{C.GREEN}Year [{cfg['birth_year']}]: {C.RESET}") or cfg['birth_year'])
        cfg["birth_day"] = max(1, min(31, d))
        cfg["birth_month"] = max(1, min(12, m))
        cfg["birth_year"] = max(1950, min(2005, y))
        save_config(cfg)
        print(f"{C.GREEN}[✓] Birthday: {cfg['birth_day']}/{cfg['birth_month']}/{cfg['birth_year']}{C.RESET}")
    except:
        print(f"{C.RED}[!] Invalid{C.RESET}")

def handle_set_name(cfg):
    n = input(f"{C.GREEN}Custom name (or 'auto'): {C.RESET}").strip()
    if n.lower() == "auto":
        cfg["custom_name"] = ""
        print(f"{C.YELLOW}[✓] Auto name on{C.RESET}")
    elif n:
        cfg["custom_name"] = n
        print(f"{C.GREEN}[✓] Name: {n}{C.RESET}")

def handle_toggle_proxy(cfg):
    cfg["use_proxy"] = not cfg["use_proxy"]
    save_config(cfg)
    print(f"{C.GREEN}[✓] Proxy: {'ON' if cfg['use_proxy'] else 'OFF'}{C.RESET}")

def handle_add_email(cfg):
    e = input(f"{C.GREEN}Enter email: {C.RESET}").strip()
    if e and '@' in e:
        with open(cfg["email_file"], "a") as f:
            f.write(e + "\n")
        print(f"{C.GREEN}[✓] Email added: {e}{C.RESET}")

def handle_add_number(cfg):
    n = input(f"{C.GREEN}Enter number: {C.RESET}").strip()
    if n:
        with open(cfg["number_file"], "a") as f:
            f.write(n + "\n")
        print(f"{C.GREEN}[✓] Number added: {n}{C.RESET}")

def handle_view_accounts(cfg):
    method = cfg["method"]
    file_path = f"{ACCOUNTS_DIR}/method_{method}.txt"
    if os.path.exists(file_path):
        with open(file_path) as f:
            content = f.read()
        lines = content.strip().split('\n')
        print(f"\n{C.CYAN}── Saved Accounts ({method}) ──{C.RESET}")
        for line in lines[-40:]:
            print(f"  {line}")
    else:
        # Show all files in accounts directory
        files = os.listdir(ACCOUNTS_DIR)
        if files:
            print(f"{C.CYAN}Files in accounts/: {', '.join(files)}{C.RESET}")
        else:
            print(f"{C.YELLOW}No accounts saved yet.{C.RESET}")


# ██████████████████████████████████████████████████████████████████████████████
# MAIN LOOP
# ██████████████████████████████████████████████████████████████████████████████

def main():
    cfg = load_config()
    
    # Ensure data files exist
    for f in [cfg["email_file"], cfg["number_file"], cfg["name_file"], cfg["proxy_file"], cfg["ua_file"]]:
        if not os.path.exists(f):
            open(f, "a").close()
    
    while True:
        show_banner()
        show_status(cfg)
        show_menu()
        
        ch = input(f"{C.GREEN}Choose: {C.RESET}").strip().lower()
        
        if ch == "1":
            handle_set_method(cfg, "email")
        elif ch == "2":
            handle_set_method(cfg, "phone")
        elif ch == "3":
            handle_set_method(cfg, "automail")
        elif ch == "4":
            handle_set_count(cfg)
        elif ch == "5":
            handle_set_threads(cfg)
        elif ch == "6":
            handle_set_country(cfg)
        elif ch == "7":
            handle_set_gender(cfg)
        elif ch == "8":
            handle_set_password(cfg)
        elif ch == "9":
            handle_set_birthday(cfg)
        elif ch == "10":
            handle_set_name(cfg)
        elif ch == "11":
            handle_toggle_proxy(cfg)
        elif ch == "12":
            handle_add_email(cfg)
        elif ch == "13":
            handle_add_number(cfg)
        elif ch == "14":
            handle_view_accounts(cfg)
        elif ch == "15":
            sc = input(f"{C.GREEN}1=Save  2=Load: {C.RESET}").strip()
            if sc == "1":
                save_config(cfg)
                print(f"{C.GREEN}[✓] Config saved{C.RESET}")
            elif sc == "2":
                cfg = load_config()
                print(f"{C.GREEN}[✓] Config loaded{C.RESET}")
        elif ch == "s":
            start_creation(cfg)
        elif ch == "x":
            cfg["running"] = False
            print(f"\n{C.RED}🛑 Stopped!{C.RESET}")
            time.sleep(1)
        elif ch == "0":
            cfg["running"] = False
            print(f"\n{C.YELLOW}Exiting...{C.RESET}")
            time.sleep(0.5)
            sys.exit(0)
        else:
            print(f"{C.RED}[!] Invalid option{C.RESET}")
        
        if ch not in ("s", "x"):
            input(f"\n{C.YELLOW}Press Enter...{C.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{C.RED}Exiting...{C.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C.RED}Error: {e}{C.RESET}")
        sys.exit(1)
