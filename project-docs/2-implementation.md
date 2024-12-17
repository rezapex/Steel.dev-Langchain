
# Breaking Down the Steel-LangChain Integration Project


This breakdown organizes the project into actionable steps, referencing the provided documentation and examples.

================================================================================
**I. Project Setup and Research (Day 1)**
================================================================================

1. **Set up Development Environment:**
    - Create a virtual environment.
    - Install required libraries: `langchain`, `steel-sdk`, `playwright`.
    - Clone the LangChain repository (for contributing later).

2. **Deep Dive into LangChain Loaders:**
    - Study the `browserbase` and `browserless` loaders for implementation patterns.  Pay close attention to:
        - `BaseLoader` inheritance.
        - Asynchronous loading (`aloud`).
        - Handling loader options (e.g., headless mode, viewport).
    - Examine the `youtube_transcript` loader for handling different data types.

3. **Familiarize with Steel SDK:**
    - Go through the Steel documentation, particularly:
        - Connecting with Playwright (Python): This is crucial for controlling the browser within Steel.
        - Intro to Steel: Understand core concepts and session management.

4. **Plan the Shopping Assistant Example:**
    - Decide on specific e-commerce sites for testing.
    - Define the scope of each tool (Product Search, Price Analysis, Review Analysis).  Consider realistic scenarios and potential challenges.

================================================================================
**II. Core Loader Implementation (Day 2)**
================================================================================

1. **Implement `SteelLoader`:**
    - [x] Create a new file (e.g., `steel_loader.py`) within the LangChain `document_loaders` directory.
    - [ ] Inherit from `langchain.document_loaders.BaseLoader`.
    - [ ] Implement `__init__` to initialize Steel connection parameters (API key, session ID, etc.).  Consider both self-hosted and Steel Cloud options.
    - [ ] Implement `aloud` to:
        - [ ] Establish a connection to Steel using the SDK.
        - [ ] Use Playwright through the Steel connection to navigate to the URL.
        - [ ] Extract the page content.
        - [ ] Handle potential errors (timeouts, network issues).
        - [ ] Close the Steel session.
    - [ ] Add support for common browser options (headless, viewport, wait_until).

2. **Initial Testing:**
    - Write unit tests to verify `SteelLoader` functionality.
    - Test with different websites and options.

**III. Shopping Assistant Tools (Day 3)**

1. **Implement `ProductSearchTool`:**
    - Create a new file for the tools (e.g., `shopping_tools.py`).
    - Inherit from `langchain.tools.BaseTool`.
    - Implement `_run` to:
        - Use `SteelLoader` to load the search results page.
        - Extract product information (title, price, URL, etc.) using Playwright selectors.
        - Format the results into a structured output (e.g., a list of dictionaries).
        - Handle pagination if necessary.

2. **Implement `PriceAnalysisTool` and `ReviewAnalysisTool`:**
    - Follow a similar pattern as `ProductSearchTool`, adapting the logic for price extraction and review analysis.

3. **Tool Testing:**
    - Write unit tests for each tool.
    - Test with various product URLs and search queries.

**IV. Agent Integration and Testing (Day 4)**

1. **Integrate Tools with LangChain Agent:**
    - Use `initialize_agent` with the created tools, a suitable LLM (e.g., `ChatOpenAI`), and an appropriate agent type.

2. **Develop Conversation Flows:**
    - Define specific user queries and expected agent responses.
    - Test the agent with these queries.

3. **Implement Error Handling and Retries:**
    - Add robust error handling within the tools and agent.
    - Implement retry logic for transient errors (e.g., network issues).

4. **Integration Testing:**
    - Conduct end-to-end tests to verify agent behavior in different scenarios.
    - Test error handling and retry mechanisms.

**V. Documentation and Demo (Day 5)**

1. **Write the Tutorial:**
    - Create a step-by-step guide for building the shopping assistant.
    - Include clear code examples and explanations.
    - Add testing instructions.

2. **Update README:**
    - Add installation instructions.
    - Write a quick start guide.
    - Provide an architecture overview.
    - Include usage examples.

3. **Create Demo Video/GIF:**
    - Record a terminal session showcasing the shopping assistant in action.
    - Highlight key features and functionalities.

4. **Prepare for Project Review:**
    - Organize your code and documentation.
    - Prepare a brief presentation to walk through the implementation.


This breakdown provides a structured approach to tackling the project within the given timeframe. Remember to prioritize the core functionality and documentation, focusing on delivering a working integration and a clear understanding of how to use it. The shopping assistant example serves as a demonstration of the integration's capabilities.  Adjust the scope and focus based on your progress and the feedback you receive. Remember to communicate regularly with the Steel team.


---

Reference: 

## Langchain
[Langchain Document Loader PR repo](https://github.com/langchain-ai/langchain/tree/fa0618883493cf6a1447a73b66cd10c0f028e09b/libs/community/langchain_community/document_loaders)
[Langchain Python Playwright Agent](https://python.langchain.com/docs/integrations/tools/playwright/#use-within-an-agent)
[Langchain youtube_transcript](https://python.langchain.com/docs/integrations/document_loaders/youtube_transcript)
[Langchain BrowserbaseLoader](https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.browserbase.BrowserbaseLoader.html#langchain_community.document_loaders.browserbase.BrowserbaseLoader)

## Steel
[Steel Get started](https://docs.steel.dev/overview/intro-to-steel)
[Steel SDK](https://pypi.org/project/steel-sdk/)
[Steel Python Playwright](https://docs.steel.dev/overview/guides/connect-with-playwright-python)

[Personal Fork](https://github.com/rezapex/langchain/tree/add_steel_loader)
