# Add Unit Tests for the JSON Loader

Scope:
- Add unit tests for the JSON loader and input validation rules.
- Cover at least the following scenarios: valid input, missing required fields, malformed JSON, and unsupported values where relevant.

Requirements:
- Use the existing Python test setup and keep tests focused on loader behavior.
- Verify that valid JSON input loads successfully and returns the expected normalized data structure.
- Verify that missing required fields raise a clear, actionable validation error.
- Verify that malformed JSON raises a parsing error or validation failure with a useful message.
- Include assertions for the exact error handling that the application should provide.
- Keep the tests small, deterministic, and easy to run locally.

Output requirements:
- Add or update the relevant test file(s) in the project.
- Write concise, professional test cases that describe the scenario being validated.
- Ensure the tests can be executed with the project’s existing Python test command.
