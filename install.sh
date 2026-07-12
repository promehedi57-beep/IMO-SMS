#!/usr/bin/env bash
#
# Zero EMU SMS Sender — Auto Installer
# Install all dependencies and setup sample files
#

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${CYAN}${BOLD}  ╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}  ║                                                    ║${NC}"
echo -e "${CYAN}${BOLD}  ║     ZERO EMU SMS SENDER — AUTO INSTALLER v3.0       ║${NC}"
echo -e "${CYAN}${BOLD}  ║                                                    ║${NC}"
echo -e "${CYAN}${BOLD}  ╚══════════════════════════════════════════════════════╝${NC}"
echo ""

# ────────────────────────────────────────────
# Step 1: System Update
# ────────────────────────────────────────────
echo -e "${YELLOW}[1/5] Checking system packages...${NC}"
if command -v apt &>/dev/null; then
    sudo apt update -qq 2>/dev/null || true
    echo -e "${GREEN}  [✓] System packages updated${NC}"
else
    echo -e "${YELLOW}  [!] apt not found, skipping system update${NC}"
fi

# ────────────────────────────────────────────
# Step 2: Check Python
# ────────────────────────────────────────────
echo -e "${YELLOW}[2/5] Checking Python 3...${NC}"
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo -e "${GREEN}  [✓] $PYTHON_VERSION${NC}"
else
    echo -e "${RED}  [!] Python3 not found! Installing...${NC}"
    if command -v apt &>/dev/null; then
        sudo apt install -y python3 python3-pip -qq
        echo -e "${GREEN}  [✓] Python3 installed${NC}"
    else
        echo -e "${RED}  [!] Please install Python 3.8+ manually${NC}"
        exit 1
    fi
fi

# ────────────────────────────────────────────
# Step 3: Install Python Packages
# ────────────────────────────────────────────
echo -e "${YELLOW}[3/5] Installing Python packages...${NC}"
pip3 install requests colorama urllib3 --break-system-packages -q 2>/dev/null || \
pip3 install requests colorama urllib3 -q 2>/dev/null || {
    echo -e "${RED}  [!] Failed to install packages. Trying with pip...${NC}"
    pip install requests colorama urllib3 -q
}
echo -e "${GREEN}  [✓] Python packages installed (requests, colorama)${NC}"

# ────────────────────────────────────────────
# Step 4: Create Sample Files
# ────────────────────────────────────────────
echo -e "${YELLOW}[4/5] Setting up configuration files...${NC}"

# numbers.txt
if [ ! -f "numbers.txt" ]; then
    cat > numbers.txt << 'NUMEOF'
+8801712345670
+8801712345671
+8801712345672
+8801712345673
+8801712345674
+8801712345675
NUMEOF
    echo -e "${GREEN}  [✓] Created: numbers.txt${NC}"
else
    echo -e "${CYAN}  [⋅] Exists: numbers.txt${NC}"
fi

# proxies.txt
if [ ! -f "proxies.txt" ]; then
    cat > proxies.txt << 'PROXEOF'
http://8.219.97.248:80
http://20.205.61.143:80
http://45.77.26.123:3128
http://103.152.112.178:80
http://188.166.56.189:8080
PROXEOF
    echo -e "${GREEN}  [✓] Created: proxies.txt${NC}"
else
    echo -e "${CYAN}  [⋅] Exists: proxies.txt${NC}"
fi

# user_agents.txt
if [ ! -f "user_agents.txt" ]; then
    cat > user_agents.txt << 'UAEOF'
Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1
Mozilla/5.0 (Linux; Android 15; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/134.0.6998.89 Mobile/15E148 Safari/604.1
Mozilla/5.0 (Linux; Android 14; Pixel 9 Pro XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.90 Mobile Safari/537.36
Mozilla/5.0 (iPad; CPU OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Mobile/15E148 Safari/604.1
UAEOF
    echo -e "${GREEN}  [✓] Created: user_agents.txt${NC}"
else
    echo -e "${CYAN}  [⋅] Exists: user_agents.txt${NC}"
fi

# ────────────────────────────────────────────
# Step 5: Final Setup
# ────────────────────────────────────────────
echo -e "${YELLOW}[5/5] Finalizing...${NC}"

# Make scripts executable
if [ -f "zero_bot.py" ]; then
    chmod +x zero_bot.py
    echo -e "${GREEN}  [✓] zero_bot.py is executable${NC}"
fi
if [ -f "run.sh" ]; then
    chmod +x run.sh
    echo -e "${GREEN}  [✓] run.sh is executable${NC}"
fi

# Create directories
mkdir -p logs
touch bad_proxies.txt

# Create config.json if not exists
if [ ! -f "config.json" ]; then
    cat > config.json << 'CONFIGEOF'
{
    "_note": "Zero EMU SMS Sender Configuration",
    "threads": 50,
    "delay": 0.2,
    "timeout": 8,
    "max_retries": 2,
    "rotate_proxy": true,
    "rotate_ua": true,
    "rotate_mode": "random",
    "country_switch": false,
    "country_codes": ["+880"],
    "numbers_file": "numbers.txt",
    "proxies_file": "proxies.txt",
    "ua_file": "user_agents.txt",
    "api_endpoints": [],
    "api_payloads": [],
    "log_requests": true,
    "auto_retry_on_fail": true
}
CONFIGEOF
    echo -e "${GREEN}  [✓] Created: config.json${NC}"
fi

# ────────────────────────────────────────────
# Complete!
# ────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}  ╔══════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}  ║                INSTALLATION COMPLETE!                ║${NC}"
echo -e "${GREEN}${BOLD}  ╚══════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}  ─────────────────────────────────────────────${NC}"
echo -e "${CYAN}   লঞ্চ করতে নিচের কমান্ড দিন:${NC}"
echo -e "${YELLOW}    python3 zero_bot.py${NC}"
echo -e "${CYAN}   অথবা${NC}"
echo -e "${YELLOW}    bash run.sh${NC}"
echo -e "${CYAN}  ─────────────────────────────────────────────${NC}"
echo ""
