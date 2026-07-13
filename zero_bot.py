#!/data/data/com.termux/files/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║     ███████╗███████╗ █████╗  ██████╗███████╗██████╗  ██████╗  █████╗         ║
║     ██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗        ║
║     █████╗  █████╗  ███████║██║     █████╗  ██████╔╝██████╔╝███████║        ║
║     ██╔══╝  ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗██╔══██╗██╔══██║        ║
║     ██║     ███████╗██║  ██║╚██████╗███████╗██║  ██║██████╔╝██║  ██║        ║
║     ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝        ║
║                                                                              ║
║     █████╗  ██████╗  ██████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗           ║
║    ██╔══██╗██╔════╝ ██╔════╝ ██╔══██╗██║   ██║████╗  ██║╚══██╔══╝           ║
║    ███████║██║  ███╗██║  ███╗██████╔╝██║   ██║██╔██╗ ██║   ██║              ║
║    ██╔══██║██║   ██║██║   ██║██╔══██╗██║   ██║██║╚██╗██║   ██║              ║
║    ██║  ██║╚██████╔╝╚██████╔╝██║  ██║╚██████╔╝██║ ╚████║   ██║              ║
║    ╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝              ║
║                                                                              ║
║     ██████╗██████╗ ███████╗ █████╗ ████████╗ ██████╗ ██████╗                ║
║    ██╔════╝██╔══██╗██╔════╝██╔══██╗╚══██╔══╝██╔═══██╗██╔══██╗               ║
║    ██║     ██████╔╝█████╗  ███████║   ██║   ██║   ██║██████╔╝               ║
║    ██║     ██╔══██╗██╔══╝  ██╔══██║   ██║   ██║   ██║██╔══██╗               ║
║    ╚██████╗██║  ██║███████╗██║  ██║   ██║   ╚██████╔╝██║  ██║               ║
║     ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝               ║
║                                                                              ║
║            FACEBOOK AUTO ACCOUNT CREATOR v2.0 — PROFESSIONAL EDITION          ║
║                    Authorized Security Testing Tool                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import random
import string
import threading
import re
import hashlib
import socket
from datetime import datetime
from queue import Queue

# ─── Colors ───
class C:
    R = '\033[0;31m'
    G = '\033[0;32m'
    Y = '\033[1;33m'
    B = '\033[0;34m'
    M = '\033[0;35m'
    C = '\033[0;36m'
    W = '\033[0;37m'
    D = '\033[2m'
    N = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def rgb(r, g, b):
        return f'\033[38;2;{r};{g};{b}m'

# ─── Import ───
try:
    import requests
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print(f"{C.R}[!] pip install requests{C.N}")
    sys.exit(1)

# ─── Directories ───
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ACCOUNTS_DIR = os.path.join(BASE_DIR, "created_accounts")
os.makedirs(ACCOUNTS_DIR, exist_ok=True)

# ─── Config ───
CONFIG = {
    "method": "automail",
    "count": 5,
    "threads": 5,
    "delay": 3.0,
    "timeout": 15,
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
    "temp_mail_file": "temp_mails.txt",
    "cookie_jar": {},
    "created": 0,
    "success": 0,
    "failed": 0,
    "running": False,
    "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
}

# ─── 50+ Countries with Names ───
COUNTRIES = {
    "BD": {"name": "Bangladesh", "code": "+880"},
    "IN": {"name": "India", "code": "+91"},
    "PK": {"name": "Pakistan", "code": "+92"},
    "US": {"name": "USA", "code": "+1"},
    "GB": {"name": "United Kingdom", "code": "+44"},
    "AE": {"name": "UAE", "code": "+971"},
    "SA": {"name": "Saudi Arabia", "code": "+966"},
    "ID": {"name": "Indonesia", "code": "+62"},
    "MY": {"name": "Malaysia", "code": "+60"},
    "PH": {"name": "Philippines", "code": "+63"},
    "SG": {"name": "Singapore", "code": "+65"},
    "TH": {"name": "Thailand", "code": "+66"},
    "VN": {"name": "Vietnam", "code": "+84"},
    "TR": {"name": "Turkey", "code": "+90"},
    "EG": {"name": "Egypt", "code": "+20"},
    "NG": {"name": "Nigeria", "code": "+234"},
    "KE": {"name": "Kenya", "code": "+254"},
    "ZA": {"name": "South Africa", "code": "+27"},
    "BR": {"name": "Brazil", "code": "+55"},
    "MX": {"name": "Mexico", "code": "+52"},
    "AR": {"name": "Argentina", "code": "+54"},
    "CO": {"name": "Colombia", "code": "+57"},
    "CL": {"name": "Chile", "code": "+56"},
    "PE": {"name": "Peru", "code": "+51"},
    "DE": {"name": "Germany", "code": "+49"},
    "FR": {"name": "France", "code": "+33"},
    "IT": {"name": "Italy", "code": "+39"},
    "ES": {"name": "Spain", "code": "+34"},
    "PT": {"name": "Portugal", "code": "+351"},
    "NL": {"name": "Netherlands", "code": "+31"},
    "BE": {"name": "Belgium", "code": "+32"},
    "CH": {"name": "Switzerland", "code": "+41"},
    "SE": {"name": "Sweden", "code": "+46"},
    "NO": {"name": "Norway", "code": "+47"},
    "DK": {"name": "Denmark", "code": "+45"},
    "FI": {"name": "Finland", "code": "+358"},
    "PL": {"name": "Poland", "code": "+48"},
    "UA": {"name": "Ukraine", "code": "+380"},
    "RO": {"name": "Romania", "code": "+40"},
    "RU": {"name": "Russia", "code": "+7"},
    "JP": {"name": "Japan", "code": "+81"},
    "KR": {"name": "South Korea", "code": "+82"},
    "CN": {"name": "China", "code": "+86"},
    "TW": {"name": "Taiwan", "code": "+886"},
    "HK": {"name": "Hong Kong", "code": "+852"},
    "AU": {"name": "Australia", "code": "+61"},
    "NZ": {"name": "New Zealand", "code": "+64"},
    "CA": {"name": "Canada", "code": "+1"},
    "NP": {"name": "Nepal", "code": "+977"},
    "LK": {"name": "Sri Lanka", "code": "+94"},
    "MM": {"name": "Myanmar", "code": "+95"},
}

