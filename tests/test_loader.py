"""Test suite for Steel Web Loader."""
import os
import signal
import asyncio
from dotenv import load_dotenv
from steel import Steel
from steel_langchain import SteelWebLoader

# Global state for cleanup
cleanup_tasks = []

def handle_sigint(signum, frame):
    """Handle SIGINT (Ctrl+C) gracefully."""
    print("\nCleaning up...")
    try:
        # Release all sessions
        Steel(steel_api_key=os.getenv("STEEL_API_KEY")).sessions.release_all()
        
        # Cancel any pending tasks
        for task in cleanup_tasks:
            if not task.done():
                task.cancel()
    except Exception as e:
        print(f"Error during cleanup: {e}")
    print("Cleanup complete")
    exit(0)

async def test_basic_loading():
    """Test basic webpage loading"""
    print("\nTest 1: Basic Loading")
    
    # Create loader with single URL and shorter timeout
    loader = SteelWebLoader(
        urls=["https://example.com"],
        extract_strategy="text",
        timeout=10000  # 10 seconds
    )
    
    try:
        print("Creating Steel session...")
        docs = await loader.load()
        
        if docs:
            print("✅ Successfully loaded webpage!")
            print("\nMetadata:", docs[0].metadata)
            print("\nContent preview:", docs[0].page_content[:200])
        else:
            print("❌ No documents returned")
            
    except asyncio.CancelledError:
        print("\nTest cancelled, cleaning up...")
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

async def test_multiple_pages():
    """Test loading multiple pages"""
    print("\nTest 2: Multiple Pages")
    
    # Create loader with multiple URLs
    loader = SteelWebLoader(
        urls=[
            "https://example.com",
            "https://httpbin.org/html"
        ],
        extract_strategy="html",
        timeout=10000
    )
    
    try:
        print("Loading multiple pages...")
        docs = await loader.load()
        
        if docs:
            print(f"✅ Successfully loaded {len(docs)} pages!")
            for i, doc in enumerate(docs, 1):
                print(f"\nPage {i}:")
                print("URL:", doc.metadata['source'])
                print("Content preview:", doc.page_content[:100])
        else:
            print("❌ No documents returned")
            
    except asyncio.CancelledError:
        print("\nTest cancelled, cleaning up...")
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

async def test_lazy_loading():
    """Test lazy loading functionality"""
    print("\nTest 3: Lazy Loading")
    
    # Create loader with multiple URLs
    loader = SteelWebLoader(
        urls=[
            "https://example.com",
            "https://httpbin.org/html"
        ],
        timeout=10000
    )
    
    try:
        print("Lazy loading pages...")
        async for doc in loader.lazy_load():
            print(f"\n✅ Successfully loaded: {doc.metadata['source']}")
            print("Content preview:", doc.page_content[:100])
            
    except asyncio.CancelledError:
        print("\nTest cancelled, cleaning up...")
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

async def test_session_info():
    """Test session information access"""
    print("\nTest 4: Session Information")
    
    loader = SteelWebLoader(
        urls=["https://example.com"],
        timeout=10000
    )
    
    try:
        print("Creating session...")
        # Create session by loading first URL
        async for doc in loader.lazy_load():
            # Get session info before the session is released
            session_info = loader.get_session_info()
            print("\nSession Information:")
            print("Session ID:", session_info['session_id'])
            print("Viewer URL:", session_info['viewer_url'])
            print("WebSocket URL:", session_info['websocket_url'])
            break  # Only need first document
            
    except asyncio.CancelledError:
        print("\nTest cancelled, cleaning up...")
        raise
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

async def run_tests():
    """Run all tests"""
    try:
        # Clean up any existing sessions
        steel = Steel(steel_api_key=os.getenv("STEEL_API_KEY"))
        print("Releasing all sessions...")
        steel.sessions.release_all()
        print("✅ Cleaned up existing sessions")
        
        # Run tests
        test_tasks = [
            asyncio.create_task(test_basic_loading()),
            asyncio.create_task(test_multiple_pages()),
            asyncio.create_task(test_lazy_loading()),
            asyncio.create_task(test_session_info())
        ]
        cleanup_tasks.extend(test_tasks)
        
        # Wait for all tests to complete
        await asyncio.gather(*test_tasks)
        
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
    except asyncio.CancelledError:
        print("\nTests cancelled")
    except Exception as e:
        print(f"Error during tests: {e}")
        raise
    finally:
        # Clean up sessions
        try:
            steel.sessions.release_all()
            print("\n✅ All sessions released")
        except Exception as e:
            print(f"\nError releasing sessions: {e}")

def main():
    # Set up signal handler
    signal.signal(signal.SIGINT, handle_sigint)
    
    # Load environment variables
    load_dotenv()
    
    if not os.getenv("STEEL_API_KEY"):
        print("❌ STEEL_API_KEY not found in environment variables")
        return
    
    print(f"Using Steel API Key: {os.getenv('STEEL_API_KEY')[:10]}...")
    
    try:
        # Run tests with asyncio
        asyncio.run(run_tests())
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
