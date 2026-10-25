# Information Disclosure — Database test scenarios

Information disclosure in databases is usually **excessive read access**, **misconfiguration**, or **leaky exports/backups**.

## Scenarios (Given/When/Then)
1. Read permissions minimal
   ```gherkin
   Given an application role
   When it queries sensitive tables/columns
   Then access is denied unless explicitly required
   ```

2. Multi-tenant isolation for reads
   ```gherkin
   Given tenant A and tenant B
   When tenant A queries data
   Then it never returns tenant B’s rows (RLS/policies verified)
   ```

3. Backups and snapshots protected
   ```gherkin
   Given backups exist
   When a non-privileged principal attempts to access them
   Then access is denied and audited
   ```

4. Search/index exposure checks (e.g., public endpoints)
   ```gherkin
   Given a search index or analytics store exists
   When accessed without proper authentication/network controls
   Then data is not readable and the exposure test fails the pipeline
   ```

## Evidence to capture
- Permissions matrix and “deny by default” results.
- Audit logs for backup access attempts.