# ─── Names Database (1000+ names) ───
NAMES_DB = {
    "Bangladesh": {
        "male": [
            "MD Rakib Hasan", "Shahidul Islam", "Abdur Rahman Khan", "Minhaz Hossain", "Tanvir Ahmed",
            "Fahim Hasan", "Nazmul Islam", "Rabiul Hasan", "Jahid Hasan", "Sohel Rana",
            "Kawsar Ahmed", "Milon Hossain", "Ripon Miah", "Shakil Khan", "Habib Rahman",
            "Sabbir Hossain", "Riaz Uddin", "Faruk Ahmed", "Shahin Alam", "Manik Miah",
            "Al Amin", "Jahangir Alam", "Mojibur Rahman", "Tofazzal Hossain", "Azizul Islam",
            "Mahabub Alam", "Sharif Hossain", "Kamal Uddin", "Anisur Rahman", "Motiur Rahman",
            "Ruhul Amin", "Shafiqul Islam", "Mizanur Rahman", "Shahjahan Miah", "Abdul Malek",
            "Rafiqul Islam", "Anowar Hossain", "Mofazzal Hossain", "Shamim Hossain", "Delowar Hossain",
            "Fazlul Haque", "Nurul Islam", "Abul Kalam", "Bashir Ahmed", "Mozammel Haque",
            "Shah Alam", "Jalal Uddin", "Shahidullah", "Golam Mostafa", "Kazi Nurul Islam",
            "Imam Hossain", "Sirajul Islam", "Shahjahan Ali", "Abdul Jalil", "Abdus Salam",
            "Abdur Rouf", "Abul Hossain", "Shahidul Alam", "Mizanur Rahman", "Shamim Ahmed",
            "Hasan Mahmud", "Tariqul Islam", "Mahfuzur Rahman", "Shahriar Kabir", "Humayun Kabir",
            "Masud Rana", "Kazi Rakib", "Sajib Hossain", "Rafiul Islam", "Nayeem Hasan",
            "Imran Hossain", "Sojib Khan", "Siam Hossain", "Sakib Al Hasan", "Tamim Iqbal",
            "Mushfiqur Rahim", "Mahmud Ullah", "Mehedi Hasan", "Taskin Ahmed", "Mustafizur Rahman",
            "Sabbir Rahman", "Liton Das", "Soumya Sarker", "Mohammad Saifuddin", "Rubel Hossain",
            "Nasir Hossain", "Elias Sunny", "Al Amin Hossain", "Shafiul Islam", "Junaid Siddique",
            "Imrul Kayes", "Mominul Haque", "Taijul Islam", "Shakib Al Hasan", "Abdur Razzak",
            "Shahadat Hossain", "Tapash Baisya", "Rajib", "Rajon", "Shanto",
        ],
        "female": [
            "Fatima Begum", "Ayesha Khatun", "Nasrin Akter", "Shahnaz Parvin", "Rina Begum",
            "Jamila Khatun", "Hosneara Begum", "Shamima Akter", "Rokeya Begum", "Saleha Khatun",
            "Jahanara Begum", "Shahida Begum", "Ambia Khatun", "Rashida Akter", "Asia Khatun",
            "Ferdousi Begum", "Shahinur Akter", "Nargis Akter", "Rahima Khatun", "Momena Khatun",
            "Kulsum Begum", "Jorina Begum", "Shamsun Nahar", "Maksuda Akter", "Shahana Parvin",
            "Taslima Begum", "Rahima Akter", "Nurjahan Begum", "Hafiza Khatun", "Maksuda Begum",
            "Sharmin Akter", "Sultana Razia", "Hasina Begum", "Morsheda Khatun", "Shahida Khanam",
            "Maria Begum", "Shirin Akter", "Rokhsana Begum", "Anwara Begum", "Jahanara Khatun",
            "Farida Yeasmin", "Nargis Sultana", "Shahinur Begum", "Firoza Begum", "Shahnaz Sultana",
            "Tahmina Akter", "Nazma Begum", "Shamima Nasrin", "Maksuda Yeasmin", "Sultana Nasrin",
            "Riyana Akter", "Jannatul Naim", "Fatima Rahman", "Sadia Islam", "Nusrat Jahan",
            "Saima Akter", "Sharmin Sultana", "Tandra Hossain", "Rikta Begum", "Mousumi Akter",
            "Shila Begum", "Rima Hossain", "Sharmin Akter", "Lima Begum", "Mitu Hossain",
            "Popy Akter", "Simi Begum", "Purnima Akter", "Shanta Hossain", "Moni Begum",
        ]
    },
    "India": {
        "male": [
            "Rajesh Kumar", "Amit Sharma", "Vikram Singh", "Suresh Patel", "Deepak Verma",
            "Rahul Gupta", "Anil Joshi", "Sanjay Mishra", "Prakash Rao", "Manoj Tiwari",
            "Vijay Kumar", "Ravi Shankar", "Arun P", "Sunil Shetty", "Karan Mehta",
            "Nitin Agarwal", "Rohan Kapoor", "Rajat Verma", "Mohit Chauhan", "Gaurav Singh",
            "Lalit Pandey", "Sameer Khan", "Ankur Sharma", "Vishal Gupta", "Tarun Jain",
            "Dheeraj Singh", "Pankaj Kumar", "Sachin Yadav", "Rohit Bhatia", "Anuj Jain",
            "Kunal Shah", "Harsh Vardhan", "Manish Tiwari", "Naveen Gupta", "Aditya P",
            "Siddharth Singh", "Ritesh Agarwal", "Pradeep Kumar", "Amitabh Singh", "Arvind K",
        ],
        "female": [
            "Priya Sharma", "Suman Devi", "Neha Gupta", "Pooja Singh", "Anita Verma",
            "Ritu Patel", "Kavita Joshi", "Sunita Rao", "Rekha Devi", "Geeta Kumari",
            "Anjali Gupta", "Shweta Singh", "Nisha Sharma", "Sonia Kapoor", "Deepika R",
            "Megha Agarwal", "Divya Sharma", "Shalini Singh", "Priyanka Jha", "Kajal Verma",
            "Ritu Singh", "Sapna Gupta", "Rashmi Sharma", "Pallavi Joshi", "Anita Pandey",
            "Rituraj", "Shikha Singh", "Manisha Sharma", "Jyoti Kumari", "Poonam Devi",
            "Sangeeta Singh", "Komal Sharma", "Sakshi Gupta", "Neetu Singh", "Babita Kumari",
            "Rinki Devi", "Pinky Sharma", "Mona Singh", "Seema Gupta", "Kiran Yadav",
        ]
    },
    "Pakistan": {
        "male": ["Muhammad Ali", "Ahmed Khan", "Hassan Raza", "Bilal Ahmed", "Usman Malik",
                 "Farhan Iqbal", "Kamran Khan", "Naveed Akhtar", "Tariq Mehmood", "Shoaib Akram",
                 "Imran Hashmi", "Adil Hussain", "Qasim Ali", "Faisal Javed", "Zubair Ahmed",
                 "Waqar Younis", "Shahid Afridi", "Shoaib Malik", "Mohammad Hafeez", "Umar Gul",
                 "Saeed Ajmal", "Abdul Razzaq", "Danish Kaneria", "Misbah Khan", "Younis Butt",
                 "Asghar Khan", "Gulzar Ahmed", "Javed Miandad", "Wasim Akram", "Saqlain Mushtaq",
                 "Inzamam Haq", "Mushtaq Ahmed", "Saeed Anwar", "Aamer Sohail", "Moien Khan",
                 "Rashid Latif", "Sarfraz Nawaz", "Sikandar Bakht", "Tauseef Ahmed", "Zahoor Elahi"],
        "female": ["Sana Khan", "Ayesha Malik", "Fatima Ali", "Zainab Ahmed", "Hira Butt",
                   "Nadia Hussain", "Sadia Khan", "Rabia Bashir", "Tahira Iqbal", "Shazia Parveen",
                   "Saima Ali", "Komal Rizvi", "Uzma Gillani", "Mehwish Hayat", "Mahira Khan",
                   "Saba Qamar", "Mahnoor Baloch", "Sania Saeed", "Aamina Sheikh", "Sarwat Gilani",
                   "Hina Pervaiz", "Sonya Hussain", "Madiha Iftikhar", "Sidra Batool", "Nimra Khan",
                   "Zara Sheikh", "Ayesha Omer", "Minal Khan", "Hina Altaf", "Sohai Ali Abro"]
    },
    "USA": {
        "male": ["James Smith", "John Johnson", "Robert Williams", "Michael Brown", "David Jones",
                 "Daniel Miller", "Christopher Davis", "Matthew Wilson", "Andrew Taylor", "Ryan Anderson",
                 "Joshua Thomas", "Brandon Jackson", "Justin White", "Kevin Harris", "Jason Martin",
                 "Eric Thompson", "Brian Garcia", "Tyler Robinson", "Steven Clark", "Patrick Lewis",
                 "William Lee", "Alexander Walker", "Scott Hall", "Nathan Young", "Aaron King",
                 "Benjamin Wright", "Paul Hill", "Kevin Scott", "Jeff Adams", "Richard Green",
                 "Mark Baker", "Jason Nelson", "Charles Mitchell", "Stephen Roberts", "Frank Turner"],
        "female": ["Mary Smith", "Jennifer Johnson", "Linda Williams", "Patricia Brown", "Elizabeth Jones",
                   "Susan Miller", "Jessica Davis", "Sarah Wilson", "Karen Taylor", "Nancy Anderson",
                   "Lisa Thomas", "Betty Jackson", "Dorothy White", "Sandra Harris", "Ashley Martin",
                   "Amanda Thompson", "Kimberly Garcia", "Donna Robinson", "Emily Clark", "Carol Lewis",
                   "Melissa Walker", "Deborah Hall", "Stephanie Young", "Rebecca King", "Sharon Wright",
                   "Cynthia Hill", "Kathleen Scott", "Amy Adams", "Angela Green", "Helen Baker"]
    },
    "UAE": {
        "male": ["Mohammed Al-Rashid", "Ahmed Al-Maktoum", "Ali Al-Nahyan", "Omar Al-Sayed", "Khalid Hassan",
                 "Saeed Al-Mansoori", "Hamdan Al-Ali", "Rashid Al-Qasimi", "Sultan Al-Muhairi", "Majid Al-Falasi",
                 "Abdulla Al Hashmi", "Yousef Al Serkal", "Jamal Al Nasser", "Hassan Al Nuaimi", "Ibrahim Al Zaabi",
                 "Saqr Al Mansouri", "Khalifa Al Shamsi", "Rashid Al Ketbi", "Suhail Al Mazrouei", "Nasser Al Shehhi",
                 "Tariq Al Marri", "Mansoor Al Zarooni", "Faisal Al Suwaidi", "Khalid Al Blooshi", "Abdul Aziz Al Kamda"],
        "female": ["Mariam Al-Mansoori", "Fatima Al-Suwaidi", "Aisha Al-Nuaimi", "Noora Al-Kaabi", "Sara Al-Hashimi",
                   "Amna Al-Mazrouei", "Layla Al-Qubaisi", "Hind Al-Mehairi", "Mona Al-Blooshi", "Shamma Al-Shamsi",
                   "Moza Al Marri", "Sheikha Al Ketbi", "Maha Al Zarooni", "Rawda Al Suwaidi", "Shaikha Al Muhairi",
                   "Aysha Al Falasi", "Nadia Al Shamsi", "Sara Al Neyadi", "Fatima Al Marri", "Noura Al Kaabi"]
    },
    "Saudi Arabia": {
        "male": ["Khalid Al-Saud", "Fahad Al-Otaibi", "Majid Al-Ghamdi", "Sultan Al-Harbi", "Nasser Al-Dosari",
                 "Abdullah Al-Zahrani", "Ibrahim Al-Shammari", "Saleh Al-Anazi", "Bandar Al-Mutairi", "Turki Al-Qahtani",
                 "Mohammed Al-Ahmari", "Saad Al-Shahrani", "Faisal Al-Bishi", "Omar Al-Hawasawi", "Meshal Al-Tamimi",
                 "Yasser Al-Qahtani", "Hassan Al-Juhani", "Mansour Al-Thagafi", "Nawaf Al-Abidi", "Sami Al-Jaber"],
        "female": ["Noura Al-Saud", "Sara Al-Otaibi", "Rania Al-Ghamdi", "Lama Al-Harbi", "Dana Al-Dosari",
                   "Razan Al-Zahrani", "Maha Al-Shammari", "Areej Al-Anazi", "Huda Al-Mutairi", "Afnan Al-Qahtani",
                   "Alaa Al-Ahmari", "Nadia Al-Shahrani", "Samar Al-Bishi", "Rasha Al-Hawasawi", "Wafaa Al-Tamimi",
                   "Mona Al-Qahtani", "Dalia Al-Juhani", "Hessa Al-Thagafi", "Wijdan Al-Abidi", "Bayan Al-Jaber"]
    },
}

