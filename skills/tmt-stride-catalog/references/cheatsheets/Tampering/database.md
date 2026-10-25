# Tampering — Database test scenarios

Tampering in databases includes **unauthorized writes**, **schema/config changes**, or **integrity violations**.

## Scenarios (Given/When/Then)
1. Row-level authorization (where applicable)
   ```gherkin
   Given a multi-tenant database
   When a tenant tries to update another tenant’s row
   Then the update is denied (RLS/policies) and logged
   ```

2. Integrity constraints enforced
   ```gherkin
   Given referential integrity rules
   When a write attempts to create orphan records or inconsistent references
   Then the database rejects it and no partial write persists
   ```

3. Unauthorized schema changes
   ```gherkin
   Given a runtime application role
   When it attempts `ALTER TABLE` / index creation / privilege grants
   Then the operation is denied and audited
   ```

4. Backups/restore integrity
   ```gherkin
   Given backups exist
   When a restore is performed in a test environment
   Then checksums/validation confirm backups were not corrupted or altered
   ```

## Evidence to capture
- Audit logs for DDL attempts and denied operations.
- Constraint violation outcomes and rollback behavior.

