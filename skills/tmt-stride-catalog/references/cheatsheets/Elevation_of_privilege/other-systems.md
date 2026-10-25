# Elevation of Privilege — Other systems (suggestions)

- Cloud IAM: privilege escalation path tests (least privilege, permission boundaries, break-glass accounts).
- Kubernetes: RBAC escalation checks (no `*` verbs/resources, no `cluster-admin` leakage).
- CI/CD: protect secrets and runner permissions; verify PRs can’t gain deploy rights.

