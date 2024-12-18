#!/usr/bin/env python3
"""Environment checker for Steel LangChain setup."""
import os
from dotenv import load_dotenv

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

def check_environment():
    """Check if all required environment variables are set."""
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    # Required environment variables
    required_vars = {
        "OPENAI_API_KEY": "Required for LangChain agents",
        "STEEL_API_KEY": "Required for Steel browser automation"
    }
    
    # Check each variable
    all_good = True
    print(f"\n{BOLD}Checking environment setup...{RESET}\n")
    
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            print(f"{GREEN}✓{RESET} {var} is set - {description}")
        else:
            all_good = False
            print(f"{RED}✗{RESET} {var} is not set - {description}")
    
    # Print summary and instructions
    print("\n" + "="*50)
    if all_good:
        print(f"{GREEN}{BOLD}Environment is properly configured!{RESET}")
        print("\nYou can now run the shopping agent:")
        print("python agents/shopping_agent.py")
    else:
        print(f"{RED}{BOLD}Missing required environment variables!{RESET}")
        print("\nPlease set up your environment variables in one of these ways:")
        print("\n1. Create a .env file in the project root with:")
        print("STEEL_API_KEY=your_steel_api_key_here")
        print("OPENAI_API_KEY=your_openai_api_key_here")
        print("\n2. Or set them in your shell:")
        print("export STEEL_API_KEY=your_steel_api_key_here")
        print("export OPENAI_API_KEY=your_openai_api_key_here")
    print("="*50 + "\n")

if __name__ == "__main__":
    check_environment()
