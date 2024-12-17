"""Example of using Steel Web Loader with LangChain agents."""
import os
from typing import List
from dotenv import load_dotenv
from langchain_core.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from rich.console import Console
from steel_langchain import SteelWebLoader
from steel import Steel

console = Console()

def create_web_tools():
    """Create tools for web automation."""
    
    def load_webpage(url: str) -> str:
        """Load content from a webpage."""
        loader = SteelWebLoader(
            urls=[url],
            extract_strategy="text"  # Use text for better agent comprehension
        )
        docs = loader.load()
        return docs[0].page_content if docs else "Failed to load page"

    def analyze_page_structure(url: str) -> str:
        """Analyze HTML structure of a webpage."""
        loader = SteelWebLoader(
            urls=[url],
            extract_strategy="html",  # Use HTML for structure analysis
            solve_captcha=True  # Enable CAPTCHA solving for protected pages
        )
        docs = loader.load()
        return docs[0].page_content if docs else "Failed to load page"

    def compare_pages(urls_str: str) -> str:
        """Compare content from multiple web pages."""
        urls = [url.strip() for url in urls_str.split(',')]
        loader = SteelWebLoader(
            urls=urls,
            extract_strategy="text"
        )
        docs = loader.load()
        return "\n\nComparison:\n".join(
            f"Page {i+1} ({doc.metadata['source']}):\n{doc.page_content[:500]}..."
            for i, doc in enumerate(docs)
        )

    return [
        Tool(
            name="ReadWebPage",
            func=load_webpage,
            description=(
                "Read and extract text content from a webpage. "
                "Use this for understanding page content. "
                "Input should be a URL."
            )
        ),
        Tool(
            name="AnalyzePageStructure",
            func=analyze_page_structure,
            description=(
                "Analyze the HTML structure of a webpage. "
                "Use this when you need to understand page layout or find specific elements. "
                "Input should be a URL."
            )
        ),
        Tool(
            name="ComparePages",
            func=compare_pages,
            description=(
                "Compare content from multiple web pages. "
                "Input should be URLs separated by commas. "
                "Example: 'https://example1.com,https://example2.com'"
            )
        )
    ]

def create_agent_prompt():
    """Create the agent prompt template."""
    template = """You are a web automation agent that can browse and analyze web pages using Steel's browser infrastructure.

Available tools:
{tools}

To use a tool, use the following format:
```
Thought: I need to [explain what you want to do]
Action: [tool name]
Action Input: [tool input]
```

After using a tool, you'll get an observation. Use this format to continue:
```
Observation: [result from tool]
Thought: I now know [explain what you learned]
Action: [next tool to use, or "Final Answer" to give your response]
```

Current task: {input}

Begin!

{agent_scratchpad}"""

    return PromptTemplate.from_template(template)

def main():
    # Load environment variables
    load_dotenv()
    
    # Create tools and agent
    tools = create_web_tools()
    llm = ChatOpenAI(temperature=0)
    prompt = create_agent_prompt()
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    # Example tasks demonstrating different capabilities
    tasks = [
        # Basic content extraction
        "What is the main content of https://example.com?",
        
        # Structure analysis
        "Analyze the HTML structure of https://example.com and identify its main sections",
        
        # Multi-page comparison
        "Compare the content of https://example.com and https://httpbin.org/html. What are the main differences?"
    ]
    
    # Run tasks
    for i, task in enumerate(tasks, 1):
        console.print(f"\n{'='*80}\nTask {i}: {task}\n{'='*80}")
        try:
            result = agent_executor.invoke({"input": task})
            console.print(f"\n[green]Result:[/green] {result['output']}")
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")
        console.print("\n[blue]Session released automatically through loader cleanup[/blue]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\n\nError: {e}")
    finally:
        # Clean up any active sessions
        steel = Steel(steel_api_key=os.getenv("STEEL_API_KEY"))
        steel.sessions.release_all()
        print("\n✓ All sessions released")
