"""Simple LangChain agent for interacting with Steel web sessions."""
import os
import re
import json
import asyncio
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from steel_langchain import SteelWebLoader

# ANSI color codes
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"

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
    
    async def extract_links(self, url: str) -> str:
        """Extract all links from a webpage."""
        url = self._normalize_url(url)
        
        loader = SteelWebLoader(
            urls=[url],
            extract_strategy="links",
            solve_captcha=True,
            use_proxy=False,
            timeout=60000
        )
        try:
            docs = await loader.load()
            if not docs:
                return "No links found on page"
            links = docs[0].metadata.get('links', [])
            return json.dumps(links, indent=2)
        except Exception as e:
            return f"Error extracting links: {str(e)}"
    
    def sync_extract_links(self, url: str) -> str:
        """Synchronous wrapper for extract_links."""
        return self._loop.run_until_complete(self.extract_links(url))
    
    async def take_screenshot(self, url: str) -> str:
        """Take a screenshot of a webpage."""
        url = self._normalize_url(url)
        
        loader = SteelWebLoader(
            urls=[url],
            extract_strategy="screenshot",
            solve_captcha=True,
            use_proxy=False,
            timeout=60000
        )
        try:
            docs = await loader.load()
            if not docs:
                return "Failed to take screenshot"
            screenshot_path = docs[0].metadata.get('screenshot_path', '')
            return f"Screenshot saved to: {screenshot_path}"
        except Exception as e:
            return f"Error taking screenshot: {str(e)}"
    
    def sync_take_screenshot(self, url: str) -> str:
        """Synchronous wrapper for take_screenshot."""
        return self._loop.run_until_complete(self.take_screenshot(url))
    
    async def get_metadata(self, url: str) -> str:
        """Get metadata from a webpage (title, description, etc.)."""
        url = self._normalize_url(url)
        
        loader = SteelWebLoader(
            urls=[url],
            extract_strategy="metadata",
            solve_captcha=True,
            use_proxy=False,
            timeout=60000
        )
        try:
            docs = await loader.load()
            if not docs:
                return "No metadata found"
            metadata = {
                'title': docs[0].metadata.get('title', ''),
                'description': docs[0].metadata.get('description', ''),
                'keywords': docs[0].metadata.get('keywords', ''),
                'author': docs[0].metadata.get('author', ''),
                'language': docs[0].metadata.get('language', '')
            }
            return json.dumps(metadata, indent=2)
        except Exception as e:
            return f"Error getting metadata: {str(e)}"
    
    def sync_get_metadata(self, url: str) -> str:
        """Synchronous wrapper for get_metadata."""
        return self._loop.run_until_complete(self.get_metadata(url))
    
    async def extract_tables(self, url: str) -> str:
        """Extract tables from a webpage."""
        url = self._normalize_url(url)
        
        loader = SteelWebLoader(
            urls=[url],
            extract_strategy="tables",
            solve_captcha=True,
            use_proxy=False,
            timeout=60000
        )
        try:
            docs = await loader.load()
            if not docs:
                return "No tables found on page"
            tables = docs[0].metadata.get('tables', [])
            return json.dumps(tables, indent=2)
        except Exception as e:
            return f"Error extracting tables: {str(e)}"
    
    def sync_extract_tables(self, url: str) -> str:
        """Synchronous wrapper for extract_tables."""
        return self._loop.run_until_complete(self.extract_tables(url))
    
    async def search_in_page(self, url_and_query: str) -> str:
        """Search for specific text within a webpage."""
        try:
            url, query = url_and_query.split('|')
            url = self._normalize_url(url.strip())
            query = query.strip()
        except ValueError:
            return "Error: Input should be in format 'url|search_query'"
        
        loader = SteelWebLoader(
            urls=[url],
            extract_strategy="text",
            solve_captcha=True,
            use_proxy=False,
            timeout=60000
        )
        try:
            docs = await loader.load()
            if not docs:
                return "Failed to load page"
            
            content = docs[0].page_content.lower()
            query = query.lower()
            
            # Find all occurrences with surrounding context
            matches = []
            for match in re.finditer(re.escape(query), content):
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = f"...{content[start:end]}..."
                matches.append(context)
            
            if not matches:
                return f"No matches found for '{query}'"
            
            return f"Found {len(matches)} matches:\n" + "\n\n".join(matches)
        except Exception as e:
            return f"Error searching page: {str(e)}"
    
    def sync_search_in_page(self, url_and_query: str) -> str:
        """Synchronous wrapper for search_in_page."""
        return self._loop.run_until_complete(self.search_in_page(url_and_query))

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
        ),
        Tool(
            name="ExtractLinks",
            func=tools.sync_extract_links,
            description=(
                "Extract all links from a webpage. "
                "Use this to find navigation options or linked resources. "
                "Input should be a URL (e.g. example.com or www.example.com)."
            )
        ),
        Tool(
            name="TakeScreenshot",
            func=tools.sync_take_screenshot,
            description=(
                "Take a screenshot of a webpage. "
                "Use this to capture the visual state of a page. "
                "Input should be a URL (e.g. example.com or www.example.com)."
            )
        ),
        Tool(
            name="GetMetadata",
            func=tools.sync_get_metadata,
            description=(
                "Get metadata from a webpage (title, description, etc.). "
                "Use this to understand basic page information. "
                "Input should be a URL (e.g. example.com or www.example.com)."
            )
        ),
        Tool(
            name="ExtractTables",
            func=tools.sync_extract_tables,
            description=(
                "Extract tables from a webpage. "
                "Use this when you need to analyze tabular data. "
                "Input should be a URL (e.g. example.com or www.example.com)."
            )
        ),
        Tool(
            name="SearchInPage",
            func=tools.sync_search_in_page,
            description=(
                "Search for specific text within a webpage. "
                "Use this to find specific content or verify text presence. "
                "Input should be in format 'url|search_query' "
                "(e.g. 'example.com|search term')."
            )
        )
    ]

