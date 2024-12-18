import asyncio
import re
from typing import List
from langchain_core.tools import Tool
from steel_langchain import SteelWebLoader

class WebTools:
    """Web interaction tools using Steel sessions."""
    
    def __init__(self):
        try:
            self._loop = asyncio.get_running_loop()
        except RuntimeError:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL to ensure it works with Steel."""
        # Clean URL
        url = url.strip().strip('`')
        
        # Add www if needed
        if not re.match(r'^https?://(www\.)?', url):
            url = f"https://www.{url.replace('https://', '')}"
        elif not re.match(r'^https?://www\.', url):
            url = url.replace('https://', 'https://www.')
        
        return url
    
    async def browse_page(self, url: str) -> str:
        """Browse and extract content from a webpage using Steel session."""
        url = self._normalize_url(url)
        
        loader = SteelWebLoader(
            urls=[url],
            extract_strategy="text",
            solve_captcha=True,
            use_proxy=False,  # Disable proxy for public websites
            timeout=60000  # Increase timeout to 60 seconds
        )
        try:
            docs = await loader.load()
            return docs[0].page_content if docs else "Failed to load page"
        except Exception as e:
            return f"Error loading page: {str(e)}"
    
    def sync_browse_page(self, url: str) -> str:
        """Synchronous wrapper for browse_page."""
        return self._loop.run_until_complete(self.browse_page(url))
    
    async def get_page_html(self, url: str) -> str:
        """Get the HTML structure of a webpage using Steel session."""
        url = self._normalize_url(url)
        
        loader = SteelWebLoader(
            urls=[url],
            extract_strategy="html",
            solve_captcha=True,
            use_proxy=False,  # Disable proxy for public websites
            timeout=60000  # Increase timeout to 60 seconds
        )
        try:
            docs = await loader.load()
            if not docs:
                return "Failed to load page"
            return f"Page HTML structure from {url}:\n{docs[0].page_content}"
        except Exception as e:
            return f"Error loading page: {str(e)}"
    
    def sync_get_page_html(self, url: str) -> str:
        """Synchronous wrapper for get_page_html."""
        return self._loop.run_until_complete(self.get_page_html(url))

def create_web_tools() -> List[Tool]:
    """Create tools for web interaction using Steel sessions."""
    tools = WebTools()
    
    return [
        Tool(
            name="BrowsePage",
            func=tools.sync_browse_page,
            description=(
                "Browse a webpage and extract its text content. "
                "Use this to understand the main content of a page. "
                "Input should be a URL (e.g. example.com or www.example.com)."
            )
        ),
        Tool(
            name="GetPageHTML",
            func=tools.sync_get_page_html,
            description=(
                "Get the HTML structure of a webpage. "
                "Use this when you need to analyze page layout or find specific elements. "
                "Only use if BrowsePage doesn't give you what you need. "
                "Input should be a URL (e.g. example.com or www.example.com)."
            )
        )
    ]
