#!/data/data/com.termux/files/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, json, time, random, string, threading, re, hashlib
from datetime import datetime
from queue import Queue

# ─── Colors ───
class C:
    R = '\033[0;31m'; G = '\033[0;32m'; Y = '\033[1;33m'
    B = '\033[0;34m'; M = '\033[0;35m'; C = '\033[0;36m'
    W = '\033[0;37m'; D = '\033[2m'; N = '\033[0m'
    BOLD = '\033[1m'; BLINK = '\033[5m'

try:
    import requests
    import urllib3
    urllib3.disable_warnings()
except:
    print(f"{C.R}[!] pip install requests{C.N}")
    sys.exit(1)

# ─── Config ───
CONFIG = {
    "method": "automail", "count": 5, "threads": 5, "delay": 3.0, "timeout": 15,
    "country": "Bangladesh", "gender": "male", "password": "", "custom_name": "",
    "birth_day": 15, "birth_month": 6, "birth_year": 1998,
    "use_proxy": False, "proxy_file": "proxies.txt", "email_file": "emails.txt",
    "number_file": "numbers.txt", "temp_mail_file": "temp_mails.txt",
    "created": 0, "success": 0, "failed": 0, "running": False,
}
ACCOUNTS_DIR = "created_accounts"
os.makedirs(ACCOUNTS_DIR, exist_ok=True)

# ─── Names ───
NAMES_BY_COUNTRY = {
    "Bangladesh": {
        "male": ["MD Rakib Hasan", "Shahidul Islam", "Abdur Rahman", "Minhaz Hossain", "Tanvir Ahmed", "Fahim Hasan", "Nazmul Islam", "Rabiul Hasan", "Jahid Hasan", "Sohel Rana", "Kawsar Ahmed", "Milon Hossain", "Shakil Khan", "Habib Rahman", "Sabbir Hossain", "Riaz Uddin", "Faruk Ahmed", "Shahin Alam", "Al Amin", "Jahangir Alam"],
        "female": ["Fatima Begum", "Ayesha Khatun", "Nasrin Akter", "Shahnaz Parvin", "Rina Begum", "Jamila Khatun", "Hosneara Begum", "Shamima Akter", "Rokeya Begum", "Saleha Khatun", "Jahanara Begum", "Shahida Begum", "Ambia Khatun", "Rashida Akter", "Ferdousi Begum", "Shahinur Akter", "Nargis Akter", "Momena Khatun", "Kulsum Begum", "Shamsun Nahar"]
    },
    "India": {"male": ["Rajesh Kumar", "Amit Sharma", "Vikram Singh", "Suresh Patel", "Deepak Verma", "Rahul Gupta", "Anil Joshi", "Sanjay Mishra", "Prakash Rao", "Manoj Tiwari", "Sunil Shetty", "Karan Mehta", "Nitin Agarwal", "Rohan Kapoor", "Rajat Verma", "Mohit Chauhan", "Gaurav Singh", "Lalit Pandey", "Sameer Khan", "Ankur Sharma"], "female": ["Priya Sharma", "Suman Devi", "Neha Gupta", "Pooja Singh", "Anita Verma", "Ritu Patel", "Kavita Joshi", "Sunita Rao", "Rekha Devi", "Geeta Kumari", "Anjali Gupta", "Shweta Singh", "Nisha Sharma", "Sonia Kapoor", "Deepika R", "Megha Agarwal", "Divya Sharma", "Shalini Singh", "Priyanka Jha", "Kajal Verma"]},
    "Pakistan": {"male": ["Muhammad Ali", "Ahmed Khan", "Hassan Raza", "Bilal Ahmed", "Usman Malik", "Farhan Iqbal", "Kamran Khan", "Naveed Akhtar", "Tariq Mehmood", "Shoaib Akram", "Imran Hashmi", "Adil Hussain", "Qasim Ali", "Faisal Javed", "Zubair Ahmed", "Shahid Afridi", "Shoaib Malik", "Misbah Khan", "Asghar Khan", "Javed Miandad"], "female": ["Sana Khan", "Ayesha Malik", "Fatima Ali", "Zainab Ahmed", "Hira Butt", "Nadia Hussain", "Sadia Khan", "Rabia Bashir", "Tahira Iqbal", "Shazia Parveen", "Saima Ali", "Komal Rizvi", "Uzma Gillani", "Mahira Khan", "Saba Qamar", "Mahnoor Baloch", "Aamina Sheikh", "Sarwat Gilani", "Sania Saeed", "Sonya Hussain"]},
    "USA": {"male": ["James Smith", "John Johnson", "Robert Williams", "Michael Brown", "David Jones", "Daniel Miller", "Christopher Davis", "Matthew Wilson", "Andrew Taylor", "Ryan Anderson", "Joshua Thomas", "Brandon Jackson", "Justin White", "Kevin Harris", "Jason Martin", "Eric Thompson", "Brian Garcia", "Tyler Robinson", "Steven Clark", "Patrick Lewis"], "female": ["Mary Smith", "Jennifer Johnson", "Linda Williams", "Patricia Brown", "Elizabeth Jones", "Susan Miller", "Jessica Davis", "Sarah Wilson", "Karen Taylor", "Nancy Anderson", "Lisa Thomas", "Betty Jackson", "Dorothy White", "Sandra Harris", "Ashley Martin", "Amanda Thompson", "Kimberly Garcia", "Donna Robinson", "Emily Clark", "Carol Lewis"]},
    "UAE": {"male": ["Mohammed Al-Rashid", "Ahmed Al-Maktoum", "Ali Al-Nahyan", "Omar Al-Sayed", "Khalid Hassan", "Saeed Al-Mansoori", "Hamdan Al-Ali", "Rashid Al-Qasimi", "Sultan Al-Muhairi", "Majid Al-Falasi", "Abdulla Al Hashmi", "Yousef Al Serkal", "Jamal Al Nasser", "Hassan Al Nuaimi", "Ibrahim Al Zaabi", "Saqr Al Mansouri", "Khalifa Al Shamsi", "Rashid Al Ketbi", "Suhail Al Mazrouei", "Tariq Al Marri"], "female": ["Mariam Al-Mansoori", "Fatima Al-Suwaidi", "Aisha Al-Nuaimi", "Noora Al-Kaabi", "Sara Al-Hashimi", "Amna Al-Mazrouei", "Layla Al-Qubaisi", "Hind Al-Mehairi", "Mona Al-Blooshi", "Shamma Al-Shamsi", "Moza Al Marri", "Sheikha Al Ketbi", "Maha Al Zarooni", "Rawda Al Suwaidi", "Shaikha Al Muhairi", "Aysha Al Falasi", "Nadia Al Shamsi", "Sara Al Neyadi", "Fatima Al Marri", "Noura Al Kaabi"]},
    "Saudi Arabia": {"male": ["Khalid Al-Saud", "Fahad Al-Otaibi", "Majid Al-Ghamdi", "Sultan Al-Harbi", "Nasser Al-Dosari", "Abdullah Al-Zahrani", "Ibrahim Al-Shammari", "Saleh Al-Anazi", "Bandar Al-Mutairi", "Turki Al-Qahtani", "Mohammed Al-Ahmari", "Saad Al-Shahrani", "Faisal Al-Bishi", "Omar Al-Hawasawi", "Meshal Al-Tamimi", "Yasser Al-Qahtani", "Hassan Al-Juhani", "Mansour Al-Thagafi", "Nawaf Al-Abidi", "Sami Al-Jaber"], "female": ["Noura Al-Saud", "Sara Al-Otaibi", "Rania Al-Ghamdi", "Lama Al-Harbi", "Dana Al-Dosari", "Razan Al-Zahrani", "Maha Al-Shammari", "Areej Al-Anazi", "Huda Al-Mutairi", "Afnan Al-Qahtani", "Alaa Al-Ahmari", "Nadia Al-Shahrani", "Samar Al-Bishi", "Rasha Al-Hawasawi", "Wafaa Al-Tamimi", "Mona Al-Qahtani", "Dalia Al-Juhani", "Hessa Al-Thagafi", "Wijdan Al-Abidi", "Bayan Al-Jaber"]}
}

