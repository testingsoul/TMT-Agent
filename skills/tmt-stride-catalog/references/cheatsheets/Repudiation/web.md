# Repudiation — Web test scenarios

Repudiation is about **a user denying actions** because evidence is missing, ambiguous, or untrustworthy.

## Scenarios (Given/When/Then)
1. Audit log completeness for critical actions
   ```gherkin
   Given a user performs a critical action (purchase, password change, data export)
   When the action succeeds
   Then an audit record exists with actor, timestamp, target, and correlation ID
   ```

2. Audit log integrity (no silent deletion)
   ```gherkin
   Given audit logs are enabled
   When an admin attempts to delete/modify audit records
   Then the system prevents it or records a separate immutable “audit of audit”
   ```

3. Session-to-action traceability
   ```gherkin
   Given a user session
   When multiple actions occur
   Then logs correlate actions to the session/request chain without storing secrets
   ```

4. Clear user feedback for sensitive actions
   ```gherkin
   Given a user changes a security setting
   When the change is applied
   Then the UI confirms the change and (optionally) sends a notification
   ```

## Evidence to capture
- Immutable audit trail entries and correlation IDs.
- Notification evidence (email/SMS event recorded, not message content).

