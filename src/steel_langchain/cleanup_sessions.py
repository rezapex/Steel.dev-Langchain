"""Script to cleanup all active Steel sessions."""
import os
from dotenv import load_dotenv
from steel import Steel

def main():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    steel_api_key = os.getenv("STEEL_API_KEY")
    if not steel_api_key:
        print("❌ STEEL_API_KEY not found in environment variables")
        return
    
    # Initialize Steel client
    steel = Steel(steel_api_key=steel_api_key)
    
    try:
        # Release all sessions
        print("Releasing all active sessions...")
        steel.sessions.release_all()
        print("✅ All sessions released")
    except Exception as e:
        print(f"❌ Error releasing sessions: {e}")

if __name__ == "__main__":
    main()
