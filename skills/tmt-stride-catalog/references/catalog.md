# TMT Scenario Catalog

Stable IDs for every scenario in [TMT-CheatSheets](https://github.com/testingsoul/TMT-CheatSheets)
(vendored in `cheatsheets/`, upstream commit `eaabf3d`, 2026-03-01).

**ID format:** `<STRIDE>-<SYSTEM>-<NN>`, where STRIDE ∈ `S T R I D E` and SYSTEM ∈ `WEB API DB OTH`.
For `OTH` the suffix is a short slug (`S-OTH-K8S`) instead of a number.

Each row says:
- **Applies when**: what the system must contain for the scenario to be relevant. If that's absent, mark the scenario `not_applicable` and say why.
- **Covered when a test…**: the minimum assertions a test needs before it counts as `covered`. A test that exercises the scenario but skips the **outcome**, the **no side effects** check, or the **evidence** check is `partial`.
- **Hints**: grep seeds for finding candidate tests. They only point to candidates. Read the test before you classify it.

The three TMT assertions (from the cheat sheets' "Evidence to capture"):
1. **Outcome**: the control rejects or handles the attack (status code, exception, denied decision).
2. **No side effects**: state is unchanged after a rejected action (no rows written, no message published, no file stored).
3. **Evidence**: the system records it (security/audit event, log line, metric, alert), without leaking secrets.

---

## S — Spoofing

| ID | Scenario | Applies when | Covered when a test… | Hints |
|---|---|---|---|---|
| S-WEB-01 | Session fixation / session swap | Server-side sessions or session cookies | sets a known session ID before login and asserts a **new** ID is issued after login; old ID rejected | `session`, `fixation`, `regenerate`, `Set-Cookie` |
| S-WEB-02 | Auth bypass via UI-only flows | Web routes behind login | calls protected routes/backing endpoints **directly** (no UI navigation) unauthenticated and asserts redirect/401 | `login_required`, `authenticated`, `redirect`, `302`, `401` |
| S-WEB-03 | Weak "remember me" token | Persistent login feature | asserts token is random/opaque, rotated on use, invalidated on logout/password change | `remember`, `persistent`, `rotate`, `logout` |
| S-WEB-04 | Brute force / credential stuffing | Password login | sends N failed logins and asserts throttling/lockout/captcha **and** an auth-failure event | `rate`, `throttle`, `lockout`, `429`, `attempts` |
| S-API-01 | Invalid/expired token | API with protected endpoints | sends expired, malformed, wrong-signature or `alg:none` tokens and asserts 401/403 + auth-failure event | `expired`, `jwt`, `exp`, `signature`, `401` |
| S-API-02 | Token audience/scope misuse | Multiple services/audiences or scoped tokens | uses a token minted for another audience/scope and asserts denial with no processing | `aud`, `audience`, `scope`, `issuer` |
| S-API-03 | Authn vs authz confusion | Roles/permissions exist | uses a **valid** low-privilege token on an admin endpoint and asserts 403 + no privileged action | `admin`, `role`, `403`, `forbidden` |
| S-API-04 | Replay of signed requests | Signed requests, webhooks, nonces/timestamps | replays a valid signed request outside the window / with reused nonce and asserts rejection + replay event | `nonce`, `timestamp`, `replay`, `webhook`, `hmac` |
| S-API-05 | Client identity (mTLS / API keys) | API keys, mTLS, client credentials | uses a key from the wrong client/org/environment and asserts denial + alert | `api_key`, `x-api-key`, `mtls`, `client_cert` |
| S-DB-01 | Shared credentials / no attribution | App connects to a DB | asserts each service/user uses a distinct DB identity, and audit records map actions to it | `DATABASE_URL`, `user=`, `role`, `audit` |
| S-DB-02 | Least-privilege roles | App connects to a DB | connects as the runtime role and asserts DDL/out-of-scope tables are denied | `GRANT`, `REVOKE`, `permission denied`, `role` |
| S-DB-03 | Unencrypted connections | DB over network where TLS is required | asserts a non-TLS connection is refused / `sslmode=require`+ enforced | `sslmode`, `ssl`, `tls`, `require_secure_transport` |
| S-DB-04 | Service identity per environment | Multiple environments | asserts prod credentials/identities are not usable from non-prod config | `env`, `staging`, `prod`, `credentials` |
| S-OTH-MOBILE | Mobile identity | Mobile client | device-bound tokens, root/jailbreak signals, refresh-token rotation tests | `refresh_token`, `device`, `jailbreak` |
| S-OTH-MQ | Queue publisher/consumer identity | Message broker | asserts unauthorized publisher/consumer is rejected per topic, DLQ permissions | `publish`, `consume`, `topic`, `acl` |
| S-OTH-K8S | K8s service accounts | Kubernetes manifests | SA token scope, RBAC impersonation, namespace isolation checks | `serviceAccount`, `automountServiceAccountToken`, `impersonate` |
| S-OTH-LLM | LLM instruction identity | LLM/agent features | asserts untrusted content (docs, tool output, users) cannot act as system instructions; tool calls authorized per caller | `prompt`, `system`, `tool`, `injection` |

## T — Tampering

| ID | Scenario | Applies when | Covered when a test… | Hints |
|---|---|---|---|---|
| T-WEB-01 | Hidden field manipulation | Forms with hidden/derived fields (price, role, user_id) | submits modified hidden fields and asserts server rejects/ignores them + data unchanged | `hidden`, `price`, `form`, `csrf` |
| T-WEB-02 | File upload tampering | File uploads | uploads wrong MIME/magic bytes, oversize, path-traversal names, polyglots; asserts rejection + nothing stored | `upload`, `multipart`, `content_type`, `filename` |
| T-WEB-03 | Client-side state integrity | State in cookies/localStorage/JWT client-side | modifies client state and asserts server detects tampering (signature/HMAC) | `cookie`, `signed`, `localStorage`, `itsdangerous` |
| T-API-01 | IDOR via parameter tampering | Resources addressed by ID | user A modifies/reads user B's resource by ID and asserts 403/404 + B's data unchanged | `/{id}`, `other_user`, `owner`, `idor` |
| T-API-02 | Mass assignment / over-posting | Create/update endpoints binding request bodies | sends extra fields (`role`, `is_admin`, `owner_id`, `balance`) and asserts they're ignored/rejected | `is_admin`, `role`, `extra`, `forbid`, `allow_unknown` |
| T-API-03 | Signature/HMAC validation | Signed payloads/webhooks | alters one byte of a signed payload and asserts rejection | `hmac`, `signature`, `X-Signature`, `verify` |
| T-API-04 | Concurrency/race on state changes | Balances, inventory, single-use tokens, workflows | fires concurrent requests and asserts invariants hold (no double-spend, optimistic-lock conflict) | `concurrent`, `race`, `version`, `etag`, `If-Match`, `asyncio.gather` |
| T-DB-01 | Row-level authorization | Multi-tenant or per-user rows | asserts queries/policies restrict writes to the owning tenant/user (RLS or repository filters) | `tenant_id`, `RLS`, `POLICY`, `owner_id` |
| T-DB-02 | Integrity constraints enforced | Relational schema | asserts DB rejects invalid data (FK, unique, check, not-null) independent of app validation | `IntegrityError`, `constraint`, `unique`, `foreign key` |
| T-DB-03 | Unauthorized schema changes | Migrations | asserts runtime role cannot run DDL; migrations reviewed/applied by separate identity | `ALTER`, `DROP`, `migration`, `DDL` |
| T-DB-04 | Backup/restore integrity | Backups exist | restore test verifies checksum/consistency | `backup`, `restore`, `checksum` |
| T-OTH-CICD | Build artifact integrity | CI/CD pipelines | artifact signing, provenance verification, config drift checks | `cosign`, `sigstore`, `slsa`, `provenance` |
| T-OTH-IAC | IaC change control | Terraform/CloudFormation/Pulumi/Helm | policy checks on PR (OPA/Conftest/Checkov), drift detection | `conftest`, `checkov`, `tfsec`, `opa` |
| T-OTH-MQ | Event integrity | Message broker / events | schema validation of events, tamper-evident headers, DLQ policy | `schema`, `avro`, `jsonschema`, `dead_letter` |
| T-OTH-LLM | LLM tool-call tampering | LLM tool use | tool-call parameter validation, output constraints, guardrail regression tests | `tool_call`, `guardrail`, `validate` |

## R — Repudiation

| ID | Scenario | Applies when | Covered when a test… | Hints |
|---|---|---|---|---|
| R-WEB-01 | Audit log completeness | Critical user actions (payments, profile/email/password change, deletes) | performs the action and asserts an audit entry with actor, action, target, timestamp | `audit`, `log`, `event`, `actor` |
| R-WEB-02 | Audit log integrity | Audit storage exists | asserts audit entries can't be updated/deleted by app roles (append-only) | `append`, `immutable`, `delete audit` |
| R-WEB-03 | Session-to-action traceability | Sessions + audit | asserts audit entries carry session/correlation ID linking to the authenticated principal | `session_id`, `correlation`, `request_id` |
| R-WEB-04 | User feedback for sensitive actions | Sensitive account actions | asserts a notification event is recorded (not its contents) on email/password/MFA changes | `notify`, `email`, `sms`, `notification` |
| R-API-01 | Correlation IDs propagated | Multi-service or async calls | asserts incoming/generated correlation ID is returned and forwarded downstream | `X-Request-ID`, `traceparent`, `correlation` |
| R-API-02 | Audit events for privileged endpoints | Admin/privileged endpoints | calls a privileged endpoint (allowed **and** denied) and asserts structured event: principal, resource, action, decision | `audit`, `security_event`, `decision` |
| R-API-03 | Non-repudiation for integrations | Contractual/financial integrations | asserts signed receipts or signed request logging | `receipt`, `sign`, `non-repudiation` |
| R-API-04 | No side effects on rejection | Any rejecting control | asserts rejected requests leave no persisted change/messages **and** the rejection is logged | `rollback`, `count()`, `assert_not_called` |
| R-DB-01 | Audit logging for writes and DDL | DB in scope | asserts DB/app audit captures writes and DDL | `pgaudit`, `audit`, `trigger` |
| R-DB-02 | Privileged access monitored | Human/admin DB access | asserts privileged sessions are logged / JIT access recorded | `superuser`, `jit`, `break-glass` |
| R-DB-03 | Change attribution (multi-tenant) | Multi-tenant data | asserts rows record `created_by`/`updated_by` + tenant | `created_by`, `updated_by`, `modified_by` |
| R-OTH-SERVERLESS | Serverless traceability | Lambdas/functions | invocations carry request ID + principal | `context.aws_request_id`, `invocation` |
| R-OTH-PIPELINE | Data lineage | ETL/data pipelines | lineage and job-run audit events | `lineage`, `job_run`, `openlineage` |
| R-OTH-K8S | K8s audit | Kubernetes | audit policy covers `exec`, secret reads, RBAC changes | `audit-policy`, `exec`, `secrets` |

## I — Information disclosure

| ID | Scenario | Applies when | Covered when a test… | Hints |
|---|---|---|---|---|
| I-WEB-01 | Access control on profile/documents | User-owned pages or files | user A requests user B's profile/document URL and asserts denial | `profile`, `document`, `download`, `other user` |
| I-WEB-02 | Sensitive data in HTML/JS | Server-rendered pages / SPA bootstrap data | asserts page source/state blobs exclude secrets, tokens, other users' PII | `__INITIAL_STATE__`, `window.`, `token`, `html` |
| I-WEB-03 | Cache-control on sensitive pages | Authenticated pages | asserts `Cache-Control: no-store` (or private) on sensitive responses | `Cache-Control`, `no-store`, `Pragma` |
| I-WEB-04 | Errors don't leak internals | Any web app | triggers errors and asserts no stack traces/SQL/paths/versions in body | `500`, `traceback`, `stack`, `DEBUG` |
| I-API-01 | Over-fetching / excessive fields | APIs returning objects | asserts response schema per role excludes internal/sensitive fields (`password_hash`, `ssn`, internal IDs) | `password`, `hash`, `serializer`, `exclude`, `schema` |
| I-API-02 | Enumeration resistance | Login, reset, signup, resource lookups | asserts identical responses/timing for existing vs non-existing users/resources | `user not found`, `enumerat`, `reset`, `404` |
| I-API-03 | Debug endpoints disabled | Frameworks with debug/admin/actuator/docs routes | asserts debug/actuator/swagger/graphiql are off in prod config | `actuator`, `debug`, `/docs`, `graphiql`, `swagger` |
| I-API-04 | Secrets not in error bodies | Any API | triggers failures and asserts no keys, connection strings, tokens in body | `error`, `exception`, `secret` |
| I-DB-01 | Minimal read permissions | DB in scope | asserts runtime role can't read tables it doesn't need | `SELECT`, `GRANT`, `permission denied` |
| I-DB-02 | Multi-tenant read isolation | Multi-tenant data | tenant A query never returns tenant B rows (repository + RLS level) | `tenant`, `org_id`, `workspace_id` |
| I-DB-03 | Backups/snapshots protected | Backups exist | asserts backups encrypted and access-restricted | `backup`, `snapshot`, `encrypt` |
| I-DB-04 | Search/index exposure | Elasticsearch/OpenSearch/Solr/Mongo/Redis | asserts index/cluster isn't reachable unauthenticated or publicly | `elasticsearch`, `opensearch`, `xpack.security`, `bind`, `0.0.0.0` |
| I-OTH-LOGS | Log/observability leakage | Logging | asserts PII/secrets are redacted in logs on common failures | `redact`, `mask`, `caplog`, `logger` |
| I-OTH-STORAGE | Object storage exposure | S3/GCS/Azure Blob | bucket policy/public-access-block tests, signed URL expiry | `s3`, `bucket`, `presigned`, `public` |
| I-OTH-LLM | LLM data leakage | LLM features | asserts secrets/other users' data aren't placed in context or returned; tool output redaction | `context`, `prompt`, `redact` |

## D — Denial of service

> Upstream has no Web DoS sheet. For web front-ends, apply the API scenarios to the backing endpoints.

| ID | Scenario | Applies when | Covered when a test… | Hints |
|---|---|---|---|---|
| D-API-01 | Per-client quotas | Public or multi-tenant API | exceeds quota and asserts 429 + `Retry-After`, other clients unaffected | `429`, `rate_limit`, `quota`, `Retry-After` |
| D-API-02 | Timeouts and circuit breakers | Outbound calls to dependencies | simulates slow/failing dependency and asserts timeout + fallback/circuit open | `timeout`, `circuit`, `breaker`, `retry` |
| D-API-03 | Pagination and query cost limits | List/search endpoints | requests huge `limit`/page size and asserts it's capped | `limit`, `page_size`, `max`, `per_page` |
| D-API-04 | GraphQL complexity limits | GraphQL | sends deep/wide/aliased queries and asserts rejection | `depth`, `complexity`, `alias`, `graphql` |
| D-DB-01 | Connection limits and pooling | DB connections | exhausts pool and asserts bounded wait/graceful error | `pool_size`, `max_connections`, `pool_timeout` |
| D-DB-02 | Query timeouts | DB queries | asserts statement timeout is configured/enforced | `statement_timeout`, `query_timeout`, `max_execution_time` |
| D-DB-03 | Lock contention | Concurrent writes | asserts lock timeouts / no deadlock hang | `lock_timeout`, `deadlock`, `SELECT ... FOR UPDATE` |
| D-DB-04 | Index/maintenance protections | Large tables, user-driven filters | asserts critical queries use indexes (explain baseline) | `EXPLAIN`, `index` |
| D-OTH-CACHE | Cache abuse | Caches | stampede protection, eviction, key cardinality limits | `cache`, `ttl`, `lock`, `stampede` |
| D-OTH-MQ | Queue backpressure | Queues/streams | poison message handling, consumer lag, backpressure | `poison`, `dlq`, `lag`, `prefetch` |
| D-OTH-K8S | K8s resources | Kubernetes | requests/limits set, HPA, PDB | `resources:`, `limits:`, `HorizontalPodAutoscaler`, `PodDisruptionBudget` |

## E — Elevation of privilege

| ID | Scenario | Applies when | Covered when a test… | Hints |
|---|---|---|---|---|
| E-WEB-01 | Horizontal EoP (IDOR via routes) | User-owned resources in web routes | user A acts on user B's resource via route and asserts 403/404 + no side effects | `owner`, `other_user`, `idor` |
| E-WEB-02 | Vertical EoP via UI-only checks | Roles with UI hiding of actions | low-priv user calls admin action endpoint directly and asserts 403 | `admin`, `is_staff`, `role`, `hidden button` |
| E-WEB-03 | Role changes need step-up | Role/permission management | asserts role change requires re-auth/MFA | `reauth`, `step_up`, `mfa`, `confirm password` |
| E-WEB-04 | Admin panels with layered controls | Admin panel | asserts admin panel requires role **and** extra control (network/MFA) | `/admin`, `mfa`, `ip_allowlist` |
| E-API-01 | Vertical EoP (role boundary) | Roles | each privileged endpoint tested with each lower role and asserts 403 (permission matrix) | `parametrize`, `role`, `403` |
| E-API-02 | Horizontal EoP (ownership) | Per-user/tenant resources | cross-user/tenant read+write+delete each asserted denied | `owner`, `tenant`, `404` |
| E-API-03 | Confused deputy | Service acting on behalf of users (jobs, webhooks, proxies, LLM tools) | asserts downstream call uses the **caller's** authority, not the service's | `on_behalf_of`, `impersonat`, `service account`, `delegat` |
| E-API-04 | Client-controlled roles | Roles/flags in headers, claims, or body | sends `X-Role: admin`, `isAdmin=true`, forged claims and asserts ignored | `X-User`, `X-Role`, `isAdmin`, `claims` |
| E-DB-01 | Runtime role can't grant | DB in scope | asserts `GRANT`/`CREATE ROLE` denied for runtime role | `GRANT`, `CREATE ROLE` |
| E-DB-02 | Separation of duties for migrations | Migrations | migration identity ≠ runtime identity | `migrat`, `owner` |
| E-DB-03 | Dangerous functions restricted | DB with extensions/UDFs | asserts `COPY PROGRAM`, `xp_cmdshell`, `LOAD_FILE`, etc. denied | `COPY`, `xp_cmdshell`, `LOAD_FILE` |
| E-DB-04 | Stored procedure ownership | Stored procedures/`SECURITY DEFINER` | asserts procs don't let callers exceed their privileges | `SECURITY DEFINER`, `procedure` |
| E-OTH-IAM | Cloud IAM escalation | Cloud IAM policies | least privilege, permission boundaries, no wildcard actions | `"Action": "*"`, `iam:PassRole`, `boundary` |
| E-OTH-K8S | K8s RBAC escalation | Kubernetes RBAC | no `*` verbs/resources, no `cluster-admin` bindings | `ClusterRoleBinding`, `cluster-admin`, `verbs: ["*"]` |
| E-OTH-CICD | CI/CD privilege | CI pipelines | PRs from forks can't access secrets / deploy; minimal runner permissions | `pull_request_target`, `permissions:`, `secrets.` |

---

## Custom scenarios from a threat model

Threats from the team's own threat model that don't match a row above become `TM-<NN>`.
Classify each by STRIDE letter and component. Write its hypothesis as Given/When/Then and its required
assertions the same way as above (outcome, no side effects, evidence).