COUNTRIES = {"BD": "Bangladesh", "IN": "India", "PK": "Pakistan", "US": "USA", "GB": "United Kingdom", "AE": "UAE", "SA": "Saudi Arabia", "ID": "Indonesia", "MY": "Malaysia", "PH": "Philippines", "SG": "Singapore", "TH": "Thailand", "VN": "Vietnam", "TR": "Turkey", "EG": "Egypt", "NG": "Nigeria", "KE": "Kenya", "ZA": "South Africa", "BR": "Brazil", "MX": "Mexico", "AR": "Argentina", "CO": "Colombia", "DE": "Germany", "FR": "France", "IT": "Italy", "ES": "Spain", "NL": "Netherlands", "RU": "Russia", "JP": "Japan", "KR": "South Korea", "CN": "China", "AU": "Australia", "CA": "Canada", "NP": "Nepal", "LK": "Sri Lanka"}

REAL_UAS = [
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; 23116PN5BC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 9 Pro XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; OnePlus 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/134.0.6998.89 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; Redmi Note 13 Pro+) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; HUAWEI P60 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.113 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; 22071219AI) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; 2211133C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.85 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/127.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-A556B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Poco F5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.85 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; HUAWEI Mate 50 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.84 Mobile Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-A236E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.84 Mobile Safari/537.36",
]

# ═══════════════════════════════════════════════════════════════
# ANIMATION & UI
# ═══════════════════════════════════════════════════════════════

