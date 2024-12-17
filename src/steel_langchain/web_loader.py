"""Load web pages using Steel.dev browser automation."""
import os
from typing import List, Optional, AsyncIterator
import logging
import asyncio
from langchain_core.documents import Document
from langchain_community.document_loaders.base import BaseLoader
from steel import AsyncSteel
from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

class SteelWebLoader(BaseLoader):
    """Load web pages using Steel.dev browser automation.
    
    This loader uses Steel.dev's managed browser infrastructure to load web pages,
    with support for proxy networks, automated CAPTCHA solving, and session management.
    
    Features:
        - Managed browser infrastructure
        - Proxy network support
        - Automated CAPTCHA solving
        - Session management and reuse
        - Multiple content extraction strategies
        - Live session viewer for debugging
        
    Args:
        urls: List of URLs to load
        steel_api_key: Steel API key. If not provided, will look for STEEL_API_KEY env var
        extract_strategy: Content extraction method ('text', 'markdown', or 'html')
        timeout: Navigation timeout in milliseconds
        use_proxy: Whether to use Steel's proxy network
        solve_captcha: Whether to enable automated CAPTCHA solving
    
    Example:
        .. code-block:: python

            from langchain_community.document_loaders import SteelWebLoader

            loader = SteelWebLoader(
                urls=["https://example.com"],
                steel_api_key="your-api-key"
            )
            documents = await loader.load()
    """
    
    def __init__(
        self,
        urls: List[str],
        steel_api_key: Optional[str] = None,
        extract_strategy: str = 'text',
        timeout: int = 30000,
        use_proxy: bool = True,
        solve_captcha: bool = True
    ) -> None:
        """Initialize the Steel Web Loader."""
        self.urls = urls
        self.steel_api_key = steel_api_key or os.getenv("STEEL_API_KEY")
        if not self.steel_api_key:
            raise ValueError(
                "Steel API key must be provided either through steel_api_key parameter "
                "or STEEL_API_KEY environment variable"
            )
        
        self.extract_strategy = extract_strategy
        self.timeout = timeout
        self.use_proxy = use_proxy
        self.solve_captcha = solve_captcha
        
        valid_strategies = ['text', 'markdown', 'html']
        if extract_strategy not in valid_strategies:
            raise ValueError(
                f"Invalid extract_strategy. Must be one of {valid_strategies}"
            )
        
        # Initialize Steel client
        self.steel = AsyncSteel(
            steel_api_key=self.steel_api_key,
            timeout=timeout / 1000.0  # Convert to seconds
        )
        
        # Session management
        self.session = None
        self.browser = None
        self.context = None
        self._playwright = None
        self._cleanup_lock = asyncio.Lock()
    
    async def _wait_for_session(self, max_retries: int = 5, delay: int = 2) -> None:
        """Wait for session to be ready."""
        for i in range(max_retries):
            try:
                # Initialize Playwright
                if not self._playwright:
                    self._playwright = await async_playwright().start()
                
                # Try to connect to session
                if not self.browser:
                    print(f"Connecting to session {self.session.id}...")
                    self.browser = await self._playwright.chromium.connect_over_cdp(
                        f"wss://connect.steel.dev?apiKey={self.steel_api_key}&sessionId={self.session.id}",
                        timeout=10000  # 10 second connection timeout
                    )
                
                # Create context if needed
                if not self.context:
                    self.context = await self.browser.new_context()
                return
                
            except Exception as e:
                logger.warning(f"Attempt {i+1} failed: {e}")
                if i == max_retries - 1:
                    raise
                await asyncio.sleep(delay)
    
    async def _create_session(self) -> None:
        """Create a new Steel session and connect browser."""
        try:
            # Create Steel session with longer timeout
            self.session = await self.steel.sessions.create(
                api_timeout=300000,  # 5 minute timeout
                use_proxy=self.use_proxy,
                solve_captcha=self.solve_captcha,
                timeout=300000  # 5 minute session timeout
            )
            print(f"Created Steel session: {self.session.id}")
            
            # Wait for session to be ready and connect
            await self._wait_for_session()
            
        except Exception as e:
            logger.error(f"Error creating session: {e}")
            await self._cleanup()
            raise
    
    async def _cleanup(self) -> None:
        """Clean up resources."""
        async with self._cleanup_lock:
            if self.context:
                try:
                    await self.context.close()
                except Exception as e:
                    logger.error(f"Error closing context: {e}")
                self.context = None
                
            if self.browser:
                try:
                    await self.browser.close()
                except Exception as e:
                    logger.error(f"Error closing browser: {e}")
                self.browser = None
            
            if self._playwright:
                try:
                    await self._playwright.stop()
                except Exception as e:
                    logger.error(f"Error stopping playwright: {e}")
                self._playwright = None
            
            if self.session:
                try:
                    await self.steel.sessions.release(self.session.id)
                    print(f"Released Steel session: {self.session.id}")
                except Exception as e:
                    if "Session already stopped" not in str(e):
                        logger.error(f"Error releasing session: {e}")
                self.session = None
    
    def get_session_info(self) -> dict:
        """Get information about the current session.
        
        Returns:
            Dict containing session details including:
            - session_id: Unique identifier for the session
            - viewer_url: URL to view the session in Steel's session viewer
            - websocket_url: WebSocket URL for connecting to the session
        """
        if not self.session:
            raise RuntimeError("No active session")
        
        return {
            'session_id': self.session.id,
            'viewer_url': self.session.debug_url,
            'websocket_url': f"wss://connect.steel.dev?apiKey={self.steel_api_key}&sessionId={self.session.id}"
        }
    
    async def _aload_url(self, url: str) -> Document:
        """Load a single URL."""
        if not self.session:
            await self._create_session()
        
        try:
            # Create new page
            page = await self.context.new_page()
            print(f"Loading {url}...")
            
            try:
                # Navigate to URL
                await page.goto(url, wait_until="networkidle", timeout=self.timeout)
                print(f"Successfully loaded {url}")
                
                # Extract content based on strategy
                if self.extract_strategy == 'text':
                    content = await page.inner_text('body')
                elif self.extract_strategy == 'markdown':
                    content = await page.inner_text('body')  # Simplified
                else:  # html
                    content = await page.content()
                
                return Document(
                    page_content=content,
                    metadata={
                        'source': url,
                        'steel_session_id': self.session.id,
                        'steel_session_viewer_url': self.session.debug_url,
                        'extract_strategy': self.extract_strategy
                    }
                )
            finally:
                await page.close()
                
        except Exception as e:
            logger.error(f"Error loading {url}: {e}")
            raise
    
    async def lazy_load(self) -> AsyncIterator[Document]:
        """Load pages one at a time.
        
        This method yields documents as they are loaded, which is more memory
        efficient for large numbers of URLs.
        
        Yields:
            Document: Loaded web page as a Document object
        """
        try:
            for url in self.urls:
                try:
                    yield await self._aload_url(url)
                except asyncio.CancelledError:
                    print("\nOperation cancelled, cleaning up...")
                    await self._cleanup()
                    raise
                except Exception as e:
                    logger.error(f"Error loading {url}: {e}")
                    raise
        finally:
            await self._cleanup()
    
    async def load(self) -> List[Document]:
        """Load all pages.
        
        This method loads all pages and returns them as a list. For large numbers
        of URLs, consider using lazy_load() instead.
        
        Returns:
            List[Document]: List of loaded web pages as Document objects
        """
        documents = []
        try:
            async for doc in self.lazy_load():
                documents.append(doc)
            return documents
        except asyncio.CancelledError:
            print("\nOperation cancelled, cleaning up...")
            await self._cleanup()
            raise