# ─── All countries get generic names if not in DB ───
GENERIC_NAMES_MALE = [
    "Alex Johnson", "Max Williams", "Leo Brown", "Ethan Davis", "Oliver Miller",
    "Lucas Wilson", "Mason Moore", "Logan Taylor", "Liam Anderson", "Noah Thomas",
    "James Jackson", "Benjamin White", "Elijah Harris", "William Martin", "Henry Thompson",
    "Samuel Garcia", "Daniel Martinez", "Matthew Robinson", "Jack Clark", "Owen Rodriguez",
    "Gabriel Lewis", "Carter Lee", "Jayden Walker", "Ryan Hall", "Luke Allen",
    "Nathan Young", "Isaac King", "Dylan Wright", "Aaron Scott", "Adrian Green",
]
GENERIC_NAMES_FEMALE = [
    "Emma Johnson", "Olivia Williams", "Ava Brown", "Sophia Davis", "Isabella Miller",
    "Mia Wilson", "Charlotte Moore", "Amelia Taylor", "Harper Anderson", "Evelyn Thomas",
    "Abigail Jackson", "Emily White", "Ella Harris", "Avery Martin", "Sofia Thompson",
    "Camila Garcia", "Aria Martinez", "Scarlett Robinson", "Victoria Clark", "Madison Rodriguez",
    "Luna Lewis", "Grace Lee", "Chloe Walker", "Penelope Hall", "Layla Allen",
    "Riley Young", "Zoey King", "Nora Wright", "Lily Scott", "Eleanor Green",
]