def loading_animation(text="Processing", duration=2):
    """Show loading animation"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{C.C}{frames[i % len(frames)]}{C.N} {C.Y}{text}...{C.N}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    print(f"\r{C.G}✓{C.N} {C.Y}{text}{C.N} {' ' * 20}")

def spinner(text="Working..."):
    """Generator spinner"""
    frames = ["◴", "◷", "◶", "◵"]
    i = 0
    while True:
        sys.stdout.write(f"\r{C.C}{frames[i % 4]}{C.N} {text}")
        sys.stdout.flush()
        i += 1
        yield
        time.sleep(0.15)

def progress_bar(current, total, prefix="Progress", suffix="", length=30):
    """Show progress bar"""
    filled = int(length * current // total) if total > 0 else 0
    bar = f"{C.G}{'█' * filled}{C.D}{'░' * (length - filled)}{C.N}"
    pct = (current / total) * 100 if total > 0 else 0
    sys.stdout.write(f"\r{prefix} |{bar}| {C.Y}{pct:.1f}%{C.N} {suffix}")
    sys.stdout.flush()

def box(text, color=C.C, width=58):
    """Draw a box around text"""
    lines = text.split('\n')
    print(f"{color}╔{'═' * width}╗{C.N}")
    for line in lines:
        print(f"{color}║{C.N} {line:<{width-1}}{color}║{C.N}")
    print(f"{color}╚{'═' * width}╝{C.N}")

def show_banner():
    """Professional animated banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    banner_lines = [
        f"{C.R}  ███████╗███████╗ █████╗  ██████╗███████╗██████╗  ██████╗  █████╗ {C.N}",
        f"{C.R}  ██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗{C.N}",
        f"{C.R}  █████╗  █████╗  ███████║██║     █████╗  ██████╔╝██████╔╝███████║{C.N}",
        f"{C.R}  ██╔══╝  ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗██╔══██╗██╔══██║{C.N}",
        f"{C.R}  ██║     ███████╗██║  ██║╚██████╗███████╗██║  ██║██████╔╝██║  ██║{C.N}",
        f"{C.R}  ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝{C.N}",
    ]
    
    for line in banner_lines:
        print(line)
        time.sleep(0.05)
    
    print()
    print(f"{C.M}   █████╗  ██████╗  ██████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗{C.N}")
    print(f"{C.M}  ██╔══██╗██╔════╝ ██╔════╝ ██╔══██╗██║   ██║████╗  ██║╚══██╔══╝{C.N}")
    print(f"{C.M}  ███████║██║  ███╗██║  ███╗██████╔╝██║   ██║██╔██╗ ██║   ██║   {C.N}")
    print(f"{C.M}  ██╔══██║██║   ██║██║   ██║██╔══██╗██║   ██║██║╚██╗██║   ██║   {C.N}")
    print(f"{C.M}  ██║  ██║╚██████╔╝╚██████╔╝██║  ██║╚██████╔╝██║ ╚████║   ██║   {C.N}")
    print(f"{C.M}  ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   {C.N}")
    
    print(f"\n{C.C}  ╔══════════════════════════════════════════════════════════════════════╗{C.N}")
    print(f"{C.C}  ║{C.N}  {C.BOLD}{C.W}FB ACCOUNT CREATOR v2.0 — PROFESSIONAL EDITION{C.N}              {C.C}║{C.N}")
    print(f"{C.C}  ║{C.N}  {C.Y}Email  |  Phone  |  Auto-Mail  |  Temp Mail  |  Cookie Jar{C.N}    {C.C}║{C.N}")
    print(f"{C.C}  ║{C.N}  {C.D}Authorized Security Testing Tool{C.N}                              {C.C}║{C.N}")
    print(f"{C.C}  ╚══════════════════════════════════════════════════════════════════════╝{C.N}")
    print()

def show_config():
    """Show configuration in a nice box"""
    m = CONFIG["method"].upper()
    icons = {"EMAIL": "📧", "PHONE": "📱", "AUTOMAIL": "⚡"}
    icon = icons.get(m, "📧")
    
    lines = []
    lines.append(f"  {C.W}METHOD  :{C.N} {icon} {C.G}{m:15s}{C.N}    {C.W}COUNT :{C.N} {C.Y}{CONFIG['count']:<5}{C.N}")
    lines.append(f"  {C.W}COUNTRY :{C.N} {C.G}{CONFIG['country']:20s}{C.N}  {C.W}THREADS:{C.N} {C.Y}{CONFIG['threads']:<5}{C.N}")
    lines.append(f"  {C.W}GENDER  :{C.N} {C.G}{CONFIG['gender']:20s}{C.N}  {C.W}DELAY  :{C.N} {C.Y}{CONFIG['delay']}s{C.N}")
    lines.append(f"  {C.W}BIRTHDAY:{C.N} {C.G}{CONFIG['birth_day']}/{CONFIG['birth_month']}/{CONFIG['birth_year']:10s}{C.N}")
    lines.append(f"  {C.W}NAME    :{C.N} {C.G}{CONFIG['custom_name'] if CONFIG['custom_name'] else 'Auto by Country':25s}{C.N}")
    lines.append(f"  {C.W}PASSWORD:{C.N} {C.G}{CONFIG['password'] if CONFIG['password'] else 'Auto-Generated Random':25s}{C.N}")
    lines.append(f"  {C.W}PROXY   :{C.N} {C.G}{'ENABLED' if CONFIG['use_proxy'] else 'DISABLED':25s}{C.N}")
    if CONFIG["success"] > 0:
        lines.append(f"  {C.W}STATS   :{C.N} {C.G}✓ Created: {CONFIG['success']}{C.N}  {C.R}✗ Failed: {CONFIG['failed']}{C.N}")
    box('\n'.join(lines), C.C, 56)

