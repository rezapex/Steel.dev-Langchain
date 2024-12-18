"""Shopping Assistant Agent for interacting with Steel sessions."""
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

class ShoppingTools:
    """Shopping interaction tools using Steel sessions."""
    
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
    
    async def search_product(self, query: str) -> str:
        """Search for a product on a shopping website using Steel session."""
        url = self._normalize_url(f"https://www.example.com/search?q={query}")
        
        loader = SteelWebLoader(
            urls=[url],
            extract_strategy="text",
            solve_captcha=True,
            use_proxy=False,  # Disable proxy for public websites
            timeout=60000  # Increase timeout to 60 seconds
        )
        try:
            docs = await loader.load()
            return docs[0].page_content if docs else "Failed to load search results"
        except Exception as e:
            return f"Error loading search results: {str(e)}"
    
    def sync_search_product(self, query: str) -> str:
        """Synchronous wrapper for search_product."""
        return self._loop.run_until_complete(self.search_product(query))
    
    async def filter_results(self, url: str, filter_criteria: str) -> str:
        """Filter search results on a shopping website using Steel session."""
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
            return docs[0].page_content if docs else "Failed to load filtered results"
        except Exception as e:
            return f"Error loading filtered results: {str(e)}"
    
    def sync_filter_results(self, url: str, filter_criteria: str) -> str:
        """Synchronous wrapper for filter_results."""
        return self._loop.run_until_complete(self.filter_results(url, filter_criteria))
    
    async def compare_prices(self, url1: str, url2: str) -> str:
        """Compare prices of products on two different shopping websites using Steel session."""
        url1 = self._normalize_url(url1)
        url2 = self._normalize_url(url2)
        
        loader1 = SteelWebLoader(
            urls=[url1],
            extract_strategy="text",
            solve_captcha=True,
            use_proxy=False,  # Disable proxy for public websites
            timeout=60000  # Increase timeout to 60 seconds
        )
        loader2 = SteelWebLoader(
            urls=[url2],
            extract_strategy="text",
            solve_captcha=True,
            use_proxy=False,  # Disable proxy for public websites
            timeout=60000  # Increase timeout to 60 seconds
        )
        try:
            docs1 = await loader1.load()
            docs2 = await loader2.load()
            if not docs1 or not docs2:
                return "Failed to load one or both pages"
            return f"Price comparison:\n\nSite 1:\n{docs1[0].page_content}\n\nSite 2:\n{docs2[0].page_content}"
        except Exception as e:
            return f"Error comparing prices: {str(e)}"
    
    def sync_compare_prices(self, url1: str, url2: str) -> str:
        """Synchronous wrapper for compare_prices."""
        return self._loop.run_until_complete(self.compare_prices(url1, url2))

def create_shopping_tools() -> List[Tool]:
    """Create tools for shopping interaction using Steel sessions."""
    tools = ShoppingTools()
    
    return [
        Tool(
            name="SearchProduct",
            func=tools.sync_search_product,
            description=(
                "Search for a product on a shopping website. "
                "Input should be a search query (e.g. 'laptop')."
            )
        ),
        Tool(
            name="FilterResults",
            func=tools.sync_filter_results,
            description=(
                "Filter search results on a shopping website. "
                "Input should be a URL and filter criteria (e.g. 'price:low-to-high')."
            )
        ),
        Tool(
            name="ComparePrices",
            func=tools.sync_compare_prices,
            description=(
                "Compare prices of products on two different shopping websites. "
                "Input should be two URLs (e.g. 'site1.com/product' and 'site2.com/product')."
            )
        )
    ]

def create_agent_prompt() -> PromptTemplate:
    """Create the agent prompt template."""
    template = """You are a shopping assistant agent that can interact with shopping websites using Steel's browser infrastructure.

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
- Use SearchProduct first to find products
- Use FilterResults to narrow down the search results
- Use ComparePrices to compare prices between different websites
- Don't repeat tool calls on the same URL unless you get an error
- URLs can be in any format (e.g. example.com or www.example.com)

Question: {input}

{agent_scratchpad}"""

    return PromptTemplate.from_template(template)

def create_shopping_agent(openai_api_key: str = None) -> AgentExecutor:
    """Create a shopping assistant agent.
    
    Args:
        openai_api_key: OpenAI API key. If not provided, will look for OPENAI_API_KEY env var.
    
    Returns:
        AgentExecutor: Ready-to-use shopping assistant agent
    """
    if not openai_api_key:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError(
                "OpenAI API key must be provided either through parameter "
                "or OPENAI_API_KEY environment variable"
            )
    
    # Create tools and agent
    tools = create_shopping_tools()
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
        f"\n{BOLD}{'='*50}\n🤖 Starting Shopping Agent\n{'='*50}{RESET}\n"
    )
    text = text.replace(
        "> Finished chain.",
        f"\n{BOLD}{'='*50}\n✅ Agent Complete\n{'='*50}{RESET}\n"
    )
    
    return text

def main():
    """Run example usage of the shopping agent."""
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
        agent = create_shopping_agent()
    except Exception as e:
        print(f"{RED}Failed to create agent: {e}{RESET}")
        return
    
    # Example task
    task = "Find the best price for a laptop"
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
