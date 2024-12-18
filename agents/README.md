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

## Shopping Assistant Agent

The shopping assistant agent (`shopping_agent.py`) is a LangChain-based agent that can search for products, filter results, and compare prices on shopping websites using Steel's managed browser infrastructure.

### Features

- 🔍 Search for products on shopping websites
- 🛒 Filter search results based on criteria
- 💲 Compare prices between different websites
- 🎨 Colored console output for better readability
- 🔄 Proper session management
- ⚡ Async support with Steel integration
- 🛡️ Error handling and retry logic

### Usage

```python
from dotenv import load_dotenv
load_dotenv()

# Create and run the shopping assistant agent
agent = create_shopping_agent()
result = agent.invoke({
    "input": "Find the best price for a laptop"
})
```

### Tools

The shopping assistant agent provides three main tools:

1. **SearchProduct**: Searches for a product on a shopping website
   - Input: Search query (e.g., 'laptop')
   - Use this to find products based on a search query

2. **FilterResults**: Filters search results on a shopping website
   - Input: URL and filter criteria (e.g., 'price:low-to-high')
   - Use this to narrow down search results based on criteria

3. **ComparePrices**: Compares prices of products on two different shopping websites
   - Input: Two URLs (e.g., 'site1.com/product' and 'site2.com/product')
   - Use this to compare prices between different websites

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
- Additional tools for product reviews and ratings
- Integration with more shopping websites
- Enhanced filtering options
- Price tracking and alerts

## Ecommerce Agent

The ecommerce agent (`ecommerce_agent.py`) is a LangChain-based agent that can automate various e-commerce tasks such as product search, price comparison, stock checking, and cart management using Steel's managed browser infrastructure.

### Features

- 🔍 Search for products across multiple e-commerce sites
- 💲 Compare prices across different vendors
- 📦 Check product availability and stock levels
- 🛒 Add/remove items from shopping cart
- 🔄 Proper session management
- ⚡ Async support with Steel integration
- 🛡️ Error handling and retry logic

### Usage

```python
from dotenv import load_dotenv
load_dotenv()

# Create and run the ecommerce agent
agent = EcommerceAgent(api_key="your_api_key")
await agent.search_products("laptop")
```

### Tools

The ecommerce agent provides four main tools:

1. **ProductSearch**: Searches for products across multiple e-commerce sites
   - Input: Search query (e.g., 'laptop')
   - Use this to find products based on a search query

2. **PriceCompare**: Compares prices across different vendors
   - Input: Product URL
   - Use this to compare prices for a specific product

3. **StockCheck**: Checks product availability and stock levels
   - Input: Product URL
   - Use this to check if a product is in stock

4. **CartManagement**: Manages shopping cart by adding/removing items
   - Input: Action (add/remove) and Product URL
   - Use this to add or remove items from the shopping cart

### Output Format

The agent provides nicely formatted output with:
- 💭 Thoughts in blue
- ⚡ Actions in green
- 👁️ Observations in blue
- 💡 Final answers in yellow
- Clear section separators

### Environment Variables

Required environment variables:
- `API_KEY`: Your API key for the e-commerce platform

### Error Handling

The agent includes comprehensive error handling for:
- Missing API keys
- Invalid URLs
- Network errors
- Page load failures
- LLM parsing errors

### Future Improvements

Potential areas for enhancement:
- Additional tools for product reviews and ratings
- Integration with more e-commerce platforms
- Enhanced filtering options
- Price tracking and alerts

## Form Automation Agent

The form automation agent (`form_automation.py`) is a LangChain-based agent that can handle complex form filling tasks with validation and error recovery using Steel's managed browser infrastructure.

### Features

- 📝 Fill complex forms with dynamic field detection
- 🔄 Handle conditional fields based on previous selections
- ✅ Validate form data and handle errors
- 🔄 Proper session management
- ⚡ Async support with Steel integration
- 🛡️ Error handling and retry logic

### Usage

```python
from dotenv import load_dotenv
load_dotenv()

# Create and run the form automation agent
agent = FormAutomationAgent()
await agent.fill_complex_form(form_data={"url": "https://example.com/form", "name": "John Doe"})
```

### Tools

