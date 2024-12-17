"""Load web pages using Steel.dev browser automation."""
from typing import List, Optional, Dict, Any
import logging
import asyncio
from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader
from playwright.async_api import async_playwright

from .session_manager import SteelSessionManager

class SteelWebLoader(BaseLoader):
    """Load web pages using Steel.dev browser automation.

    This loader uses Steel.dev's managed browser infrastructure to load web pages,
    with support for proxy networks and automated CAPTCHA solving.

    Example:
        .. code-block:: python

            from langchain_community.document_loaders import SteelWebLoader

            loader = SteelWebLoader(
                "https://example.com",
                steel_api_key="your-api-key"
            )
            documents = loader.load()

    """
    
    def __init__(
        self, 
        url: str, 
        steel_api_key: Optional[str] = None,
        extract_strategy: str = 'text',
        timeout: int = 30000,
        use_proxy: bool = True,
        solve_captcha: bool = True
    ) -> None:
        """Initialize the Steel Web Loader.

        Args:
            url: Web page URL to load
            steel_api_key: Steel API key. If not provided, will look for STEEL_API_KEY env var
            extract_strategy: Content extraction method ('text', 'markdown', or 'html')
            timeout: Navigation timeout in milliseconds
            use_proxy: Whether to use Steel's proxy network
            solve_captcha: Whether to enable automated CAPTCHA solving
        
        Raises:
            ValueError: If extract_strategy is invalid
        """
        self.url = url
        self.steel_api_key = steel_api_key
        self.extract_strategy = extract_strategy
        self.timeout = timeout
        self.use_proxy = use_proxy
        self.solve_captcha = solve_captcha
        
        self.logger = logging.getLogger(__name__)
        
        valid_strategies = ['text', 'markdown', 'html']
        if extract_strategy not in valid_strategies:
            raise ValueError(
                f"Invalid extract_strategy. Must be one of {valid_strategies}"
            )
    
    async def _aload(self) -> List[Document]:
        """Async implementation of web page loading.

        Returns:
            List[Document]: List containing the loaded web page as a Document

        Raises:
            Exception: If page loading fails
        """
        # Use session manager to handle session lifecycle
        with SteelSessionManager(steel_api_key=self.steel_api_key) as session_manager:
            # Create session and get details
            session_info = session_manager.create_session()
            self.logger.info(f"Created session: {session_info['id']}")
            
            # Initialize Playwright
            playwright = await async_playwright().start()
            
            try:
                # Connect to Steel session
                browser = await playwright.chromium.connect_over_cdp(
                    f"wss://connect.steel.dev?apiKey={self.steel_api_key}&sessionId={session_info['id']}"
                )
                
                # Create new page
                context = browser.contexts[0]
                page = await context.new_page()
                
                # Navigate to URL
                await page.goto(
                    self.url, 
                    wait_until="networkidle", 
                    timeout=self.timeout
                )
                
                # Extract content based on strategy
                if self.extract_strategy == 'text':
                    content = await page.inner_text('body')
                elif self.extract_strategy == 'markdown':
                    content = await page.inner_text('body')  # Simplified
                else:  # html
                    content = await page.content()
                
                # Create and return document
                return [
                    Document(
                        page_content=content,
                        metadata={
                            'source': self.url,
                            'steel_session_id': session_info['id'],
                            'steel_session_viewer_url': session_info['viewer_url'],
                            'extract_strategy': self.extract_strategy
                        }
                    )
                ]
            
            except Exception as e:
                self.logger.error(f"Error loading {self.url}: {e}")
                return []
            
            finally:
                # Ensure Playwright is stopped
                await playwright.stop()
    
    def load(self) -> List[Document]:
        """Load the web page.

        Returns:
            List[Document]: List containing the loaded web page as a Document
        """
        return asyncio.run(self._aload())