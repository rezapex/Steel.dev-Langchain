#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Setting up Steel LangChain development environment...${NC}"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo -e "${BLUE}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${BLUE}Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip and install setuptools
echo -e "${BLUE}Upgrading pip and installing setuptools...${NC}"
pip install --upgrade pip setuptools wheel

# Install dependencies
echo -e "${BLUE}Installing dependencies...${NC}"
pip install -e .

# Install development dependencies (optional)
read -p "Do you want to install development dependencies? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}Installing development dependencies...${NC}"
    pip install -e ".[dev]"
fi

# Install Playwright browsers
echo -e "${BLUE}Installing Playwright browsers...${NC}"
playwright install

echo -e "${GREEN}Setup complete!${NC}"

# Run environment check
echo -e "${BLUE}Checking environment setup...${NC}"
python check_env.py

echo -e "\nTo activate the virtual environment in the future, run:"
echo -e "${BLUE}source venv/bin/activate${NC}"
