# Elevation of Privilege — Web test scenarios

EoP is about **gaining capabilities beyond what the user should have** (vertical) or **acting as another user** (horizontal).

## Scenarios (Given/When/Then)
1. Horizontal privilege escalation (IDOR via web routes)
   ```gherkin
   Given user A is logged in
   When user A attempts to access user B’s settings page by changing the URL
   Then access is denied and no data is shown
   ```

2. Vertical privilege escalation via UI-only checks
   ```gherkin
   Given a standard user role
   When the user triggers an admin action via direct request (not via UI)
   Then the server denies it and records an authorization failure
   ```

3. Role changes require re-auth / step-up
   ```gherkin
   Given a user wants to enable a sensitive feature
   When they attempt it without recent authentication
   Then the app requires step-up auth and records the event
   ```

4. Admin panels protected by multiple controls
   ```gherkin
   Given an admin route exists
   When accessed without admin privileges
   Then it’s blocked even if the route is known/bookmarked
   ```

## Evidence to capture
- Consistent 403 behavior and “no side effects”.
- Audit event for denied privileged actions (without leaking details).

