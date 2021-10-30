# Unittesting

## Mocking
### What are mocks?
- Test Stub: canned response to method calls
- Test Spy: real objects that behave like normal except when a specific condition is met
- Mock Object: verifies behavior (calls) to a method


### Eliminates dependencies in the CUT


### Verifies behavior (method that have no return value)

### Tests error handling

### Others
- Eliminate dependencies on database calls
  - speed up testing
- Reduce test complexity
  - Don't have to write complex logic to handle behavior or methods not under test
- Don't have to wait to implement other methods