The form automation agent provides tools for:

1. **FillComplexForm**: Handles complex form filling with validation and error recovery
   - Input: Form data (e.g., {'url': 'https://example.com/form', 'name': 'John Doe'})
   - Use this to fill out and submit complex forms

### Output Format

The agent provides nicely formatted output with:
- 💭 Thoughts in blue
- ⚡ Actions in green
- 👁️ Observations in blue
- 💡 Final answers in yellow
- Clear section separators

### Environment Variables

Required environment variables:
- `API_KEY`: Your API key for the form automation platform

### Error Handling

The agent includes comprehensive error handling for:
- Missing API keys
- Invalid URLs
- Network errors
- Page load failures
- LLM parsing errors

### Future Improvements

Potential areas for enhancement:
- Additional tools for form validation and error handling
- Integration with more form platforms
- Enhanced field detection and matching
- Dynamic form handling

## Data Extraction Pipeline

The data extraction pipeline (`data_extraction.py`) is a LangChain-based agent that can extract structured data from web pages with pagination and transformation using Steel's managed browser infrastructure.

### Features

- 📄 Extract structured data from web pages
- 🔄 Handle pagination for multi-page data extraction
- 🔄 Transform and validate extracted data
- 🔄 Proper session management
- ⚡ Async support with Steel integration
- 🛡️ Error handling and retry logic

### Usage

```python
from dotenv import load_dotenv
load_dotenv()

# Create and run the data extraction pipeline
pipeline = DataExtractionPipeline()
data = await pipeline.extract_structured_data(urls=["https://example.com/data"], extraction_rules={"title": "h1"})
```

### Tools

The data extraction pipeline provides tools for:

1. **ExtractStructuredData**: Extracts structured data from web pages with pagination and transformation
   - Input: URLs, extraction rules, and optional pagination settings
   - Use this to extract and transform data from web pages

### Output Format

The pipeline provides nicely formatted output with:
- 💭 Thoughts in blue
- ⚡ Actions in green
- 👁️ Observations in blue
- 💡 Final answers in yellow
- Clear section separators

### Environment Variables

Required environment variables:
- `API_KEY`: Your API key for the data extraction platform

### Error Handling

The pipeline includes comprehensive error handling for:
- Missing API keys
- Invalid URLs
- Network errors
- Page load failures
- LLM parsing errors

### Future Improvements

Potential areas for enhancement:
- Additional tools for data transformation and validation
- Integration with more data extraction platforms
- Enhanced pagination handling
- Dynamic data extraction rules

## Advanced Authentication Handler

The advanced authentication handler (`auth_handler.py`) is a LangChain-based agent that can handle various authentication scenarios including multi-factor authentication (MFA) using Steel's managed browser infrastructure.

### Features

- 🔒 Handle OAuth, form-based, and token-based authentication
- 🔄 Handle multi-factor authentication (MFA)
- 🔄 Proper session management
- ⚡ Async support with Steel integration
- 🛡️ Error handling and retry logic

### Usage

```python
from dotenv import load_dotenv
load_dotenv()

# Create and run the advanced authentication handler
auth_handler = AdvancedAuthHandler(session_manager=SteelSessionManager(api_key="your_api_key"))
await auth_handler.handle_authentication(url="https://example.com/login", auth_type="oauth", credentials={"username": "user", "password": "pass"})
```

### Tools

The advanced authentication handler provides tools for:

1. **HandleAuthentication**: Handles various authentication scenarios including MFA
   - Input: URL, authentication type, credentials, and optional MFA handler
   - Use this to handle different authentication flows

### Output Format

The handler provides nicely formatted output with:
- 💭 Thoughts in blue
- ⚡ Actions in green
- 👁️ Observations in blue
- 💡 Final answers in yellow
- Clear section separators

### Environment Variables

Required environment variables:
- `API_KEY`: Your API key for the authentication platform

### Error Handling

The handler includes comprehensive error handling for:
- Missing API keys
- Invalid URLs
- Network errors
- Page load failures
- LLM parsing errors

### Future Improvements

Potential areas for enhancement:
- Additional tools for authentication flows
- Integration with more authentication platforms
- Enhanced MFA handling
- Dynamic authentication scenarios
