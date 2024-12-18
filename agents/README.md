# Steel LangChain Agents

This directory contains LangChain agents that leverage Steel's browser infrastructure for web automation tasks.

## Web Agent

The web agent (`web_agent.py`) is a LangChain-based agent that can browse and extract content from web pages using Steel's managed browser infrastructure.

### Features

- 🌐 Browse web pages and extract content
- 📄 Multiple content extraction strategies (text and HTML)
- 🎨 Colored console output for better readability
- 🔄 Proper session management
- ⚡ Async support with Steel integration
- 🛡️ Error handling and retry logic

### Usage

```python
from dotenv import load_dotenv
load_dotenv()

# Create and run the web agent
agent = create_web_agent()
result = agent.invoke({
    "input": "What is the main content of https://example.com?"
})
```

### Tools

The web agent provides two main tools:

1. **BrowsePage**: Extracts text content from a webpage
   - Input: URL (e.g., example.com or www.example.com)
   - Use this to understand the main content of a page

2. **GetPageHTML**: Retrieves the HTML structure of a webpage
   - Input: URL (e.g., example.com or www.example.com)
   - Use this when you need to analyze page layout or find specific elements

### Output Format

The agent provides nicely formatted output with:
- 💭 Thoughts in blue
- ⚡ Actions in green
- 👁️ Observations in blue
- 💡 Final answers in yellow
- Clear section separators

### Environment Variables

Required environment variables:
- `OPENAI_API_KEY`: Your OpenAI API key for the LLM
- `STEEL_API_KEY`: Your Steel API key for browser automation

### Error Handling

The agent includes comprehensive error handling for:
- Missing API keys
- Invalid URLs
- Network errors
- Page load failures
- LLM parsing errors

### Future Improvements

Potential areas for enhancement:
- Additional tools for form filling and clicking
- Screenshot capabilities
- Cookie and local storage management
- Network request interception
- Multiple page comparison
