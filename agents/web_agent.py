"""Simple LangChain agent for interacting with Steel web sessions."""
import os
import re
import asyncio
from typing import List
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
