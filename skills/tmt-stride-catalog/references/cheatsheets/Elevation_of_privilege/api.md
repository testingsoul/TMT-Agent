# Elevation of Privilege — API test scenarios

API EoP tests should verify **resource-level authorization** and **role boundaries**, not just endpoint-level checks.

## Scenarios (Given/When/Then)
1. Vertical EoP (role boundary)
   ```gherkin
   Given a user token without admin scope
   When calling an admin action
   Then the API returns 403 and does not perform the action
   ```

2. Horizontal EoP (resource ownership)
   ```gherkin
   Given user A owns resource A1
   When user A calls `GET/PUT/DELETE` on resource B1
   Then access is denied and existence is not disclosed beyond policy
   ```

3. Indirect privilege via “confused deputy”
   ```gherkin
   Given service X calls service Y on behalf of a user
   When service X forwards its own service credentials incorrectly
   Then service Y enforces “actor vs caller” rules and denies privilege escalation
   ```

4. Admin-by-header / client-controlled roles
   ```gherkin
   Given requests can include headers/claims
   When a client sets `X-Role: admin` (or similar)
   Then the API ignores it and derives roles only from trusted identity sources
   ```

## Evidence to capture
- Authorization decisions include principal + resource + action.
- Tests prove “no side effects” for denied requests.