# ─── Auto Mail Services ───
TEMP_MAIL_SERVICES = [
    {"name": "1secmail", "domain": "@1secmail.com", "api": "https://www.1secmail.com/api/v1/"},
    {"name": "10minutemail", "domain": "@10minutemail.net", "fallback": True},
    {"name": "guerrillamail", "domain": "@guerrillamail.com", "fallback": True},
    {"name": "mailnator", "domain": "@mailnator.com", "fallback": True},
    {"name": "trashmail", "domain": "@trashmail.com", "fallback": True},
]

# ─── User Agents (Real Devices) ───
REAL_UAS = [
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S926B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S921B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S908B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.85 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; 23116PN5BC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; 2211133C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.85 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; 22071219AI) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 9 Pro XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.85 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; OnePlus 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; OnePlus 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; OnePlus 10T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.85 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; HUAWEI P60 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; HUAWEI Mate 50 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; HUAWEI P40 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.86 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/134.0.6998.89 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/127.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 14; SM-A556B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.85 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-A236E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6834.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Redmi Note 12 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.90 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Redmi Note 13 Pro+) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Poco F5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.85 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Poco X6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.90 Mobile Safari/537.36",
]

# ─── Facebook Headers ───
FB_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,bn;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "TE": "trailers",
}


# ██████████████████████████████████████████████████████████████████████████████
# CORE TOOLS
# ██████████████████████████████████████████████████████████████████████████████

