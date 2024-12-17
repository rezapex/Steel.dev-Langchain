"""Visual demo of Steel x LangChain integration."""
import os
import time
from dotenv import load_dotenv
from rich.console import Console
from steel_langchain import SteelWebLoader

console = Console()

def main():
    # Load environment variables
    load_dotenv()
    
    console.print("[bold blue]Steel x LangChain Integration Demo[/bold blue]")
    time.sleep(1)
    
    # Demo 1: Basic content extraction
    console.print("\n[yellow]Demo 1: Basic Content Extraction[/yellow]")
    loader = SteelWebLoader(
        urls=["https://example.com"],
        extract_strategy="text"
    )
    
    console.print("Loading webpage...")
    docs = loader.load()
    console.print("[green]✓ Page loaded![/green]")
    console.print("\nContent:")
    console.print(docs[0].page_content)
    console.print("\nSession viewer:", docs[0].metadata['steel_session_viewer_url'])
    time.sleep(2)
    
    # Demo 2: HTML structure analysis
    console.print("\n[yellow]Demo 2: HTML Structure Analysis[/yellow]")
    loader = SteelWebLoader(
        urls=["https://example.com"],
        extract_strategy="html"
    )
    
    console.print("Analyzing HTML structure...")
    docs = loader.load()
    console.print("[green]✓ Analysis complete![/green]")
    console.print("\nHTML Structure:")
    console.print(docs[0].page_content[:500] + "...")
    console.print("\nSession viewer:", docs[0].metadata['steel_session_viewer_url'])
    time.sleep(2)
    
    # Demo 3: Multi-page comparison
    console.print("\n[yellow]Demo 3: Multi-page Comparison[/yellow]")
    loader = SteelWebLoader(
        urls=[
            "https://example.com",
            "https://httpbin.org/html"
        ],
        extract_strategy="text"
    )
    
    console.print("Comparing pages...")
    docs = loader.load()
    console.print("[green]✓ Comparison complete![/green]")
    
    for i, doc in enumerate(docs, 1):
        console.print(f"\nPage {i}:", doc.metadata['source'])
        console.print(doc.page_content[:200] + "...")
        console.print("Session viewer:", doc.metadata['steel_session_viewer_url'])
        time.sleep(1)
    
    console.print("\n[bold green]Demo Complete![/bold green]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDemo interrupted by user")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        # Clean up any active sessions
        from steel import Steel
        steel = Steel(steel_api_key=os.getenv("STEEL_API_KEY"))
        steel.sessions.release_all()
        print("\n✓ All sessions released")
