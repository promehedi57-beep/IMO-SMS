#!/bin/bash
echo "Installing dependencies..."
sudo apt update -qq
sudo apt install -y python3 python3-pip curl wget -qq
pip3 install rich requests colorama --break-system-packages -q
echo "Done! Run: python3 zero_bot.py"