def create_agent_prompt() -> PromptTemplate:
    """Create the agent prompt template."""
    template = """You are a web browsing agent that can interact with web pages using Steel's browser infrastructure.

You have access to the following tools:

{tools}

The available tools are: {tool_names}

Use this format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Important:
- Use BrowsePage first to get page content
- Only use GetPageHTML if you need to analyze page structure
- Don't repeat tool calls on the same URL unless you get an error
- URLs can be in any format (e.g. example.com or www.example.com)

Question: {input}

{agent_scratchpad}"""

    return PromptTemplate.from_template(template)

def create_web_agent(openai_api_key: str = None) -> AgentExecutor:
    """Create a web browsing agent.
    
    Args:
        openai_api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY env var.
    
    Returns:
        AgentExecutor: Ready-to-use web browsing agent
    """
    if not openai_api_key:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError(
                "OpenAI API key must be provided either through parameter "
                "or OPENAI_API_KEY environment variable"
            )
    
    # Create tools and agent
    tools = create_web_tools()
    llm = ChatOpenAI(
        temperature=0,
        api_key=openai_api_key
    )
    prompt = create_agent_prompt()
    
    # Create agent with proper error handling
    try:
        agent = create_react_agent(llm, tools, prompt)
    except ValueError as e:
        if "missing required variables" in str(e):
            print(f"{RED}Error: Prompt template configuration issue - {str(e)}{RESET}")
        raise
    except Exception as e:
        print(f"{RED}Error creating agent: {e}{RESET}")
        raise
    
    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=3,  # Limit iterations to prevent loops
        return_intermediate_steps=False  # Don't return raw output
    )

def format_agent_output(text: str) -> str:
    """Format the agent's output with colors and structure."""
    # Format thought process
    text = re.sub(
        r'Thought: (.*?)(?=\n|$)',
        f'{BLUE}💭 Thought:{RESET} \\1',
        text,
        flags=re.MULTILINE
    )
    
    # Format actions
    text = re.sub(
        r'Action: (.*?)(?=\n|$)',
        f'{GREEN}⚡ Action:{RESET} {BOLD}\\1{RESET}',
        text,
        flags=re.MULTILINE
    )
    
    # Format action inputs
    text = re.sub(
        r'Action Input: (.*?)(?=\n|$)',
        f'{GREEN}📥 Input:{RESET} \\1',
        text,
        flags=re.MULTILINE
    )
    
    # Format observations
    text = re.sub(
        r'Observation: (.*?)(?=\n|$)',
        f'{BLUE}👁️ Observation:{RESET} \\1',
        text,
        flags=re.MULTILINE
    )
    
    # Format final answer
    text = re.sub(
        r'Final Answer: (.*?)(?=\n|$)',
        f'\n{YELLOW}💡 Final Answer:{RESET} \\1',
        text,
        flags=re.MULTILINE
    )
    
    # Format chain markers
    text = text.replace(
        "> Entering new AgentExecutor chain...",
        f"\n{BOLD}{'='*50}\n🤖 Starting Web Agent\n{'='*50}{RESET}\n"
    )
    text = text.replace(
        "> Finished chain.",
        f"\n{BOLD}{'='*50}\n✅ Agent Complete\n{'='*50}{RESET}\n"
    )
    
    return text

def main():
    """Run example usage of the web agent."""
    # Load environment variables
    load_dotenv()
    
    # Verify required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print(f"{RED}Error: OPENAI_API_KEY environment variable is required{RESET}")
        return
    if not os.getenv("STEEL_API_KEY"):
        print(f"{RED}Error: STEEL_API_KEY environment variable is required{RESET}")
        return
    
    # Create agent
    try:
        agent = create_web_agent()
    except Exception as e:
        print(f"{RED}Failed to create agent: {e}{RESET}")
        return
    
    # Example task
    task = "What is the HTML structure of https://example.com?"
    # task = "What is the main content of https://example.com?"
    print(f"\n{BOLD}{'='*50}{RESET}")
    print(f"{YELLOW}🎯 Task:{RESET} {task}")
    print(f"{BOLD}{'='*50}{RESET}\n")
    
    try:
        result = agent.invoke({"input": task})
        
        # Format and display the complete chain output
        formatted_output = format_agent_output(result['output'])
        print(formatted_output)
        
    except Exception as e:
        print(f"{RED}Error during execution: {e}{RESET}")

if __name__ == "__main__":
    main()
