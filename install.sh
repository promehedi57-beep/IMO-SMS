#!/data/data/com.termux/files/usr/bin/env bash
#
# Zero EMU SMS Sender — Termux Auto Installer
#

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

echo ""
echo -e "${CYAN}${BOLD}  ╔══════════════════════════════════════════╗${NC}"
echo -e "${CYAN}${BOLD}  ║   Zero EMU SMS Sender — TERMUX INSTALL  ║${NC}"
echo -e "${CYAN}${BOLD}  ╚══════════════════════════════════════════╝${NC}"
echo ""

echo -e "${YELLOW}[1/3] Checking Python...${NC}"
if command -v python3 &>/dev/null; then
    echo -e "${GREEN}  [✓] Python: $(python3 --version)${NC}"
else
    echo -e "${YELLOW}  Installing Python...${NC}"
    pkg install -y python
fi

echo -e "${YELLOW}[2/3] Installing requests...${NC}"
pip install requests --quiet 2>/dev/null || {
    pip install requests 2>/dev/null
}
echo -e "${GREEN}  [✓] requests installed${NC}"

echo -e "${YELLOW}[3/3] Setting up files...${NC}"
mkdir -p logs
touch bad_proxies.txt

if [ ! -f "numbers.txt" ]; then
    cat > numbers.txt << 'EOF'
+8801712345670
+8801712345671
+8801712345672
EOF
    echo -e "${GREEN}  [+] Created numbers.txt${NC}"
fi

if [ ! -f "proxies.txt" ]; then
    cat > proxies.txt << 'EOF'
http://8.219.97.248:80
http://20.205.61.143:80
EOF
    echo -e "${GREEN}  [+] Created proxies.txt${NC}"
fi

chmod +x zero_bot.py 2>/dev/null
chmod +x run.sh 2>/dev/null

echo ""
echo -e "${GREEN}${BOLD}  ✅ INSTALL COMPLETE!${NC}"
echo -e "${CYAN}  Run: python3 zero_bot.py${NC}"
echo ""
