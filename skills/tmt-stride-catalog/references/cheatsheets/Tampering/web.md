# Tampering — Web test scenarios

Tampering is about **unauthorized modification** of data, requests, or UI-driven workflows.

## Scenarios (Given/When/Then)
1. Hidden field manipulation
   ```gherkin
   Given the UI includes hidden fields (price, discount, role, plan)
   When a user changes hidden field values before submit
   Then the backend recalculates/validates server-side and ignores client-supplied authority values
   ```

2. File upload tampering
   ```gherkin
   Given a file upload feature
   When a user uploads an unexpected file type or oversized file
   Then the system rejects it safely and stores no unvalidated content
   ```

3. Integrity of client-side state
   ```gherkin
   Given the app uses client-side state (localStorage/sessionStorage) for UX
   When that state is altered
   Then privileged behavior does not change unless server-side authorization allows it
   ```

## Evidence to capture
- “No side effects” confirmation (data unchanged).
- Validation error responses without leaking internals.

## Automation ideas
- API-level tests for request tampering behind the UI.
- Property-based tests for input validation boundaries.

