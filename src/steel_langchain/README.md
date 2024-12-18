# Steel LangChain Core Library

This directory contains the core implementation of the Steel LangChain integration.

## Components

### WebLoader (`web_loader.py`)

The main loader class that integrates Steel's browser infrastructure with LangChain's document loader interface.

Key features:
- Multiple content extraction strategies
- Session management
- Proxy support
- CAPTCHA solving
- Async capabilities

### Session Manager (`session_manager.py`)

Handles Steel browser session lifecycle management.

Features:
- Session creation and cleanup
- Resource management
- Error handling
- Event loop integration

### Cleanup Sessions (`cleanup_sessions.py`)

Utility for managing and cleaning up Steel browser sessions.

Features:
- Automatic session cleanup
- Resource release
- Signal handling

## Architecture

The library follows these design principles:

1. **Resource Management**
   - Proper cleanup of browser sessions
   - Memory-efficient operations
   - Event loop handling

2. **Error Handling**
   - Comprehensive error types
   - Graceful degradation
   - Informative error messages

3. **Async Support**
   - Native async/await support
   - Event loop management
   - Concurrent operations

4. **Integration Points**
   - LangChain document loader interface
   - Steel browser automation
   - Event system integration

## Development Guidelines

When contributing to the core library:

1. **Error Handling**
   - Always use custom error types
   - Provide context in error messages
   - Handle cleanup in error cases

2. **Documentation**
   - Document all public interfaces
   - Include usage examples
   - Explain error conditions

3. **Testing**
   - Write unit tests for new features
   - Include integration tests
   - Test error conditions

4. **Performance**
   - Consider memory usage
   - Implement lazy loading where appropriate
   - Clean up resources properly

## Future Improvements

Areas for enhancement:

1. **Content Extraction**
   - Additional extraction strategies
   - Custom extraction rules
   - Content transformation pipelines

2. **Session Management**
   - Session pooling
   - Automatic scaling
   - Health monitoring

3. **Integration**
   - Additional LangChain components
   - New Steel features
   - Extended browser capabilities