def input_with_default(prompt, default=""):
    """Get input with default value"""
    val = input(f"{C.C}║{C.N} {prompt}{C.D}[{default}]{C.N}: ").strip()
    return val if val else default

# ═══════════════════════════════════════════════════════════════
# INTERACTIVE WIZARD
# ═══════════════════════════════════════════════════════════════

def interactive_wizard():
    """Interactive setup wizard — asks questions one by one"""
    print()
    box(f"  {C.BOLD}{C.W}SETUP WIZARD{C.N}  \n  {C.D}Configure your preferences step by step{C.N}", C.M, 50)
    print()
    
    # Step 1: Method
    print(f"{C.Y}  Step 1: Choose Method{C.N}")
    print(f"  {C.C}[1]{C.N} Email — Use your own email list")
    print(f"  {C.C}[2]{C.N} Phone — Use your own phone number list")
    print(f"  {C.C}[3]{C.N} Auto Mail — Generate temp emails automatically")
    m = input(f"{C.G}  Choice (1-3) [{C.Y}3{C.G}]: {C.N}").strip() or "3"
    methods = {"1": "email", "2": "phone", "3": "automail"}
    CONFIG["method"] = methods.get(m, "automail")
    print(f"  {C.G}✓ Method: {CONFIG['method'].upper()}{C.N}\n")
    loading_animation("Setting method", 0.5)
    
    # Step 2: How many accounts
    print(f"{C.Y}  Step 2: How many accounts to create?{C.N}")
    count = input(f"{C.G}  Number [{C.Y}5{C.G}]: {C.N}").strip() or "5"
    CONFIG["count"] = max(1, int(count) if count.isdigit() else 5)
    print(f"  {C.G}✓ Will create {CONFIG['count']} accounts{C.N}\n")
    
    # Step 3: Country
    print(f"{C.Y}  Step 3: Select Country{C.N}")
    codes = list(COUNTRIES.keys())
    for i, code in enumerate(codes, 1):
        print(f"  {C.C}[{i:2d}]{C.N} {COUNTRIES[code]:25s} ({code})")
    c_idx = input(f"{C.G}  Choice (1-{len(codes)}) [{C.Y}1{C.G}]: {C.N}").strip() or "1"
    try:
        idx = max(0, min(len(codes)-1, int(c_idx)-1))
        CONFIG["country"] = COUNTRIES[codes[idx]]
    except:
        CONFIG["country"] = "Bangladesh"
    print(f"  {C.G}✓ Country: {CONFIG['country']}{C.N}\n")
    
    # Step 4: Gender
    print(f"{C.Y}  Step 4: Gender{C.N}")
    print(f"  {C.C}[1]{C.N} Male")
    print(f"  {C.C}[2]{C.N} Female")
    g = input(f"{C.G}  Choice (1-2) [{C.Y}1{C.G}]: {C.N}").strip() or "1"
    CONFIG["gender"] = "male" if g == "1" else "female"
    print(f"  {C.G}✓ Gender: {CONFIG['gender']}{C.N}\n")
    
    # Step 5: Password
    print(f"{C.Y}  Step 5: Password (or blank for auto-generated){C.N}")
    pw = input(f"{C.G}  Password: {C.N}").strip()
    if pw:
        CONFIG["password"] = pw
        print(f"  {C.G}✓ Password set: {pw}{C.N}")
    else:
        CONFIG["password"] = ""
        print(f"  {C.Y}✓ Auto-generated password will be used{C.N}")
    print()
    
    # Step 6: Birthday
    print(f"{C.Y}  Step 6: Birthday{C.N}")
    dd = input(f"{C.G}  Day (1-31) [{C.Y}15{C.G}]: {C.N}").strip() or "15"
    mm = input(f"{C.G}  Month (1-12) [{C.Y}6{C.G}]: {C.N}").strip() or "6"
    yy = input(f"{C.G}  Year [{C.Y}1998{C.G}]: {C.N}").strip() or "1998"
    CONFIG["birth_day"] = max(1, min(31, int(dd) if dd.isdigit() else 15))
    CONFIG["birth_month"] = max(1, min(12, int(mm) if mm.isdigit() else 6))
    CONFIG["birth_year"] = max(1950, min(2005, int(yy) if yy.isdigit() else 1998))
    print(f"  {C.G}✓ Birthday: {CONFIG['birth_day']}/{CONFIG['birth_month']}/{CONFIG['birth_year']}{C.N}\n")
    
    # Step 7: Custom Name
    print(f"{C.Y}  Step 7: Custom Name (or blank for auto by country){C.N}")
    name = input(f"{C.G}  Name: {C.N}").strip()
    CONFIG["custom_name"] = name if name else ""
    if name:
        print(f"  {C.G}✓ Name set: {name}{C.N}")
    else:
        print(f"  {C.Y}✓ Auto name by country{C.N}")
    print()
    
    # Step 8: Proxy
    print(f"{C.Y}  Step 8: Use Proxy?{C.N}")
    print(f"  {C.C}[1]{C.N} Yes — Use proxy list")
    print(f"  {C.C}[2]{C.N} No — Direct connection")
    px = input(f"{C.G}  Choice (1-2) [{C.Y}2{C.G}]: {C.N}").strip() or "2"
    CONFIG["use_proxy"] = (px == "1")
    print(f"  {C.G}✓ Proxy: {'ENABLED' if CONFIG['use_proxy'] else 'DISABLED'}{C.N}\n")
    
    # Step 9: Threads
    print(f"{C.Y}  Step 9: Threads (more threads = faster){C.N}")
    t = input(f"{C.G}  Threads (1-20) [{C.Y}5{C.G}]: {C.N}").strip() or "5"
    CONFIG["threads"] = max(1, min(20, int(t) if t.isdigit() else 5))
    print(f"  {C.G}✓ Threads: {CONFIG['threads']}{C.N}\n")
    
    # Step 10: Delay
    print(f"{C.Y}  Step 10: Delay between accounts (seconds){C.N}")
    d = input(f"{C.G}  Delay [{C.Y}3.0{C.G}]: {C.N}").strip() or "3.0"
    CONFIG["delay"] = max(0.5, float(d) if d.replace('.','',1).isdigit() else 3.0)
    print(f"  {C.G}✓ Delay: {CONFIG['delay']}s{C.N}\n")
    
    save_config()
    loading_animation("Finalizing configuration", 1)
    
    box(f"  {C.G}{C.BOLD}✅ CONFIGURATION COMPLETE!{C.N}  \n  {C.W}Press {C.G}[S]{C.W} to start creating accounts{C.N}", C.G, 45)

