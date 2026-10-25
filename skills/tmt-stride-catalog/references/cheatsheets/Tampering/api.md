# Tampering — API test scenarios

Tampering for APIs centers on **request manipulation** and **data integrity**.

## Scenarios (Given/When/Then)
1. IDOR via parameter tampering
   ```gherkin
   Given a user has access to resource `A`
   When they request resource `B` by changing the ID
   Then the API returns 403/404 and does not leak whether `B` exists
   ```

2. Mass assignment / over-posting
   ```gherkin
   Given an endpoint accepts a JSON body
   When the client includes fields that should be server-controlled (e.g., `role`, `isAdmin`)
   Then the API ignores/rejects them and records a validation event
   ```

3. Signature/HMAC validation (if used)
   ```gherkin
   Given a signed request body
   When a single byte is modified in transit
   Then the API rejects the request and produces a clear “invalid signature” outcome
   ```

4. Concurrency/race on state changes
   ```gherkin
   Given two near-simultaneous updates
   When requests arrive out of order
   Then optimistic locking/version checks prevent lost updates or inconsistent state
   ```

## Evidence to capture
- Authorization + validation outcomes, correlation IDs, version numbers.
- Data consistency checks (no partial updates).

