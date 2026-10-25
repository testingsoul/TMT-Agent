# Spoofing — API test scenarios

Spoofing for APIs focuses on **identity and trust boundaries**: tokens, signatures, clients, and mTLS.

## Scenarios (Given/When/Then)
1. Invalid/expired token
   ```gherkin
   Given an API request with an invalid or expired token
   When calling a protected endpoint
   Then the API returns 401/403 and emits an authentication failure event
   ```

2. Token audience/scope misuse
   ```gherkin
   Given a token intended for service A (audience/scope)
   When used against service B
   Then access is denied and the request is not processed
   ```

3. Missing authorization checks (authn vs authz)
   ```gherkin
   Given a valid token for a normal user
   When calling an admin-only endpoint
   Then the API returns 403 and no privileged action is performed
   ```

4. Replay protection for signed requests (if applicable)
   ```gherkin
   Given a valid signed request
   When the same request is replayed outside the allowed time window / nonce policy
   Then the API rejects it and records a replay attempt
   ```

5. Client identity validation (mTLS / API keys)
   ```gherkin
   Given an API key for app X
   When used from an unapproved client context (wrong mTLS cert / wrong org / wrong environment)
   Then requests are denied and alerted
   ```

## Evidence to capture
- Status codes, security event records, and correlation IDs.
- Authorization decision details (without leaking secrets).

## Automation ideas
- Contract tests that assert 401/403 behavior.
- Negative tests that verify “no side effects” (no rows changed, no messages published).

