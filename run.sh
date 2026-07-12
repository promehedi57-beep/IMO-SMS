#!/usr/bin/env bash
#
# Zero EMU SMS Sender — One Command Launcher
# Usage: bash run.sh
#

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo -e "${CYAN}  ╔══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}  ║  Zero EMU SMS Sender v3.0 — Auto Launcher  ║${NC}"
echo -e "${CYAN}  ╚══════════════════════════════════════════════╝${NC}"
echo ""

# Check main script
if [ ! -f "zero_bot.py" ]; then
    echo -e "${RED}  [!] zero_bot.py not found!${NC}"
    echo -e "${YELLOW}  Make sure you're in the right directory.${NC}"
    echo -e "${YELLOW}  Run: git clone https://github.com/promehedi57-beep/IMO-SMS.git && cd IMO-SMS${NC}"
    exit 1
fi

# First run? Run installer
if [ ! -f "numbers.txt" ] || [ ! -f "proxies.txt" ]; then
    echo -e "${YELLOW}  [*] First run detected — running installer...${NC}"
    if [ -f "install.sh" ]; then
        bash install.sh
    else
        echo -e "${YELLOW}  [*] Creating sample files...${NC}"
        # Create basic files
        cat > numbers.txt << 'EOF'
+8801712345670
+8801712345671
+8801712345672
EOF
        echo -e "${GREEN}  [+] Created numbers.txt${NC}"
        
        cat > proxies.txt << 'EOF'
http://8.219.97.248:80
http://20.205.61.143:80
EOF
        echo -e "${GREEN}  [+] Created proxies.txt${NC}"
    fi
    echo ""
fi

# Check dependencies
python3 -c "import requests; import colorama" 2>/dev/null || {
    echo -e "${YELLOW}  [*] Installing dependencies...${NC}"
    pip3 install requests colorama --break-system-packages -q 2>/dev/null || \
    pip3 install requests colorama -q
    echo -e "${GREEN}  [✓] Dependencies installed${NC}"
}

# Launch
echo -e "${GREEN}  [✓] Launching Zero EMU SMS Sender...${NC}"
sleep 0.5
python3 zero_bot.py
