# Denial of Service — Database test scenarios

Database DoS is often **query cost abuse**, **lock contention**, or **connection pool exhaustion**.

## Scenarios (Given/When/Then)
1. Connection limits and pooling behavior
   ```gherkin
   Given many concurrent requests
   When connections approach limits
   Then the app queues/rejects safely and the DB remains stable
   ```

2. Query timeouts
   ```gherkin
   Given an expensive query pattern
   When executed
   Then timeouts/cost limits stop it and the system returns a controlled error
   ```

3. Lock contention handling
   ```gherkin
   Given two conflicting transactions
   When a lock is held too long
   Then deadlock/lock-timeout policies prevent global impact and are observable
   ```

4. Index and maintenance protections
   ```gherkin
   Given a critical table grows
   When queries run at scale
   Then indexes/partitioning strategy prevents full scans in common paths (verified via explain plans in test env)
   ```

## Evidence to capture
- Pool metrics, slow query logs, lock wait metrics.
- Explain plan baselines for critical queries (in non-prod).

