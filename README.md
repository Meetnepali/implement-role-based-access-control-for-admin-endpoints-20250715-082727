# Guide to the Project

## Task Overview
Extend an existing FastAPI app to provide secure endpoints for authenticated users to **retrieve and update their own profile** (fields: `name`, `email`, `age`, `bio`). All storage is in-memory; assume authentication is already handled by the provided dependency. **Focus on input validation, error handling, and user field restrictions.**

### Requirements
- Implement GET `/user/profile` to retrieve only the current user's profile.
- Implement PUT `/user/profile` to allow partial updates to own profile fields.
- All input must be validated using Pydantic, including:
  - Email must be valid.
  - Age must be between 18 and 120 (inclusive).
- On validation failure, return a **structured custom error response** (not FastAPI's default), with appropriate HTTP status.
- Error response should make it clear which fields failed and why.
- Use an in-memory dictionary for user data.
- Authentication is mocked (see provided dependency, do not implement).
- Use only Python standard lib and FastAPI built-in features.

## What is Expected
- Extend the application by implementing the above endpoints and ensure validation rules are enforced.
- Use Pydantic models and FastAPI dependency injection correctly.
- Give meaningful, structured validation error messages (not generic 400 or 422 from FastAPI/Pydantic).
- Only allow the authenticated user to access/update their own profile.

## Restrictions
- Do **NOT** implement login, registration, password reset, or full authentication flows.
- Do **NOT** use a database or any storage beyond the in-memory dictionary.
- Do **NOT** change the authentication mechanism; just use the dependency provided.
- Do **NOT** change project structure or add unrelated files/modules.
- All modifications must target ONLY profile retrieval and update.

## Verifying Your Solution
- Make GET and PUT requests as the authenticated user (see sample curl commands in the code comments).
- Confirm you receive your own user profile and can update permitted fields.
- Intentionally send invalid input (e.g., `bademail`, `age: 17`) and verify that a **clear, structured error response** is returned with detail messages and correct status codes.
- Profile changes should persist only in the running server's memory (not across restarts).
- Review that only the current user is affected when updating and that all responses use robust, appropriate schemas and error formats.
