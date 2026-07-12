#!/usr/bin/env bash
#
# Zero EMU SMS Sender — Auto Installer
#

set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${CYAN}${BOLD}  ╔══════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}  ║   Zero EMU SMS Sender — INSTALLER       ║${NC}"
echo -e "${CYAN}${BOLD}  ╚══════════════════════════════════════════╝${NC}"
echo ""

# Step 1: System
echo -e "${YELLOW}[1/5] Updating system packages...${NC}"
sudo apt update -qq || echo -e "${YELLOW}  [!] Skipping apt (not root or no apt)${NC}"

# Step 2: Python
echo -e "${YELLOW}[2/5] Checking Python...${NC}"
if command -v python3 &>/dev/null; then
    echo -e "${GREEN}  [✓] Python $(python3 --version)${NC}"
else
    echo -e "${YELLOW}  Installing Python...${NC}"
    sudo apt install -y python3 python3-pip -qq || {
        echo -e "${RED}  [!] Please install Python 3 manually${NC}"
        exit 1
    }
fi

# Step 3: Dependencies
echo -e "${YELLOW}[3/5] Installing Python packages...${NC}"
pip3 install requests colorama urllib3 --break-system-packages -q || \
pip3 install requests colorama urllib3 -q
echo -e "${GREEN}  [✓] Dependencies installed${NC}"

# Step 4: Sample files
echo -e "${YELLOW}[4/5] Setting up sample files...${NC}"

if [ ! -f "numbers.txt" ]; then
    cat > numbers.txt << 'EOF'
+8801712345670
+8801712345671
+8801712345672
+8801712345673
+8801712345674
+8801712345675
EOF
    echo -e "${GREEN}  [+] Created numbers.txt (6 samples)${NC}"
fi

if [ ! -f "proxies.txt" ]; then
    cat > proxies.txt << 'EOF'
http://8.219.97.248:80
http://20.205.61.143:80
http://45.77.26.123:3128
http://103.152.112.178:80
http://188.166.56.189:8080
EOF
    echo -e "${GREEN}  [+] Created proxies.txt (5 samples)${NC}"
fi

if [ ! -f "user_agents.txt" ]; then
    cat > user_agents.txt << 'EOF'
Mozilla/5.0 (iPhone; CPU iPhone OS 18_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.5 Mobile/15E148 Safari/604.1
Mozilla/5.0 (Linux; Android 15; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.7049.84 Mobile Safari/537.36
Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/134.0.6998.89 Mobile/15E148 Safari/604.1
Mozilla/5.0 (Linux; Android 14; Pixel 9 Pro XL) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.90 Mobile Safari/537.36
Mozilla/5.0 (iPad; CPU OS 18_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Mobile/15E148 Safari/604.1
Mozilla/5.0 (Linux; Android 13; 2211133C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.85 Mobile Safari/537.36
EOF
    echo -e "${GREEN}  [+] Created user_agents.txt (6 samples)${NC}"
fi

# Step 5: Make scripts executable
echo -e "${YELLOW}[5/5] Finalizing...${NC}"
if [ -f "zero_bot.py" ]; then
    chmod +x zero_bot.py
    echo -e "${GREEN}  [✓] zero_bot.py ready${NC}"
fi
if [ -f "run.sh" ]; then
    chmod +x run.sh
    echo -e "${GREEN}  [✓] run.sh ready${NC}"
fi

# Create logs dir
mkdir -p logs
touch bad_proxies.txt

echo ""
echo -e "${GREEN}${BOLD}  ╔══════════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}  ║   INSTALLATION COMPLETE!                ║${NC}"
echo -e "${GREEN}${BOLD}  ╚══════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}  Run: ${YELLOW}python3 zero_bot.py${NC}"
echo -e "${CYAN}  Or:  ${YELLOW}bash run.sh${NC}"
echo ""
