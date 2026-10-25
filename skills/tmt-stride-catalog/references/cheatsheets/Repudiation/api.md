# Repudiation — API test scenarios

Repudiation for APIs is mainly **observability + evidence**: who did what, when, and from where.

## Scenarios (Given/When/Then)
1. Correlation IDs propagated
   ```gherkin
   Given an incoming API request
   When it triggers downstream calls
   Then the same correlation ID is propagated and appears in logs/traces
   ```

2. Audit events for privileged endpoints
   ```gherkin
   Given an admin endpoint (role/permission changes)
   When called successfully
   Then an audit event is recorded with actor identity and change diff summary
   ```

3. Non-repudiation for critical integrations (when required)
   ```gherkin
   Given a partner integration uses signed callbacks/webhooks
   When a callback is received
   Then signature verification results are recorded and failures are traceable
   ```

4. “No side effects” on rejected requests
   ```gherkin
   Given an unauthorized request
   When it is rejected
   Then no audit event claims it succeeded and no data changes occurred
   ```

## Evidence to capture
- Structured security events (authz decision, resource, action).
- Trace links for requests spanning services.

