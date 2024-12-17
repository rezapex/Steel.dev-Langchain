import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

from steel import Steel
from playwright.sync_api import sync_playwright

class SteelSessionManager:
    """
    Manages Steel browser sessions with Playwright integration
    """
    
    def __init__(
        self, 
        steel_api_key: Optional[str] = None,
        use_proxy: bool = True,
        solve_captcha: bool = True
    ):
        """
        Initialize the Steel Session Manager
        
        :param steel_api_key: Steel API key (optional, will try to load from .env)
        :param use_proxy: Use Steel's proxy network
        :param solve_captcha: Enable CAPTCHA solving
        """
        # Load environment variables
        load_dotenv()
        
        # Get API key
        self.steel_api_key = steel_api_key or os.getenv('STEEL_API_KEY')
        if not self.steel_api_key:
            raise ValueError("STEEL_API_KEY must be set in .env file")
        
        # Store configuration
        self.config = {
            'use_proxy': use_proxy,
            'solve_captcha': solve_captcha
        }
        
        # Initialize Steel client
        self.client = Steel(steel_api_key=self.steel_api_key)
        
        # Session and browser tracking
        self.current_session = None
        self.current_browser = None
    
    def create_session(self) -> Dict[str, Any]:
        """
        Create a new Steel session
        
        :return: Dictionary with session details
        """
        # Release any existing session
        self.release_session()
        
        # Create new session
        self.current_session = self.client.sessions.create(
            use_proxy=self.config['use_proxy'],
            solve_captcha=self.config['solve_captcha']
        )
        
        return {
            'id': self.current_session.id,
            'viewer_url': self.current_session.session_viewer_url
        }
    
    def connect_playwright(self) -> Any:
        """
        Connect Playwright to the current Steel session
        
        :return: Playwright browser object
        """
        if not self.current_session:
            raise RuntimeError("No active session. Call create_session() first.")
        
        # Connect Playwright
        playwright = sync_playwright().start()
        self.current_browser = playwright.chromium.connect_over_cdp(
            f"wss://connect.steel.dev?apiKey={self.steel_api_key}&sessionId={self.current_session.id}"
        )
        
        return self.current_browser
    
    def release_session(self):
        """
        Release the current Steel session and close Playwright browser
        """
        # Close Playwright browser if exists
        if self.current_browser:
            try:
                self.current_browser.close()
            except Exception as e:
                print(f"Error closing browser: {e}")
            finally:
                self.current_browser = None
        
        # Release Steel session if exists
        if self.current_session:
            try:
                self.client.sessions.release(self.current_session.id)
            except Exception as e:
                print(f"Error releasing session: {e}")
            finally:
                self.current_session = None
    
    def __enter__(self):
        """
        Context manager entry point
        """
        self.create_session()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit point
        """
        self.release_session()