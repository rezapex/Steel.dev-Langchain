# Steel LangChain Tests

This directory contains the test suite for the Steel LangChain integration.

## Test Structure

### Loader Tests (`test_loader.py`)

Tests for the core WebLoader functionality:
- Content extraction
- Session management
- Error handling
- Resource cleanup

## Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests/test_loader.py

# Run with coverage
coverage run -m unittest discover tests
coverage report
```

## Writing Tests

When adding new tests:

1. **Test Organization**
   - Group related tests in classes
   - Use descriptive test names
   - Follow the AAA pattern (Arrange, Act, Assert)

2. **Test Coverage**
   - Test happy paths
   - Test error conditions
   - Test edge cases
   - Test resource cleanup

3. **Mocking**
   - Mock external services (Steel API)
   - Mock browser interactions
   - Mock network requests
   - Provide realistic test data

4. **Documentation**
   - Document test purpose
   - Document test requirements
   - Document any special setup

## Test Categories

1. **Unit Tests**
   - Test individual components
   - Mock dependencies
   - Fast execution

2. **Integration Tests**
   - Test component interaction
   - Limited mocking
   - Real Steel sessions

3. **End-to-End Tests**
   - Test complete workflows
   - Real external services
   - Full browser automation

## Best Practices

1. **Test Independence**
   - Tests should not depend on each other
   - Clean up after each test
   - Use fresh fixtures

2. **Test Performance**
   - Keep tests fast
   - Minimize external calls
   - Use appropriate mocking

3. **Test Maintenance**
   - Keep tests simple
   - Update tests with code changes
   - Remove obsolete tests

## Continuous Integration

The test suite is integrated with CI/CD:
- Runs on pull requests
- Runs on main branch pushes
- Reports coverage metrics
- Enforces minimum coverage
