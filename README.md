# Steel x LangChain Integration

A LangChain integration for Steel.dev that enables AI agents to leverage Steel's managed browser infrastructure for web automation tasks.

## Features

- 🌐 Load web pages with Steel's managed browser infrastructure
- 🔄 Persistent sessions for efficient browsing
- 🔒 Built-in proxy network support
- 🤖 Automated CAPTCHA solving
- 📄 Multiple content extraction strategies (text, HTML, markdown)
- 🔍 Session viewer for debugging
- ⚡ Async support with proper resource management
- 🛡️ Comprehensive error handling

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/steel-langchain.git
cd steel-langchain

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Unix
# or
.\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

## Environment Setup

Create a `.env` file with your Steel API key:

```env
STEEL_API_KEY=your_steel_api_key_here
```

## Usage

### Basic Usage

```python
from steel_langchain import SteelWebLoader

# Initialize loader
loader = SteelWebLoader(
    urls=["https://example.com"],
    extract_strategy="text"
)

# Load webpage
documents = loader.load()

# Access content
print(documents[0].page_content)
print(documents[0].metadata)  # Includes session viewer URL
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

## Features

### Session Management

- Persistent sessions for efficient browsing
- Session reuse capabilities
- Automatic cleanup on interruption
- Live session viewer for debugging

### Content Extraction

- Text extraction for clean content
- HTML extraction for structure analysis
- Markdown extraction for formatting
- Configurable timeouts and retries

### Steel Integration

- Proxy network support for access
- Automated CAPTCHA solving
- Browser automation via Playwright
- Session viewer integration

### Resource Management

- Async context managers
- Proper event loop handling
- Signal handling for cleanup
- Memory-efficient lazy loading

## Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/steel-langchain.git
cd steel-langchain
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # Unix
pip install -r requirements.txt
playwright install
```

3. Run tests:
```bash
python tests/test_loader.py
```

4. Run demo:
```bash
python demo.py
```

## Project Structure

```
steel-langchain/
├── src/
│   └── steel_langchain/
│       ├── __init__.py
│       └── web_loader.py
├── tests/
│   └── test_loader.py
├── project-docs/
│   ├── 1-project-overview.md
│   └── 2-implementation.md
├── requirements.txt
├── setup.py
├── README.md
└── .env
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Steel.dev](https://steel.dev) - For providing the browser automation infrastructure
- [LangChain](https://python.langchain.com) - For the document loader interface and agent framework
