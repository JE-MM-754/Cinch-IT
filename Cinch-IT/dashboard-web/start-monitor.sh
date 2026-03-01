#!/bin/bash
# OpenClaw Process Monitor - Quick Start Script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 OpenClaw Process Monitor${NC}"
echo "=============================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

# Check if OpenClaw is available
if ! command -v openclaw &> /dev/null; then
    echo -e "${RED}❌ OpenClaw is not installed or not in PATH${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"
echo ""

# Show menu
echo "Choose monitor mode:"
echo "1) 📊 Terminal Dashboard (interactive)"
echo "2) 🌐 Web Dashboard (browser-based)"  
echo "3) 📋 JSON Export (one-time)"
echo "4) 👀 Terminal View (one-time)"
echo ""

read -p "Enter choice (1-4): " choice

case $choice in
    1)
        echo -e "${BLUE}🖥️  Starting Terminal Dashboard...${NC}"
        echo "Press Ctrl+C to exit"
        echo ""
        python3 "$SCRIPT_DIR/monitor.py" --mode terminal
        ;;
    2)
        echo -e "${BLUE}🌐 Starting Web Server...${NC}"
        echo ""
        
        # Check if port is specified
        read -p "Port (default 8080): " port
        port=${port:-8080}
        
        echo -e "${GREEN}Dashboard will be available at: http://localhost:$port${NC}"
        echo -e "${GREEN}API endpoint: http://localhost:$port/api/data${NC}"
        echo -e "${YELLOW}Press Ctrl+C to stop${NC}"
        echo ""
        
        python3 "$SCRIPT_DIR/web-server.py" --port "$port"
        ;;
    3)
        echo -e "${BLUE}📋 Generating JSON Export...${NC}"
        
        # Generate filename with timestamp
        timestamp=$(date +"%Y%m%d-%H%M%S")
        filename="openclaw-monitor-$timestamp.json"
        
        python3 "$SCRIPT_DIR/monitor.py" --mode json --export "$filename"
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✅ Export saved to: $filename${NC}"
        else
            echo -e "${RED}❌ Export failed${NC}"
        fi
        ;;
    4)
        echo -e "${BLUE}👀 Current Status:${NC}"
        echo ""
        python3 "$SCRIPT_DIR/monitor.py" --once
        ;;
    *)
        echo -e "${RED}Invalid choice${NC}"
        exit 1
        ;;
esac