def load_list(filepath):
    """Load list from file"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return [l.strip() for l in f if l.strip()]
    except: return []

def append_to(filepath, text):
    """Append text to file"""
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(text + "\n")
        return True
    except: return False

def load_config():
    """Load config from file"""
    cfg_path = os.path.join(BASE_DIR, "config.json")
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path) as f:
                loaded = json.load(f)
                CONFIG.update(loaded)
        except: pass
    return CONFIG

def save_config():
    """Save config to file"""
    cfg_path = os.path.join(BASE_DIR, "config.json")
    try:
        with open(cfg_path, "w") as f:
            json.dump(CONFIG, f, indent=2)
        return True
    except: return False

def get_random_ua():
    """Get random user agent"""
    return random.choice(REAL_UAS)

def get_random_name():
    """Get random name based on country and gender"""
    country = CONFIG.get("country", "Bangladesh")
    gender = CONFIG.get("gender", "male")
    
    if CONFIG.get("custom_name"):
        return CONFIG["custom_name"]
    
    # Check if country has name DB
    country_data = NAMES_DB.get(country)
    if country_data:
        names = country_data.get(gender, NAMES_DB["Bangladesh"]["male"])
        return random.choice(names)
    else:
        # Use generic names
        if gender == "female":
            return random.choice(GENERIC_NAMES_FEMALE)
        else:
            return random.choice(GENERIC_NAMES_MALE)

def generate_password(length=12):
    """Generate strong random password"""
    if CONFIG.get("password"):
        return CONFIG["password"]
    
    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits
    special = "!@#$%&"
    
    # Ensure at least 1 of each
    pw = [
        random.choice(upper),
        random.choice(lower),
        random.choice(digits),
        random.choice(special),
    ]
    pw += random.choices(upper + lower + digits + special, k=length-4)
    random.shuffle(pw)
    return ''.join(pw)

def get_proxy_dict(proxies, index=[0]):
    """Get proxy dict"""
    if not CONFIG["use_proxy"] or not proxies: return None
    with threading.Lock():
        p = proxies[index[0] % len(proxies)]
        index[0] += 1
    if p.startswith("socks5"):
        return {"http": p.replace("socks5", "socks5h"), "https": p.replace("socks5", "socks5h")}
    return {"http": p, "https": p}

def create_session():
    """Create request session with retries"""
    session = requests.Session()
    session.verify = False
    retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry, pool_connections=20, pool_maxsize=20)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

# ██████████████████████████████████████████████████████████████████████████████
# TEMP MAIL SYSTEM
# ██████████████████████████████████████████████████████████████████████████████

def generate_temp_email():
    """Generate temporary email address"""
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(8, 14)))
    domain = random.choice(["@1secmail.com", "@1secmail.org", "@1secmail.net"])
    return f"{username}{domain}", username, domain.replace("@", "")

def check_temp_email_inbox(email, session):
    """Check temp email inbox for verification code"""
    try:
        username, domain = email.split("@")
        url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={username}&domain={domain}"
        r = session.get(url, timeout=10)
        if r.status_code == 200:
            messages = r.json()
            if messages:
                # Get latest message
                msg = messages[-1]
                msg_id = msg.get("id")
                # Get message content
                content_url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={username}&domain={domain}&id={msg_id}"
                cr = session.get(content_url, timeout=10)
                if cr.status_code == 200:
                    msg_data = cr.json()
                    body = msg_data.get("body", "")
                    html_body = msg_data.get("htmlBody", "")
                    
                    # Extract Facebook confirmation code
                    code = extract_confirmation_code(body + " " + html_body)
                    return code
        return None
    except: return None

def extract_confirmation_code(text):
    """Extract Facebook confirmation code from email body"""
    # Facebook code patterns
    patterns = [
        r'(\d{6})[^0-9]*$',           # 6 digit at end
        r'[Cc]ode[:\s]*(\d{6})',       # Code: XXXXXX
        r'FB-(\d{6})',                 # FB-XXXXXX
        r'(\d{6})\s*is\s*your',        # XXXXXX is your
        r'(\d{6})\s*FB',               # XXXXXX FB
        r'[Cc]onfirmation[:\s]*(\d{6})', # Confirmation: XXXXXX
        r'(\d{6})\s*expires',          # XXXXXX expires
        r'(\d{6})\s*minute',           # XXXXXX minute
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None


# ██████████████████████████████████████████████████████████████████████████████
# FACEBOOK ACCOUNT CREATOR
# ██████████████████████████████████████████████████████████████████████████████

def create_facebook_account(email, password, name, proxies, session):
    """Create a Facebook account and return result"""
    try:
        first_name = name.split()[0] if name.split() else name
        last_name = " ".join(name.split()[1:]) if len(name.split()) > 1 else random.choice(["Khan", "Ahmed", "Smith", "Hasan", "Ali", "Singh"])
        
        proxy = get_proxy_dict(proxies)
        ua = get_random_ua()
        
        headers = {**FB_HEADERS, "User-Agent": ua}
        
        # Step 1: Get initial page & cookies
        r1 = session.get("https://www.facebook.com/", headers=headers, proxies=proxy, timeout=CONFIG["timeout"])
        cookies = session.cookies.get_dict()
        
        # Extract fb_dtsg, jazoest, lsd
        fb_dtsg = ""
        jazoest = ""
        lsd = ""
        
        dtsg_match = re.search(r'name="fb_dtsg"[^>]+value="([^"]+)"', r1.text)
        if dtsg_match: fb_dtsg = dtsg_match.group(1)
        
        jazoest_match = re.search(r'name="jazoest"[^>]+value="([^"]+)"', r1.text)
        if jazoest_match: jazoest = jazoest_match.group(1)
        
        lsd_match = re.search(r'"LSD",\[\],{"token":"([^"]+)"', r1.text)
        if lsd_match: lsd = lsd_match.group(1)
        
        if not lsd:
            lsd_match = re.search(r'name="lsd"[^>]+value="([^"]+)"', r1.text)
            if lsd_match: lsd = lsd_match.group(1)
        
        action_url_match = re.search(r'action="([^"]*reg[^"]*)"', r1.text)
        action_url = action_url_match.group(1) if action_match else "https://www.facebook.com/reg/"

        # Step 2: Submit registration
        reg_data = {
            "lsd": lsd or "",
            "jazoest": jazoest or "",
            "fb_dtsg": fb_dtsg or "",
            "firstname": first_name,
            "lastname": last_name,
            "reg_email__": email,
            "reg_email_confirmation__": email,
            "reg_passwd__": password,
            "birthday_day": str(CONFIG["birth_day"]),
            "birthday_month": str(CONFIG["birth_month"]),
            "birthday_year": str(CONFIG["birth_year"]),
            "sex": "2" if CONFIG["gender"] == "male" else "1",
            "custom_gender": "",
            "did_use_age": "0",
            "locale": "en_US",
            "reg_instance": int(time.time()),
            "reg_impression_id": ''.join(random.choices(string.hexdigits, k=32)).lower(),
            "source": "reg_dialog",
            "referrer": "",
            "ref": "",
            "sk": "",
            "business": "",
            "meta_referrer": "https://www.facebook.com/",
        }
        
        reg_headers = {
            **headers,
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://www.facebook.com",
            "Referer": "https://www.facebook.com/",
        }
        
        r2 = session.post(action_url, data=reg_data, headers=reg_headers, proxies=proxy, timeout=CONFIG["timeout"])
        
        # Check if email confirmation needed
        if "confirm_email" in r2.url or "enter_code" in r2.url or "code" in r2.url.lower():
            # Wait for confirmation code
            max_wait = 120  # max 2 minutes
            wait_time = 0
            confirm_code = None
            
            while wait_time < max_wait:
                time.sleep(5)
                wait_time += 5
                confirm_code = check_temp_email_inbox(email, session)
                if confirm_code:
                    break
            
            if confirm_code:
                # Submit confirmation code
                confirm_data = {
                    "code": confirm_code,
                    "fb_dtsg": fb_dtsg or "",
                    "jazoest": jazoest or "",
                }
                conf_url = r2.url if "confirm" in r2.url else "https://www.facebook.com/confirmemail.php"
                r3 = session.post(conf_url, data=confirm_data, headers=reg_headers, proxies=proxy, timeout=CONFIG["timeout"])
                
                if "welcome" in r3.url.lower() or "home" in r3.url.lower() or r3.status_code == 200:
                    # Success!
                    account_details = {
                        "name": name,
                        "email": email,
                        "password": password,
                        "status": "CREATED",
                        "confirm_code": confirm_code,
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "account_id": extract_account_id(r3.text),
                        "cookies": dict(session.cookies.get_dict()),
                    }
                    return account_details
        
        # If no email needed or redirect to welcome/home
        if "welcome" in r2.url.lower() or "home" in r2.url.lower() or "checkpoint" not in r2.url:
            account_details = {
                "name": name,
                "email": email,
                "password": password,
                "status": "CREATED",
                "confirm_code": "AUTO",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "account_id": extract_account_id(r2.text),
                "cookies": dict(session.cookies.get_dict()),
            }
            return account_details
        
        # If we got here, something else happened
        return {
            "name": name,
            "email": email,
            "password": password,
            "status": "NEED_CONFIRM",
            "note": r2.url[:100],
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        
    except Exception as e:
        return {
            "name": name,
            "email": email,
            "password": password,
            "status": f"ERROR: {str(e)[:50]}",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }


def extract_account_id(html):
    """Extract Facebook account ID from response"""
    patterns = [
        r'"userID":"(\d+)"',
        r'"uid":"(\d+)"',
        r'profile_id":(\d+)',
        r'"account_id":"(\d+)"',
    ]
    for p in patterns:
        m = re.search(p, html)
        if m: return m.group(1)
    return "N/A"


# ██████████████████████████████████████████████████████████████████████████████
# WORKER
# ██████████████████████████████████████████████████████████████████████████████

def worker_process(queue, proxies, lock, stats):
    """Worker process for creating accounts"""
    session = create_session()
    
    while CONFIG["running"]:
        try:
            job = queue.get(timeout=2)
            if job is None: break
            
            idx, email, password, name = job
            
            with lock:
                CONFIG["created"] += 1
                stats["total"] += 1
                print(f"\n{C.C}[*] Creating #{stats['total']}: {name} | {email}{C.N}")
            
            result = create_facebook_account(email, password, name, proxies, session)
            
            with lock:
                if "CREATED" in result.get("status", ""):
                    CONFIG["success"] += 1
                    stats["success"] += 1
                    
                    # Save to file
                    method = CONFIG["method"]
                    save_path = os.path.join(ACCOUNTS_DIR, f"{method}_accounts.txt")
                    
                    with open(save_path, "a", encoding="utf-8") as f:
                        f.write(f"{'='*60}\n")
                        f.write(f"Account #: {stats['success']}\n")
                        f.write(f"Name     : {result.get('name', 'N/A')}\n")
                        f.write(f"Email    : {result.get('email', 'N/A')}\n")
                        f.write(f"Password : {result.get('password', 'N/A')}\n")
                        f.write(f"Status   : {result.get('status', 'N/A')}\n")
                        f.write(f"ID       : {result.get('account_id', 'N/A')}\n")
                        f.write(f"Country  : {CONFIG['country']}\n")
                        f.write(f"Gender   : {CONFIG['gender']}\n")
                        f.write(f"Birthday : {CONFIG['birth_day']}/{CONFIG['birth_month']}/{CONFIG['birth_year']}\n")
                        f.write(f"Method   : {method}\n")
                        f.write(f"Created  : {result.get('created_at', 'N/A')}\n")
                        f.write(f"Cookies  : {json.dumps(result.get('cookies', {}))}\n")
                        f.write(f"{'='*60}\n\n")
                    
                    print(f"{C.G}{C.BOLD}  ✓ CREATED #{stats['success']}: {name[:18]:18s} | {email[:20]:20s} | Pass: {password}{C.N}")
                    
                else:
                    CONFIG["failed"] += 1
                    stats["failed"] += 1
                    status = result.get("status", "UNKNOWN")
                    print(f"{C.R}  ✗ FAILED #{stats['total']}: {email[:20]:20s} | {status[:40]}{C.N}")
                    
                    # Save failed attempt
                    failed_path = os.path.join(ACCOUNTS_DIR, "failed_attempts.txt")
                    with open(failed_path, "a", encoding="utf-8") as f:
                        f.write(f"{email} | {password} | {name} | {status}\n")
            
            queue.task_done()
            time.sleep(CONFIG["delay"])
            
        except: continue


# ██████████████████████████████████████████████████████████████████████████████
# MAIN CREATOR
# ██████████████████████████████████████████████████████████████████████████████

def start_creator():
    """Main account creation function"""
    if CONFIG["running"]:
        print(f"{C.R}[!] Already running!{C.N}")
        return
    
    method = CONFIG["method"]
    count = CONFIG["count"]
    
    # Load proxy if enabled
    proxies = []
    if CONFIG["use_proxy"]:
        proxies = load_list(CONFIG["proxy_file"])
        if not proxies:
            print(f"{C.R}[!] No proxies found in {CONFIG['proxy_file']}{C.N}")
            print(f"{C.Y}[i] Continuing without proxy...{C.N}")
    
    accounts = []
    
    if method == "email":
        emails = load_list(CONFIG["email_file"])
        if not emails:
            print(f"{C.R}[!] No emails in {CONFIG['email_file']}!{C.N}")
            return
        if count > len(emails):
            print(f"{C.Y}[!] Only {len(emails)} emails available. Creating all.{C.N}")
            count = len(emails)
        for i in range(count):
            email = emails[i]
            pw = generate_password()
            name = get_random_name()
            accounts.append((email, pw, name))
    
    elif method == "phone":
        numbers = load_list(CONFIG["number_file"])
        if not numbers:
            print(f"{C.R}[!] No numbers in {CONFIG['number_file']}!{C.N}")
            return
        if count > len(numbers):
            print(f"{C.Y}[!] Only {len(numbers)} numbers available. Creating all.{C.N}")
            count = len(numbers)
        for i in range(count):
            number = numbers[i]
            pw = generate_password()
            name = get_random_name()
            accounts.append((number, pw, name))
    
    elif method == "automail":
        for i in range(count):
            email, _, _ = generate_temp_email()
            pw = generate_password()
            name = get_random_name()
            accounts.append((email, pw, name))
            
            # Save temp email for reuse
            append_to(CONFIG["temp_mail_file"], email)
    
    if not accounts:
        print(f"{C.R}[!] No accounts to create!{C.N}")
        return
    
    # ─── Start ───
    CONFIG["running"] = True
    CONFIG["created"] = 0
    CONFIG["success"] = 0
    CONFIG["failed"] = 0
    stats = {"total": 0, "success": 0, "failed": 0}
    lock = threading.Lock()
    
    job_queue = Queue()
    
    def producer():
        for i, (em, pw, nm) in enumerate(accounts):
            if not CONFIG["running"]: break
            job_queue.put((i+1, em, pw, nm))
            time.sleep(0.1)
    
    # ─── Display ───
    print(f"\n{C.C}╔══════════════════════════════════════════════════╗{C.N}")
    print(f"{C.C}║  {C.G}{C.BOLD}🚀 CREATING {count} FACEBOOK ACCOUNTS{C.C}              ║{C.N}")
    print(f"{C.C}╠══════════════════════════════════════════════════╣{C.N}")
    print(f"{C.C}║  Method  : {C.Y}{method.upper():<20}{C.C}               ║{C.N}")
    print(f"{C.C}║  Country : {C.Y}{CONFIG['country']:<20}{C.C}              ║{C.N}")
    print(f"{C.C}║  Gender  : {C.Y}{CONFIG['gender']:<20}{C.C}              ║{C.N}")
    print(f"{C.C}║  Threads : {C.Y}{CONFIG['threads']:<20}{C.C}              ║{C.N}")
    print(f"{C.C}║  Proxy   : {C.Y}{'ON' if CONFIG['use_proxy'] else 'OFF':<20}{C.C}              ║{C.N}")
    print(f"{C.C}║  Password: {C.Y}{CONFIG['password'] if CONFIG['password'] else 'AUTO':<20}{C.C}           ║{C.N}")
    print(f"{C.C}║  Output  : {C.Y}{ACCOUNTS_DIR}/{method}_accounts.txt{C.C}║{C.N}")
    print(f"{C.C}║  Press   : {C.R}[X]{C.C} in menu to STOP                 ║{C.N}")
    print(f"{C.C}╚══════════════════════════════════════════════════╝{C.N}")
    print()
    
    # ─── Start threads ───
    threads = []
    for _ in range(CONFIG["threads"]):
        t = threading.Thread(target=worker_process, args=(job_queue, proxies, lock, stats), daemon=True)
        t.start()
        threads.append(t)
    
    prod = threading.Thread(target=producer, daemon=True)
    prod.start()
    
    # ─── Live progress ───
    try:
        while CONFIG["running"] and stats["total"] < len(accounts):
            time.sleep(2)
            total = stats["total"]
            ok = stats["success"]
            fail = stats["failed"]
            
            progress = int((total / len(accounts)) * 20) if accounts else 0
            bar = f"{C.G}{'█'*progress}{C.D}{'░'*(20-progress)}{C.N}"
            
            print(f"\r{C.C}[{datetime.now().strftime('%H:%M:%S')}] {C.W}{total}/{len(accounts)}{C.N} {bar} {C.G}✓{ok}{C.N} {C.R}✗{fail}{C.N}   ", end="")
    except: pass
    
    # ─── Summary ───
    print(f"\n\n{C.C}{C.BOLD}╔══════════════════════════════════════════════╗{C.N}")
    print(f"{C.C}║  {C.G}{C.BOLD}✅ COMPLETED!{C.C}                                   ║{C.N}")
    print(f"{C.C}╠══════════════════════════════════════════════╣{C.N}")
    print(f"{C.C}║  Requested: {C.Y}{count}{C.C}  Created: {C.G}{stats['success']}{C.C}  Failed: {C.R}{stats['failed']}{C.C}   ║{C.N}")
    print(f"{C.C}║  Saved to : {C.Y}{ACCOUNTS_DIR}/{method}_accounts.txt{C.C}     ║{C.N}")
    print(f"{C.C}║  Password : {C.Y}{CONFIG['password'] if CONFIG['password'] else 'See account file'}{C.C}  ║{C.N}")
    print(f"{C.C}╚══════════════════════════════════════════════╝{C.N}")
    
    CONFIG["running"] = False


# ██████████████████████████████████████████████████████████████████████████████
# UI
# ██████████████████████████████████████████████████████████████████████████████

def show_banner():
    """Display awesome banner"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{C.R}
  ███████╗███████╗ █████╗  ██████╗███████╗██████╗  ██████╗  █████╗ 
  ██╔════╝██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔══██╗██╔══██╗
  █████╗  █████╗  ███████║██║     █████╗  ██████╔╝██████╔╝███████║
  ██╔══╝  ██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗██╔══██╗██╔══██║
  ██║     ███████╗██║  ██║╚██████╗███████╗██║  ██║██████╔╝██║  ██║
  ╚═╝     ╚══════╝╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝╚═════╝ ╚═╝  ╚═╝
{C.M}
   █████╗ ██████╗  ██████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗
  ██╔══██╗██╔══██╗██╔════╝ ██╔══██╗██║   ██║████╗  ██║╚══██╔══╝
  ███████║██████╔╝██║  ███╗██████╔╝██║   ██║██╔██╗ ██║   ██║   
  ██╔══██║██╔══██╗██║   ██║██╔══██╗██║   ██║██║╚██╗██║   ██║   
  ██║  ██║██████╔╝╚██████╔╝██║  ██║╚██████╔╝██║ ╚████║   ██║   
  ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   {C.C}
  ════════════════════════════════════════════════════════════════════
      FACEBOOK AUTO ACCOUNT CREATOR v2.0 — PRO EDITION
        Email | Phone | Auto-Mail | Temp Mail | Cookie Jar
                  Authorized Security Testing Tool
  ════════════════════════════════════════════════════════════════════{C.N}
    """)

def show_status():
    """Show current configuration"""
    method = CONFIG["method"].upper()
    method_icons = {"EMAIL": "📧", "PHONE": "📱", "AUTOMAIL": "⚡"}
    icon = method_icons.get(method, "📧")
    
    print(f"{C.C}╔══════════════════ CONFIGURATION ══════════════════╗{C.N}")
    print(f"{C.C}║{C.N}")
    print(f"{C.C}║  {C.Y}METHOD  :{C.N} {icon} {method:15s}     {C.Y}COUNT :{C.N} {CONFIG['count']:<5}{C.C}         ║{C.N}")
    print(f"{C.C}║  {C.Y}COUNTRY :{C.N} {CONFIG['country']:18s} {C.Y}THREADS:{C.N} {CONFIG['threads']:<5}{C.C}         ║{C.N}")
    print(f"{C.C}║  {C.Y}GENDER  :{C.N} {CONFIG['gender']:18s} {C.Y}DELAY  :{C.N} {CONFIG['delay']}s{C.C}          ║{C.N}")
    print(f"{C.C}║  {C.Y}BIRTHDAY:{C.N} {CONFIG['birth_day']}/{CONFIG['birth_month']}/{CONFIG['birth_year']:12s}{C.C}     ║{C.N}")
    print(f"{C.C}║  {C.Y}NAME    :{C.N} {CONFIG['custom_name'] if CONFIG['custom_name'] else 'Auto by Country':20s}{C.C}     ║{C.N}")
    print(f"{C.C}║  {C.Y}PASSWORD:{C.N} {CONFIG['password'] if CONFIG['password'] else 'Auto-Generated':18s}{C.C}     ║{C.N}")
    print(f"{C.C}║  {C.Y}PROXY   :{C.N} {'ON' if CONFIG['use_proxy'] else 'OFF':20s}{C.C}              ║{C.N}")
    
    if CONFIG["success"] > 0:
        print(f"{C.C}║  {C.Y}STATS   :{C.N} {C.G}✓ Created: {CONFIG['success']}{C.N}  {C.R}✗ Failed: {CONFIG['failed']}{C.N}  Total: {CONFIG['created']}{C.C}   ║{C.N}")
    
    print(f"{C.C}║{C.N}")
    print(f"{C.C}╚══════════════════════════════════════════════════╝{C.N}")

def show_menu():
    """Display interactive menu"""
    print(f"""{C.Y}╔═══════════════════ MENU ═══════════════════╗