# ═══════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def load_config():
    if os.path.exists("config.json"):
        try:
            with open("config.json") as f: CONFIG.update(json.load(f))
        except: pass

def save_config():
    try:
        with open("config.json", "w") as f: json.dump(CONFIG, f, indent=2)
    except: pass

def load_file(path):
    try:
        with open(path, "r") as f: return [l.strip() for l in f if l.strip()]
    except: return []

def get_random_name():
    if CONFIG["custom_name"]: return CONFIG["custom_name"]
    country = CONFIG.get("country", "Bangladesh")
    gender = CONFIG.get("gender", "male")
    names = NAMES_BY_COUNTRY.get(country, NAMES_BY_COUNTRY["Bangladesh"])
    return random.choice(names.get(gender, names["male"]))

def gen_password():
    if CONFIG["password"]: return CONFIG["password"]
    return ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%&", k=12)) + "A1@"

def gen_temp_email():
    u = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    return f"{u}@1secmail.com"

def get_proxy(proxies, idx=[0]):
    if not CONFIG["use_proxy"] or not proxies: return None
    with threading.Lock():
        p = proxies[idx[0] % len(proxies)]; idx[0] += 1
    return {"http": p, "https": p}

def create_session():
    s = requests.Session(); s.verify = False
    return s

def check_temp_mail(email, session):
    try:
        u, d = email.split("@")
        r = session.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={u}&domain={d}", timeout=10)
        if r.status_code == 200 and r.json():
            msg = r.json()[-1]
            cr = session.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={u}&domain={d}&id={msg['id']}", timeout=10)
            if cr.status_code == 200:
                body = cr.json().get("body", "") + " " + cr.json().get("htmlBody", "")
                for p in [r'(\d{6})[^0-9]*$', r'[Cc]ode[:\s]*(\d{6})', r'FB-(\d{6})', r'(\d{6})\s*is\s*your', r'(\d{6})\s*FB']:
                    m = re.search(p, body)
                    if m: return m.group(1)
    except: pass
    return None

def create_account(email, password, name, proxies, session):
    """Create Facebook account"""
    try:
        fn = name.split()[0]
        ln = " ".join(name.split()[1:]) if len(name.split()) > 1 else "Khan"
        ua = random.choice(REAL_UAS)
        proxy = get_proxy(proxies)
        
        headers = {
            "User-Agent": ua, "Accept": "text/html,*/*", "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.facebook.com", "Referer": "https://www.facebook.com/",
        }
        
        # Get initial page
        r1 = session.get("https://www.facebook.com/", headers=headers, proxies=proxy, timeout=15)
        
        # Extract tokens
        fb_dtsg = re.search(r'name="fb_dtsg"[^>]+value="([^"]+)"', r1.text)
        lsd = re.search(r'"LSD",\[\],{"token":"([^"]+)"', r1.text)
        jazoest = re.search(r'name="jazoest"[^>]+value="([^"]+)"', r1.text)
        
        # Build reg data
        data = {
            "lsd": lsd.group(1) if lsd else "",
            "jazoest": jazoest.group(1) if jazoest else "2",
            "fb_dtsg": fb_dtsg.group(1) if fb_dtsg else "",
            "firstname": fn, "lastname": ln,
            "reg_email__": email, "reg_email_confirmation__": email,
            "reg_passwd__": password,
            "birthday_day": str(CONFIG["birth_day"]),
            "birthday_month": str(CONFIG["birth_month"]),
            "birthday_year": str(CONFIG["birth_year"]),
            "sex": "2" if CONFIG["gender"] == "male" else "1",
            "locale": "en_US", "reg_instance": str(int(time.time())),
            "reg_impression_id": ''.join(random.choices(string.hexdigits, k=32)).lower(),
            "source": "reg_dialog", "referrer": "", "ref": "", "sk": "",
            "meta_referrer": "https://www.facebook.com/",
        }
        
        r2 = session.post("https://www.facebook.com/reg/", data=data, headers=headers, proxies=proxy, timeout=15)
        
        # Check for confirmation code
        code = None
        if "confirm" in r2.url.lower() or "code" in r2.url.lower() or "enter_code" in r2.url.lower():
            for _ in range(24):  # 2 minutes max
                time.sleep(5)
                code = check_temp_mail(email, session)
                if code: break
        
        if code:
            r3 = session.post(r2.url, data={"code": code, "fb_dtsg": fb_dtsg.group(1) if fb_dtsg else ""}, headers=headers, proxies=proxy, timeout=15)
            if "welcome" in r3.url.lower() or "home" in r3.url.lower() or r3.status_code == 200:
                return {"ok": True, "name": name, "email": email, "password": password, "code": code, "cookies": dict(session.cookies.get_dict())}
        
        if "welcome" in r2.url.lower() or "home" in r2.url.lower():
            return {"ok": True, "name": name, "email": email, "password": password, "code": "AUTO", "cookies": dict(session.cookies.get_dict())}
        
        return {"ok": False, "error": f"URL: {r2.url[:60]}", "email": email, "password": password, "name": name}
        
    except Exception as e:
        return {"ok": False, "error": str(e)[:60], "email": email, "password": password, "name": name}

