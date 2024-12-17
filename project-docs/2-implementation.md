# Steel x LangChain Integration Implementation

## Core Components

### SteelWebLoader

The core of the integration is the `SteelWebLoader` class, which implements LangChain's `BaseLoader` pattern while leveraging Steel's advanced features:

```python
from steel_langchain import SteelWebLoader

# Basic usage
loader = SteelWebLoader(
    urls=["https://example.com"],
    steel_api_key="your-api-key"
)
documents = loader.load()
```

#### Key Features

1. **Session Management**
   - Automated session lifecycle management
   - Session reuse capabilities
   - Proper cleanup on interruption
   - Live session viewer integration

2. **Content Extraction**
   - Multiple extraction strategies (text, HTML, markdown)
   - Configurable timeouts and retries
   - Error handling and logging

3. **Steel Integration**
   - Proxy network support
   - Automated CAPTCHA solving
   - Browser automation via Playwright

4. **Resource Management**
   - Async context managers for resources
   - Proper event loop handling
   - Signal handling for graceful cleanup

#### Implementation Details

1. **BaseLoader Pattern**
   ```python
   class SteelWebLoader(BaseLoader):
       def lazy_load(self) -> Iterator[Document]:
           # Load pages one at a time
           
       def load(self) -> List[Document]:
           # Load all pages at once
   ```

2. **Session Management**
   ```python
   @asynccontextmanager
   async def _managed_session(self):
       try:
           if not self.session:
               await self._create_session()
           yield
       finally:
           await self._cleanup()
   ```

3. **Content Extraction**
   ```python
   async def _aload_url(self, url: str) -> Document:
       async with self._managed_session():
           # Load and extract content
           return Document(
               page_content=content,
               metadata={
                   'source': url,
                   'steel_session_id': session.id,
                   'steel_session_viewer_url': viewer_url,
                   'extract_strategy': strategy
               }
           )
   ```

## LangChain Agent Integration

The Steel loader can be used with LangChain agents for web automation tasks. Here's an example:

```python
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from steel_langchain import SteelWebLoader

# Create web tools
def load_webpage(url: str) -> str:
    loader = SteelWebLoader(
        urls=[url],
        extract_strategy="text"
    )
    docs = loader.load()
    return docs[0].page_content

tools = [
    Tool(
        name="ReadWebPage",
        func=load_webpage,
        description="Read and extract text content from a webpage."
    )
]

# Create agent
llm = ChatOpenAI(temperature=0)
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Use agent
result = agent_executor.invoke({
    "input": "What is the main content of https://example.com?"
})
```

### Example Agent Capabilities

1. **Content Analysis**
   ```python
   # Extract and analyze page content
   "What is the main content of https://example.com?"
   ```

2. **Structure Analysis**
   ```python
   # Analyze HTML structure
   "Analyze the HTML structure of https://example.com"
   ```

3. **Multi-page Comparison**
   ```python
   # Compare multiple pages
   "Compare the content of https://example.com and https://httpbin.org/html"
   ```

## Usage Examples

### Basic Document Loading

```python
# Load a single page
loader = SteelWebLoader(
    urls=["https://example.com"],
    extract_strategy="text"
)
docs = loader.load()

# Access content
print(docs[0].page_content)
print(docs[0].metadata)  # Includes session viewer URL
```

### Multiple Pages

```python
# Load multiple pages
loader = SteelWebLoader(
    urls=[
        "https://example.com",
        "https://httpbin.org/html"
    ],
    extract_strategy="html"
)

# Use lazy loading for memory efficiency
for doc in loader.lazy_load():
    print(f"Loaded: {doc.metadata['source']}")
```

### Advanced Features

```python
# Enable proxy and CAPTCHA solving
loader = SteelWebLoader(
    urls=["https://example.com"],
    use_proxy=True,
    solve_captcha=True,
    timeout=60000  # 60 seconds
)

# Get session information for debugging
session_info = loader.get_session_info()
print(f"Debug at: {session_info['viewer_url']}")
```

## Testing

The integration includes comprehensive tests covering:
1. Basic page loading
2. Multiple page loading
3. Lazy loading functionality
4. Session management
5. Error handling
6. Resource cleanup

Run tests with:
```bash
python tests/test_loader.py
```

## Next Steps

1. **Documentation**
   - [ ] Create tutorial documentation
   - [ ] Add example notebooks
   - [ ] Write API reference

2. **Examples**
   - [x] Create real-world use cases
   - [x] Add agent integration examples
   - [ ] Create demo video/gif

3. **Testing**
   - [ ] Add more edge cases
   - [ ] Add performance tests
   - [ ] Add integration tests with agents

4. **Features**
   - [ ] Add more extraction strategies
   - [ ] Add screenshot support
   - [ ] Add PDF export
   - [ ] Add more session configuration options
