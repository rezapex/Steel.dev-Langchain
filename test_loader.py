import os
from dotenv import load_dotenv
from web_loader_2 import SteelWebLoader

def test_basic_loader():
    """Test basic webpage loading"""
    loader = SteelWebLoader(
        url="https://example.com",  # Fixed URL
        steel_api_key=os.getenv("STEEL_API_KEY"),
        extract_strategy="text"
    )
    
    try:
        print("\nTest 1: Basic webpage loading")
        print("Loading webpage...")
        documents = loader.load()
        
        if documents:
            print("✅ Successfully loaded basic webpage!")
            print("\nMetadata:", documents[0].metadata)
            print("\nContent preview:", documents[0].page_content[:200])
        else:
            print("❌ No documents returned")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def test_dynamic_content():
    """Test loading a page with dynamic content"""
    loader = SteelWebLoader(
        url="https://news.ycombinator.com",
        steel_api_key=os.getenv("STEEL_API_KEY"),
        extract_strategy="html",
        timeout=60000  # Longer timeout for dynamic content
    )
    
    try:
        print("\nTest 2: Dynamic content loading")
        print("Loading webpage...")
        documents = loader.load()
        
        if documents:
            print("✅ Successfully loaded dynamic webpage!")
            print("\nMetadata:", documents[0].metadata)
            print("\nContent size:", len(documents[0].page_content), "characters")
            # Look for evidence of dynamic content
            if "item" in documents[0].page_content and "score" in documents[0].page_content:
                print("✅ Found expected dynamic content markers")
            else:
                print("⚠️ Dynamic content markers not found")
        else:
            print("❌ No documents returned")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("STEEL_API_KEY"):
        print("❌ STEEL_API_KEY not found in environment variables")
        return
    
    # Run tests
    test_basic_loader()
    test_dynamic_content()

if __name__ == "__main__":
    main()