║                                        ║
║  {C.C}[{C.G}1{C.C}] {C.W}Method: Email (your emails){C.Y}               ║
║  {C.C}[{C.G}2{C.C}] {C.W}Method: Phone (your numbers){C.Y}              ║
║  {C.C}[{C.G}3{C.C}] {C.W}Method: Auto Mail (temp mail){C.Y}             ║
║  {C.C}[{C.G}4{C.C}] {C.W}How many accounts?{C.Y}                       ║
║  {C.C}[{C.G}5{C.C}] {C.W}Threads & Delay{C.Y}                          ║
║  {C.C}[{C.G}6{C.C}] {C.W}Set Country{C.Y}                              ║
║  {C.C}[{C.G}7{C.C}] {C.W}Set Gender (Male/Female){C.Y}                 ║
║  {C.C}[{C.G}8{C.C}] {C.W}Set Password (or leave blank for auto){C.Y}   ║
║  {C.C}[{C.G}9{C.C}] {C.W}Set Birthday{C.Y}                             ║
║  {C.C}[{C.G}10{C.C}]{C.W} Set Custom Name (optional){C.Y}              ║
║  {C.C}[{C.G}11{C.C}]{C.W} Toggle Proxy ON/OFF{C.Y}                     ║
║  {C.C}[{C.G}12{C.C}]{C.W} Add Email to List{C.Y}                       ║
║  {C.C}[{C.G}13{C.C}]{C.W} Add Number to List{C.Y}                      ║
║  {C.C}[{C.G}14{C.C}]{C.W} View Saved Accounts{C.Y}                     ║
║                                        ║
║  {C.G}{C.BOLD}[S] ▶ START CREATING{C.Y}                                ║
║  {C.R}{C.BOLD}[X] ■ STOP{C.Y}                                           ║
║                                        ║
║  {C.W}[0] Exit{C.Y}                                                     ║
╚════════════════════════════════════════╝
    """)


# ██████████████████████████████████████████████████████████████████████████████
# HANDLERS
# ██████████████████████████████████████████████████████████████████████████████

def handle_set_method(m):
    CONFIG["method"] = m
    save_config()
    print(f"{C.G}[✓] Method: {m.upper()}{C.N}")

def handle_set_count():
    try:
        c = int(input(f"{C.G}How many accounts?: {C.N}"))
        CONFIG["count"] = max(1, c)
        save_config()
        print(f"{C.G}[✓] Will create {CONFIG['count']} accounts{C.N}")
    except: print(f"{C.R}[!] Invalid{C.N}")

def handle_set_threads():
    try:
        t = input(f"{C.G}Threads [{CONFIG['threads']}]: {C.N}").strip()
        if t: CONFIG["threads"] = max(1, min(20, int(t)))
        d = input(f"{C.G}Delay (seconds) [{CONFIG['delay']}]: {C.N}").strip()
        if d: CONFIG["delay"] = max(0.5, float(d))
        save_config()
        print(f"{C.G}[✓] Threads: {CONFIG['threads']}, Delay: {CONFIG['delay']}s{C.N}")
    except: print(f"{C.R}[!] Invalid{C.N}")

def handle_set_country():
    codes = list(COUNTRIES.keys())
    print(f"\n{C.C}── COUNTRIES ──{C.N}")
    for i, code in enumerate(codes, 1):
        country = COUNTRIES[code]
        print(f"  {i:2d}. {country['name']:20s} ({country['code']})")
    try:
        idx = int(input(f"\n{C.G}Choose (1-{len(codes)}): {C.N}")) - 1
        if 0 <= idx < len(codes):
            CONFIG["country"] = COUNTRIES[codes[idx]]["name"]
            save_config()
            print(f"{C.G}[✓] Country: {CONFIG['country']}{C.N}")
    except: print(f"{C.R}[!] Invalid{C.N}")

def handle_set_gender():
    g = input(f"{C.G}Gender (male/female) [{CONFIG['gender']}]: {C.N}").strip().lower()
    if g in ("male", "female"):
        CONFIG["gender"] = g
        save_config()
        print(f"{C.G}[✓] Gender: {CONFIG['gender']}{C.N}")

def handle_set_password():
    p = input(f"{C.G}Password (or 'auto' for random): {C.N}").strip()
    if p.lower() == "auto":
        CONFIG["password"] = ""
        print(f"{C.Y}[✓] Auto password mode{C.N}")
    elif p:
        CONFIG["password"] = p
        print(f"{C.G}[✓] Password: {p}{C.N}")
    save_config()

def handle_set_birthday():
    try:
        d = int(input(f"{C.G}Day (1-31) [{CONFIG['birth_day']}]: {C.N}") or CONFIG['birth_day'])
        m = int(input(f"{C.G}Month (1-12) [{CONFIG['birth_month']}]: {C.N}") or CONFIG['birth_month'])
        y = int(input(f"{C.G}Year [{CONFIG['birth_year']}]: {C.N}") or CONFIG['birth_year'])
        CONFIG["birth_day"] = max(1, min(31, d))
        CONFIG["birth_month"] = max(1, min(12, m))
        CONFIG["birth_year"] = max(1950, min(2005, y))
        save_config()
        print(f"{C.G}[✓] Birthday: {CONFIG['birth_day']}/{CONFIG['birth_month']}/{CONFIG['birth_year']}{C.N}")
    except: print(f"{C.R}[!] Invalid{C.N}")

def handle_set_name():
    n = input(f"{C.G}Custom name (or 'auto' for random): {C.N}").strip()
    if n.lower() == "auto":
        CONFIG["custom_name"] = ""
        print(f"{C.Y}[✓] Auto name mode{C.N}")
    elif n:
        CONFIG["custom_name"] = n
        print(f"{C.G}[✓] Name: {n}{C.N}")
    save_config()

def handle_toggle_proxy():
    CONFIG["use_proxy"] = not CONFIG["use_proxy"]
    save_config()
    print(f"{C.G}[✓] Proxy: {'ON' if CONFIG['use_proxy'] else 'OFF'}{C.N}")

def handle_add_email():
    e = input(f"{C.G}Enter email: {C.N}").strip()
    if e and '@' in e:
        append_to(CONFIG["email_file"], e)
        print(f"{C.G}[✓] Added: {e}{C.N}")

def handle_add_number():
    n = input(f"{C.G}Enter number (with country code): {C.N}").strip()
    if n:
        append_to(CONFIG["number_file"], n)
        print(f"{C.G}[✓] Added: {n}{C.N}")

def handle_view_accounts():
    files = os.listdir(ACCOUNTS_DIR)
    if not files:
        print(f"{C.Y}[!] No accounts saved yet.{C.N}")
        return
    print(f"\n{C.C}── Files in {ACCOUNTS_DIR}/ ──{C.N}")
    for f in files:
        fpath = os.path.join(ACCOUNTS_DIR, f)
        size = os.path.getsize(fpath)
        if size > 0:
            with open(fpath) as fh:
                lines = fh.read().strip().split('\n')
            count = lines.count('='*60)
            print(f"  {C.G}{f}{C.N} ({count} accounts, {size} bytes)")
        else:
            print(f"  {C.D}{f} (empty){C.N}")


# ██████████████████████████████████████████████████████████████████████████████
# MAIN
# ██████████████████████████████████████████████████████████████████████████████

def main():
    load_config()
    
    # Ensure data files
    for f in [CONFIG["email_file"], CONFIG["number_file"], CONFIG["proxy_file"], CONFIG["temp_mail_file"]]:
        fpath = os.path.join(BASE_DIR, f)
        if not os.path.exists(fpath): open(fpath, "a").close()
    
    while True:
        show_banner()
        show_status()
        show_menu()
        
        ch = input(f"\n{C.G}{C.BOLD}╰─➤  Choice: {C.N}").strip().lower()
        
        if ch == "1": handle_set_method("email")
        elif ch == "2": handle_set_method("phone")
        elif ch == "3": handle_set_method("automail")
        elif ch == "4": handle_set_count()
        elif ch == "5": handle_set_threads()
        elif ch == "6": handle_set_country()
        elif ch == "7": handle_set_gender()
        elif ch == "8": handle_set_password()
        elif ch == "9": handle_set_birthday()
        elif ch == "10": handle_set_name()
        elif ch == "11": handle_toggle_proxy()
        elif ch == "12": handle_add_email()
        elif ch == "13": handle_add_number()
        elif ch == "14": handle_view_accounts()
        elif ch == "s":
            start_creator()
        elif ch == "x":
            CONFIG["running"] = False
            print(f"\n{C.R}■ STOPPED{C.N}")
            time.sleep(1)
        elif ch == "0":
            CONFIG["running"] = False
            print(f"\n{C.Y}Exiting...{C.N}")
            time.sleep(0.5)
            sys.exit(0)
        else:
            print(f"{C.R}[!] Invalid{C.N}")
        
        if ch not in ("s", "x"):
            input(f"\n{C.Y}Press Enter...{C.N}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        CONFIG["running"] = False
        print(f"\n\n{C.R}Exiting...{C.N}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{C.R}Critical Error: {e}{C.N}")
        sys.exit(1)
