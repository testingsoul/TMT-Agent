# Spoofing — Web test scenarios

Spoofing on the web is about **pretending to be someone/something else** (users, sessions, devices, identity providers).

## Scenarios (Given/When/Then)
1. Session fixation / session swap
   ```gherkin
   Given a user logs in
   When the session identifier changes from an untrusted source (URL, referrer, or pre-set cookie)
   Then the app rejects it or regenerates a new session on login and keeps the user authenticated correctly
   ```

2. Authentication bypass via missing checks in UI-only flows
   ```gherkin
   Given an unauthenticated browser session
   When the user navigates directly to an authenticated page (deep link / route)
   Then the app redirects to login and does not render protected data
   ```

3. Weak “remember me” token handling
   ```gherkin
   Given a user enabled “remember me”
   When the remember token is reused after logout or password change
   Then the token no longer works and a fresh login is required
   ```

4. Login brute force / credential stuffing protection (web UX + backend)
   ```gherkin
   Given repeated failed login attempts for the same account
   When attempts exceed policy
   Then rate limiting / step-up verification triggers and security events are recorded
   ```

## Evidence to capture
- Server logs show auth failures + throttling decisions (no sensitive data).
- Session cookie flags: `HttpOnly`, `Secure`, `SameSite` appropriate to the app.
- Reproducible result in automated browser tests.

## Automation ideas
- Selenium/Playwright/Cypress for tests.
- Synthetic login tests in CI against a test environment (with rate limits tuned for CI).

