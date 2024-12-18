"""Shopping Assistant Agent for interacting with Steel sessions."""
import os
import re
import asyncio
from typing import List, Dict, Any
from urllib.parse import urlparse, urlencode, parse_qs, quote_plus
from bs4 import BeautifulSoup
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
        url = url.strip().strip('`').strip("'")
        
        # Add scheme if missing
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Add www if needed for certain domains
        parsed = urlparse(url)
        if 'amazon.com' in parsed.netloc:
            if not parsed.netloc.startswith('www.'):
                url = url.replace(parsed.netloc, 'www.' + parsed.netloc)
        
        return url
    
    def _build_amazon_url(self, query: str, sort: str = None) -> str:
        """Build a properly formatted Amazon URL."""
        base_url = "https://www.amazon.com/s"
        params = {'k': quote_plus(query.strip("'"))}
        
        if sort:
            sort = sort.lower()
            if "price:low" in sort or "price-low" in sort:
                params['s'] = 'price-asc-rank'
            elif "price:high" in sort or "price-high" in sort:
                params['s'] = 'price-desc-rank'
            elif "rating" in sort or "review" in sort:
                params['s'] = 'review-rank'
        
        return f"{base_url}?{urlencode(params)}"
    
    def _extract_product_info(self, html_content: str) -> List[Dict[str, Any]]:
        """Extract product information from Amazon search results."""
        soup = BeautifulSoup(html_content, 'html.parser')
        products = []
        
        # Find all product containers
        for item in soup.find_all('div', {'data-component-type': 's-search-result'}):
            try:
                # Get product link
                link_elem = item.find('a', {'class': 'a-link-normal s-no-outline'})
                if not link_elem:
                    continue
                    
                link = 'https://www.amazon.com' + link_elem.get('href', '')
                
                # Get product title
                title_elem = item.find('span', {'class': 'a-text-normal'})
                title = title_elem.text if title_elem else 'No title'
                
                # Get price
                price_elem = item.find('span', {'class': 'a-offscreen'})
                price = price_elem.text if price_elem else 'Price not available'
                
                # Get rating
                rating_elem = item.find('span', {'class': 'a-icon-alt'})
                rating = rating_elem.text if rating_elem else 'No rating'
                
                # Get review count
                review_elem = item.find('span', {'class': 'a-size-base'})
                reviews = review_elem.text if review_elem else '0'
                
                products.append({
                    'title': title,
                    'price': price,
                    'rating': rating,
                    'reviews': reviews,
                    'link': link
                })
                
            except Exception as e:
                print(f"Error extracting product info: {e}")
                continue
        
        return products
    
    async def search_product(self, query: str) -> str:
        """Search for a product on Amazon using Steel session."""
        url = self._build_amazon_url(query)
        print(f"\n{BLUE}🔗 Searching URL:{RESET} {url}")
        
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
                return "Failed to load search results"
                
            # Extract and format product information
            products = self._extract_product_info(docs[0].page_content)
            
            # Format results
            result = "Found the following products:\n\n"
            for i, product in enumerate(products, 1):
                result += f"{i}. {product['title']}\n"
                result += f"   Price: {product['price']}\n"
                result += f"   Rating: {product['rating']}\n"
                result += f"   Reviews: {product['reviews']}\n"
                result += f"   Link: {product['link']}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error loading search results: {str(e)}"
    
    def sync_search_product(self, query: str) -> str:
        """Synchronous wrapper for search_product."""
        return self._loop.run_until_complete(self.search_product(query))
    
    async def filter_results(self, input_str: str) -> str:
        """Filter search results on Amazon using Steel session."""
        # Parse input string
        parts = [x.strip() for x in input_str.split(',', 1)]
        if len(parts) != 2:
            return "Error: Input must be 'URL, filter_criteria'"
        
        url, filter_criteria = parts
        
        # Extract base query from URL
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        search_query = query_params.get('k', ['laptop'])[0]
        
        # Build new URL with sorting
        url = self._build_amazon_url(search_query, filter_criteria)
        print(f"\n{BLUE}🔗 Filtering URL:{RESET} {url}")
        
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
                return "Failed to load filtered results"
                
            # Extract and format product information
            products = self._extract_product_info(docs[0].page_content)
            
            # Format results
            result = "Found the following filtered products:\n\n"
            for i, product in enumerate(products, 1):
                result += f"{i}. {product['title']}\n"
                result += f"   Price: {product['price']}\n"
                result += f"   Rating: {product['rating']}\n"
                result += f"   Reviews: {product['reviews']}\n"
                result += f"   Link: {product['link']}\n\n"
            
            return result
            
        except Exception as e:
            return f"Error loading filtered results: {str(e)}"
    
    def sync_filter_results(self, input_str: str) -> str:
        """Synchronous wrapper for filter_results."""
        return self._loop.run_until_complete(self.filter_results(input_str))

def create_shopping_tools() -> List[Tool]:
    """Create tools for shopping interaction using Steel sessions."""
    tools = ShoppingTools()
    
    return [
        Tool(
            name="SearchProduct",
            func=tools.sync_search_product,
            description=(
                "Search for a product on Amazon. "
                "Input should be a search query (e.g. 'laptop')."
            )
        ),
        Tool(
            name="FilterResults",
            func=tools.sync_filter_results,
            description=(
                "Filter search results on Amazon. "
                "Input should be a URL and filter criteria separated by comma. "
                "Filter criteria can be 'price:low-to-high', 'price:high-to-low', or 'rating'. "
                "Example: 'https://www.amazon.com/s?k=laptop, price:low-to-high'"
            )
        )
    ]

def create_agent_prompt() -> PromptTemplate:
    """Create the agent prompt template."""
    template = """You are a shopping assistant agent that helps find good laptop deals on Amazon.

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
1. First use SearchProduct to find laptops on Amazon
2. Then use FilterResults with 'price:low-to-high' to sort by price
3. Analyze the results to find laptops that:
   - Are under $1000
   - Have good specs (RAM, storage, processor)
   - Have good reviews (4+ stars)
4. Recommend the best options based on value for money

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
    task = "Find me a good laptop under $1000"
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
