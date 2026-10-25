# Denial of Service — API test scenarios

API DoS defenses should prove that **abuse degrades gracefully** and doesn’t cause cascading failures.

## Scenarios (Given/When/Then)
1. Per-client quotas
   ```gherkin
   Given a single client sends a burst of requests
   When it exceeds quota
   Then the API returns 429 (or policy) and protects shared capacity
   ```

2. Timeouts and circuit breakers
   ```gherkin
   Given a downstream dependency is slow
   When the API calls it
   Then timeouts/circuit breakers prevent thread/connection exhaustion
   ```

3. Pagination and query cost limits
   ```gherkin
   Given list/search endpoints
   When the client requests extreme page sizes or deep offsets
   Then the API enforces limits and returns a safe error or capped results
   ```

4. GraphQL complexity limits (if applicable)
   ```gherkin
   Given a complex query
   When complexity exceeds threshold
   Then the API rejects it and returns guidance for safe usage
   ```

## Evidence to capture
- Load test results + dashboards demonstrating graceful degradation.
- Dependency health and fallback behavior in traces.

