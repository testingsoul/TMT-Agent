# Information Disclosure — API test scenarios

Information disclosure for APIs includes **overly verbose responses**, **metadata leaks**, and **misconfigured endpoints**.

## Scenarios (Given/When/Then)
1. Over-fetching / excessive fields
   ```gherkin
   Given an endpoint returns user data
   When called by a standard user role
   Then it returns only allowed fields (no internal IDs, no secrets, no admin-only data)
   ```

2. Enumeration resistance
   ```gherkin
   Given a resource ID that doesn’t belong to the caller
   When requested
   Then the API responds consistently (403/404 policy) without confirming existence
   ```

3. Debug endpoints disabled
   ```gherkin
   Given non-production debug endpoints exist
   When running in production mode
   Then debug endpoints are unavailable and configuration is validated in CI
   ```

4. Secrets not returned in error bodies
   ```gherkin
   Given a downstream failure occurs
   When the API returns an error
   Then it does not include credentials, connection strings, or raw upstream bodies
   ```

## Evidence to capture
- Response schema assertions per role.
- Production config checks preventing debug flags.

