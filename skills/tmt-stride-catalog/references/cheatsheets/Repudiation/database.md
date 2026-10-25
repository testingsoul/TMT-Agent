# Repudiation — Database test scenarios

Repudiation in databases is about **proving who changed what** and preventing “untraceable” writes.

## Scenarios (Given/When/Then)
1. Audit logging enabled for writes and DDL
   ```gherkin
   Given write and schema operations
   When they occur
   Then audit records include user/role, query type, timestamp, and source (app/service)
   ```

2. Privileged access monitored
   ```gherkin
   Given a high-privilege role exists
   When it is used for direct access
   Then access is logged, alerted, and time-bound (JIT access where possible)
   ```

3. Change attribution in multi-tenant systems
   ```gherkin
   Given tenant-scoped data
   When updates happen
   Then audit fields (who/when) are set consistently and cannot be overwritten by clients
   ```

## Evidence to capture
- Database audit logs and immutable storage controls.
- JIT access records / approvals (where applicable).

