# Elevation of Privilege — Database test scenarios

Database EoP is about **gaining more privileges** (roles, grants) or **executing privileged operations** via misconfiguration.

## Scenarios (Given/When/Then)
1. Runtime roles cannot grant privileges
   ```gherkin
   Given an application runtime role
   When it attempts `GRANT`, role switches, or superuser actions
   Then the operation is denied and audited
   ```

2. Separation of duties for migrations
   ```gherkin
   Given schema migrations exist
   When running in production
   Then only a dedicated migration role can apply DDL, not the runtime app role
   ```

3. Dangerous functions disabled or restricted
   ```gherkin
   Given the database supports admin-only functions/procedures
   When a low-privilege role calls them
   Then access is denied and logged
   ```

4. Stored procedure ownership checks
   ```gherkin
   Given stored procedures exist
   When invoked with user-controlled parameters
   Then execution context does not elevate privileges unexpectedly (definer/invoker verified)
   ```

## Evidence to capture
- Role/privilege tests executed in CI against an ephemeral DB.
- Audit trails for denied privilege changes.

