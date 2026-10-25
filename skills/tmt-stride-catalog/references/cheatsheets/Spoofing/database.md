# Spoofing — Database test scenarios

Spoofing for databases often appears as **using the wrong identity** (shared accounts, missing attribution) or **bypassing identity controls**.

## Scenarios (Given/When/Then)
1. Shared credentials / no attribution
   ```gherkin
   Given multiple applications/users access the database
   When queries are executed
   Then activity is attributable (distinct DB users/roles, or strong app-level identity in logs)
   ```

2. Least-privilege roles enforced
   ```gherkin
   Given an application role intended to be read-only
   When it attempts to write/update/delete
   Then the database denies the operation and logs the authorization failure
   ```

3. Connection without encryption (where required)
   ```gherkin
   Given a client attempts a plaintext connection
   When connecting to the database
   Then the connection is refused or upgraded to TLS per policy
   ```

4. Service identity separation by environment
   ```gherkin
   Given a staging credential
   When used to connect to production
   Then authentication fails and the access attempt is recorded
   ```

## Evidence to capture
- Database audit logs mapping actions to roles/users.
- IAM/credential policies showing environment separation.

## Automation ideas
- Integration tests using dedicated low-privilege DB roles.
- Policy-as-code checks for DB users/roles and TLS requirements.

