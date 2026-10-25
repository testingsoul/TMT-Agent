# Information Disclosure — Web test scenarios

Information disclosure is about **data exposure**: content, metadata, errors, caches, and unintended access.

## Scenarios (Given/When/Then)
1. Access control on profile and documents
   ```gherkin
   Given user A and user B exist
   When user A attempts to view user B’s private page/document
   Then access is denied and no sensitive content is rendered
   ```

2. Sensitive data in HTML/JS payloads
   ```gherkin
   Given an authenticated page loads
   When inspecting the response payload
   Then it does not include secrets (tokens, API keys) or unnecessary PII
   ```

3. Cache-control for sensitive pages
   ```gherkin
   Given a page with personal data
   When served via browser/proxy
   Then headers prevent unintended caching where required
   ```

4. Error handling doesn’t leak internals
   ```gherkin
   Given invalid input triggers an error
   When an error page/JSON is returned
   Then it does not include stack traces, internal hostnames, or query details
   ```

## Evidence to capture
- Responses show correct redaction and caching headers.
- Negative tests confirm “no PII in logs” for common failures.

