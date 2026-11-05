# Tests and production code

Read before removing test-only code from production or fixing a test that leans on a mock. This is about keeping production code honest; for writing tests or test-first work use `tdd`.

## Test-only code in production

The scanner doesn't find these. Search for them:

```bash
rg -n "NODE_ENV.{0,12}test|isTest|IS_TEST|__TEST__|forTesting|testOnly|_for_test"
```

Also look for methods only test files call (a `reset()` or `destroy()` production never uses), exports added so a test can reach an internal, and fake data or stub clients returned when a real dependency is missing.

Fix by testing observable behaviour through the public interface. Move builders, cleanup and doubles into test utilities. When a test needs isolation, inject the dependency through an argument or constructor parameter that production would also use, and let the test pass its own double.

## Testing the mock

```ts
// Passes because the mock rendered, not because the code works
expect(screen.getByTestId("sidebar-mock")).toBeInTheDocument();
```

Delete the assertion or unmock the part. Assert on what the unit does with the double in place; a call count on a mock is rarely enough on its own.

## Mocking the wrong layer

Mocking a high-level method can drop a side effect the test depends on, such as a config write that a duplicate check reads, so the test passes or fails for the wrong reason. Mock the slow or external edge underneath and keep the real effects. "Mock it to be safe" is not a reason.

## Incomplete mocks

A response mock with only the fields the test reads hides what downstream code consumes, so the test passes while integration fails. Build it from the same type or schema the production code parses with, or from a recorded response.

When mock setup is longer than the test, an integration test against the real component is usually simpler.