def worker(q, proxies, lock):
    """Worker thread"""
    session = create_session()
    while CONFIG["running"]:
        try:
            job = q.get(timeout=2)
            if job is None: break
            idx, email, pw, name = job
            
            with lock:
                CONFIG["created"] += 1
            
            result = create_account(email, pw, name, proxies, session)
            
            with lock:
                if result.get("ok"):
                    CONFIG["success"] += 1
                    # Save
                    method = CONFIG["method"]
                    fpath = f"{ACCOUNTS_DIR}/{method}_accounts.txt"
                    with open(fpath, "a", encoding="utf-8") as f:
                        f.write(f"{'='*60}\n")
                        f.write(f"Account #{CONFIG['success']}\n")
                        f.write(f"Name     : {result.get('name', '')}\n")
                        f.write(f"Email    : {result.get('email', '')}\n")
                        f.write(f"Password : {result.get('password', '')}\n")
                        f.write(f"Code     : {result.get('code', '')}\n")
                        f.write(f"Country  : {CONFIG['country']}\n")
                        f.write(f"Gender   : {CONFIG['gender']}\n")
                        f.write(f"Birthday : {CONFIG['birth_day']}/{CONFIG['birth_month']}/{CONFIG['birth_year']}\n")
                        f.write(f"Method   : {method}\n")
                        f.write(f"Created  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write(f"{'='*60}\n\n")
                    
                    print(f"\n{C.G}{C.BOLD}  ✓ CREATED #{CONFIG['success']}: {name[:20]:20s} | {email[:18]:18s} | {pw}{C.N}")
                else:
                    CONFIG["failed"] += 1
                    err = result.get("error", "Unknown")
                    print(f"\n{C.R}  ✗ FAILED #{CONFIG['created']}: {email[:18]:18s} | {err[:40]}{C.N}")
                    
                    with open(f"{ACCOUNTS_DIR}/failed.txt", "a") as f:
                        f.write(f"{email} | {pw} | {name} | {err}\n")
            
            q.task_done()
            time.sleep(CONFIG["delay"])
        except: continue

def start_creator():
    """Start account creation"""
    if CONFIG["running"]:
        print(f"{C.R}[!] Already running!{C.N}"); return
    
    method = CONFIG["method"]
    count = CONFIG["count"]
    
    proxies = load_file(CONFIG["proxy_file"]) if CONFIG["use_proxy"] else []
    
    accounts = []
    if method == "email":
        emails = load_file(CONFIG["email_file"])
        if not emails: print(f"{C.R}[!] No emails in {CONFIG['email_file']}!{C.N}"); return
        if count > len(emails): count = len(emails)
        for i in range(count):
            accounts.append((emails[i], gen_password(), get_random_name()))
    elif method == "phone":
        nums = load_file(CONFIG["number_file"])
        if not nums: print(f"{C.R}[!] No numbers in {CONFIG['number_file']}!{C.N}"); return
        if count > len(nums): count = len(nums)
        for i in range(count):
            accounts.append((nums[i], gen_password(), get_random_name()))
    elif method == "automail":
        for i in range(count):
            accounts.append((gen_temp_email(), gen_password(), get_random_name()))
    
    if not accounts: print(f"{C.R}[!] No accounts!{C.N}"); return
    
    CONFIG["running"] = True
    CONFIG["created"] = 0; CONFIG["success"] = 0; CONFIG["failed"] = 0
    lock = threading.Lock()
    q = Queue()
    
    def producer():
        for i, (em, pw, nm) in enumerate(accounts):
            if not CONFIG["running"]: break
            q.put((i+1, em, pw, nm))
            time.sleep(0.1)
    
    # Show banner
    print()
    box(f"  {C.BOLD}{C.G}🚀 CREATING {count} FACEBOOK ACCOUNTS{C.N}  \n"
        f"  {C.W}Method : {C.Y}{method.upper():20s}{C.N}  \n"
        f"  {C.W}Country: {C.Y}{CONFIG['country']:20s}{C.N}  \n"
        f"  {C.W}Threads: {C.Y}{CONFIG['threads']:<20}{C.N}  \n"
        f"  {C.W}Proxy  : {C.Y}{'ON' if CONFIG['use_proxy'] else 'OFF':20s}{C.N}  \n"
        f"  {C.W}Output : {C.Y}{ACCOUNTS_DIR}/{method}_accounts.txt{C.N}  \n"
        f"  {C.W}Press  : {C.R}[X]{C.W} in menu to STOP{C.N}", C.G, 52)
    print()
    
    # Start threads
    for _ in range(CONFIG["threads"]):
        t = threading.Thread(target=worker, args=(q, proxies, lock), daemon=True)
        t.start()
    
    prod = threading.Thread(target=producer, daemon=True)
    prod.start()
    
    # Live progress
    try:
        while CONFIG["running"] and CONFIG["created"] < len(accounts):
            time.sleep(2)
            total = CONFIG["created"]
            ok = CONFIG["success"]
            fail = CONFIG["failed"]
            progress_bar(total, len(accounts), f"  {C.C}Progress{C.N}", 
                        f"{C.G}✓{ok}{C.N} {C.R}✗{fail}{C.N} {C.Y}{total}/{len(accounts)}{C.N}")
    except: pass
    
    print(f"\n\n{C.G}{C.BOLD}  ✅ COMPLETED!{C.N}")
    print(f"  {C.C}Created: {C.G}{CONFIG['success']}{C.N}  {C.R}Failed: {CONFIG['failed']}{C.N}")
    print(f"  {C.C}Saved to: {C.Y}{ACCOUNTS_DIR}/{method}_accounts.txt{C.N}\n")
    CONFIG["running"] = False

# ═══════════════════════════════════════════════════════════════
# MAIN MENU
# ═══════════════════════════════════════════════════════════════

def main():
    load_config()
    
    # Ensure files exist
    for f in ["emails.txt", "numbers.txt", "proxies.txt", "temp_mails.txt"]:
        if not os.path.exists(f): open(f, "a").close()
    
    while True:
        show_banner()
        show_config()
        
        print(f"{C.Y}╔══════════════════════════════════════════════════════════════════════╗{C.N}")
        print(f"{C.Y}║{C.N}  {C.C}[{C.G}W{C.C}]{C.N} Setup Wizard (step by step config)                              {C.Y}║{C.N}")
        print(f"{C.Y}║{C.N}  {C.C}[{C.G}1{C.C}]{C.N} Method: {C.G}Email{C.N}     {C.C}[{C.G}2{C.C}]{C.N} Method: {C.G}Phone{C.N}     {C.C}[{C.G}3{C.C}]{C.N} Method: {C.G}Auto Mail{C.N}  {C.Y}║{C.N}")
        print(f"{C.Y}║{C.N}  {C.C}[{C.G}4{C.C}]{C.N} Account Count   {C.C}[{C.G}5{C.C}]{C.N} Threads & Delay  {C.C}[{C.G}6{C.C}]{C.N} Country          {C.Y}║{C.N}")
        print(f"{C.Y}║{C.N}  {C.C}[{C.G}7{C.C}]{C.N} Gender          {C.C}[{C.G}8{C.C}]{C.N} Password         {C.C}[{C.G}9{C.C}]{C.N} Birthday          {C.Y}║{C.N}")
        print(f"{C.Y}║{C.N}  {C.C}[{C.G}10{C.C}]{C.N} Custom Name     {C.C}[{C.G}11{C.C}]{C.N} Toggle Proxy     {C.C}[{C.G}12{C.C}]{C.N} Add Email/Number  {C.Y}║{C.N}")
        print(f"{C.Y}║{C.N}  {C.C}[{C.G}13{C.C}]{C.N} View Accounts    {C.C}[{C.G}14{C.C}]{C.N} Save/Load Config                                    {C.Y}║{C.N}")
        print(f"{C.Y}║{C.N}                                                                      {C.Y}║{C.N}")
        print(f"{C.Y}║{C.N}  {C.G}{C.BOLD}[S] ▶ START CREATING{C.N}            {C.R}{C.BOLD}[X] ■ STOP{C.N}            {C.W}{C.BOLD}[0] EXIT{C.N}           {C.Y}║{C.N}")
        print(f"{C.Y}╚══════════════════════════════════════════════════════════════════════╝{C.N}")
        
        ch = input(f"\n{C.G}{C.BOLD}  ➤ Choice: {C.N}").strip().lower()
        
        if ch == "w": interactive_wizard()
        elif ch == "1": CONFIG["method"] = "email"; save_config(); print(f"{C.G}✓ Method: EMAIL{C.N}")
        elif ch == "2": CONFIG["method"] = "phone"; save_config(); print(f"{C.G}✓ Method: PHONE{C.N}")
        elif ch == "3": CONFIG["method"] = "automail"; save_config(); print(f"{C.G}✓ Method: AUTO MAIL{C.N}")
        elif ch == "4":
            try:
                c = int(input(f"{C.G}  How many accounts?: {C.N}"))
                CONFIG["count"] = max(1, c); save_config()
            except: print(f"{C.R}Invalid{C.N}")
        elif ch == "5":
            try:
                t = input(f"{C.G}  Threads [{CONFIG['threads']}]: {C.N}").strip()
                if t: CONFIG["threads"] = max(1, min(20, int(t)))
                d = input(f"{C.G}  Delay [{CONFIG['delay']}]: {C.N}").strip()
                if d: CONFIG["delay"] = max(0.5, float(d))
                save_config()
            except: print(f"{C.R}Invalid{C.N}")
        elif ch == "6":
            print(f"\n{C.C}Countries:{C.N}")
            codes = list(COUNTRIES.keys())
            for i, code in enumerate(codes, 1):
                print(f"  {i:2d}. {COUNTRIES[code]}")
            try:
                idx = int(input(f"{C.G}  Choose: {C.N}")) - 1
                if 0 <= idx < len(codes): CONFIG["country"] = COUNTRIES[codes[idx]]; save_config()
            except: print(f"{C.R}Invalid{C.N}")
        elif ch == "7":
            g = input(f"{C.G}  Gender (male/female) [{CONFIG['gender']}]: {C.N}").strip().lower()
            if g in ("male", "female"): CONFIG["gender"] = g; save_config()
        elif ch == "8":
            p = input(f"{C.G}  Password (or 'auto'): {C.N}").strip()
            CONFIG["password"] = "" if p.lower() == "auto" else p; save_config()
        elif ch == "9":
            try:
                d = int(input(f"{C.G}  Day [{CONFIG['birth_day']}]: {C.N}") or CONFIG['birth_day'])
                m = int(input(f"{C.G}  Month [{CONFIG['birth_month']}]: {C.N}") or CONFIG['birth_month'])
                y = int(input(f"{C.G}  Year [{CONFIG['birth_year']}]: {C.N}") or CONFIG['birth_year'])
                CONFIG["birth_day"] = max(1, min(31, d))
                CONFIG["birth_month"] = max(1, min(12, m))
                CONFIG["birth_year"] = max(1950, min(2005, y))
                save_config()
            except: print(f"{C.R}Invalid{C.N}")
        elif ch == "10":
            n = input(f"{C.G}  Custom name (or 'auto'): {C.N}").strip()
            CONFIG["custom_name"] = "" if n.lower() == "auto" else n; save_config()
        elif ch == "11":
            CONFIG["use_proxy"] = not CONFIG["use_proxy"]; save_config()
            print(f"{C.G}✓ Proxy: {'ON' if CONFIG['use_proxy'] else 'OFF'}{C.N}")
        elif ch == "12":
            val = input(f"{C.G}  Enter email or phone: {C.N}").strip()
            if val:
                f = CONFIG["number_file"] if val.replace('+','',1).replace('-','').isdigit() else CONFIG["email_file"]
                with open(f, "a") as fh: fh.write(val + "\n")
                print(f"{C.G}✓ Added: {val}{C.N}")
        elif ch == "13":
            files = [f for f in os.listdir(ACCOUNTS_DIR) if f.endswith(".txt") and f != "failed.txt"]
            if files:
                print(f"\n{C.C}Saved Account Files:{C.N}")
                for f in files:
                    fp = os.path.join(ACCOUNTS_DIR, f)
                    with open(fp) as fh: lines = fh.read().strip().split('\n')
                    count = lines.count('='*60)
                    size = os.path.getsize(fp)
                    print(f"  {C.G}{f}{C.N} — {count} accounts ({size} bytes)")
                print()
                # Show last 5 lines of most recent file
                latest = max(files, key=lambda f: os.path.getmtime(os.path.join(ACCOUNTS_DIR, f)))
                with open(os.path.join(ACCOUNTS_DIR, latest)) as fh:
                    content = fh.read().strip().split('\n')
                print(f"{C.D}Last accounts from {latest}:{C.N}")
                print('\n'.join(content[-10:]))
            else: print(f"{C.Y}No accounts saved yet.{C.N}")
        elif ch == "14":
            s = input(f"{C.G}  1=Save  2=Load: {C.N}").strip()
            if s == "1": save_config(); print(f"{C.G}✓ Saved{C.N}")
            elif s == "2": load_config(); print(f"{C.G}✓ Loaded{C.N}")
        elif ch == "s": start_creator()
        elif ch == "x": CONFIG["running"] = False; print(f"{C.R}■ Stopped{C.N}"); time.sleep(1)
        elif ch == "0": CONFIG["running"] = False; print(f"{C.Y}Exiting...{C.N}"); time.sleep(0.5); break
        else: print(f"{C.R}Invalid option{C.N}")
        
        if ch not in ("s", "x"):
            input(f"\n{C.Y}Press Enter...{C.N}")

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{C.R}Exiting...{C.N}")
    except Exception as e: print(f"\n{C.R}Error: {e}{C.N}")
