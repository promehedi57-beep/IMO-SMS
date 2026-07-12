#!/usr/bin/env bash
#
# Zero EMU SMS Sender — One Command Launcher
# Usage: bash run.sh
# This will install dependencies (first run) and launch the tool
#

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${CYAN}${BOLD}  ╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}  ║                                                    ║${NC}"
echo -e "${CYAN}${BOLD}  ║        ZERO EMU SMS SENDER — AUTO LAUNCHER          ║${NC}"
echo -e "${CYAN}${BOLD}  ║              v3.0 — Gold Edition                    ║${NC}"
echo -e "${CYAN}${BOLD}  ║                                                    ║${NC}"
echo -e "${CYAN}${BOLD}  ╚══════════════════════════════════════════════════════╝${NC}"
echo ""

# ── Check main script exists ──
if [ ! -f "zero_bot.py" ]; then
    echo -e "${RED}  [!] zero_bot.py not found!${NC}"
    echo -e "${YELLOW}  নিশ্চিত করুন আপনি সঠিক ডিরেক্টরিতে আছেন:${NC}"
    echo -e "${YELLOW}    cd IMO-SMS${NC}"
    exit 1
fi

# ── First run check ──
if [ ! -f "numbers.txt" ] || [ ! -f "proxies.txt" ] || [ ! -f "config.json" ]; then
    echo -e "${YELLOW}  [*] প্রথমবার — ইনস্টলার রান হচ্ছে...${NC}"
    echo ""
    
    if [ -f "install.sh" ]; then
        bash install.sh
    else
        echo -e "${YELLOW}  [*] install.sh নেই — বেসিক ফাইল তৈরি হচ্ছে...${NC}"
        
        # Create minimal files
        [ ! -f "numbers.txt" ] && echo "+8801712345670" > numbers.txt && echo -e "${GREEN}  [+] numbers.txt তৈরি${NC}"
        [ ! -f "proxies.txt" ] && echo "http://8.219.97.248:80" > proxies.txt && echo -e "${GREEN}  [+] proxies.txt তৈরি${NC}"
        mkdir -p logs
        touch bad_proxies.txt
    fi
    
    echo ""
fi

# ── Check dependencies ──
echo -e "${YELLOW}  [*] ডিপেন্ডেন্সি চেক করা হচ্ছে...${NC}"
python3 -c "import requests; import colorama" 2>/dev/null || {
    echo -e "${YELLOW}  [!] ডিপেন্ডেন্সি নেই — ইন্সটল করা হচ্ছে...${NC}"
    pip3 install requests colorama --break-system-packages -q 2>/dev/null || \
    pip3 install requests colorama -q 2>/dev/null || \
    pip install requests colorama -q
    echo -e "${GREEN}  [✓] ডিপেন্ডেন্সি ইন্সটল করা হয়েছে${NC}"
}
echo -e "${GREEN}  [✓] ডিপেন্ডেন্সি ঠিক আছে${NC}"
echo ""

# ── Launch ──
echo -e "${GREEN}${BOLD}  [✓] Zero EMU SMS Sender লঞ্চ হচ্ছে...${NC}"
sleep 0.5
python3 zero_bot.py

# ── If script exits, show message ──
echo ""
echo -e "${YELLOW}  টুল বন্ধ হয়েছে। আবার রান করতে: bash run.sh${NC}"
echo ""
