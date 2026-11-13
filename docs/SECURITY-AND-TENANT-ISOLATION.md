# Security and Tenant Isolation Policy

## Non-negotiable confidentiality requirement

**No person outside a customer organization may access that organization's business information.** This includes OpenRig platform administrators, infrastructure operators, developers, and support personnel.

Customer organizations control access through their own authorized users. Platform-level access is limited to service operation and software delivery and must not provide a path to view customer records.

## Data isolation

- Every organization-owned record must be associated with an organization identifier.
- Every API request must be authorized against the authenticated user's active organization membership.
- Database queries must be tenant-scoped by design; tenant filters must not depend on frontend behavior.
- File storage, attachments, exports, search indexes, caches, background jobs, and analytics must preserve the same tenant boundary.
- Client-supplied identifiers must never bypass tenant authorization.
- Automated tests must prove that one tenant cannot read, update, delete, export, or infer another tenant's data.

## Platform operator restrictions

Platform operators may access operational telemetry needed to keep the service running, such as service health, deployment status, error rates, and resource utilization. Telemetry must not contain customer business content, credentials, or sensitive document data.

Support tooling must not include impersonation or view-as-customer features. Database consoles, object storage, backups, and observability tools must prevent routine human access to plaintext customer data.

## Encryption and key ownership

- Encrypt network traffic using current TLS.
- Encrypt persistent storage and backups.
- Use a separate data-encryption key boundary for each organization.
- Prefer customer-controlled keys or a design where the customer controls key release/decryption authorization.
- Never store plaintext encryption keys in source code, logs, or ordinary database records.
- Document key rotation, recovery, revocation, and organization offboarding.

**Important:** encryption at rest alone does not prevent a privileged server operator from reading plaintext after application decryption. Meeting the confidentiality requirement requires an architecture that prevents platform operators from obtaining decryption capability, such as customer-controlled keys and a carefully designed client-side or customer-controlled decryption boundary. This must be threat-modeled and independently tested before claiming the guarantee.

## Backups and support

Backups must be encrypted with tenant-aware key controls. Restore operations must preserve tenant separation. Support personnel may receive non-sensitive diagnostic metadata, but not customer records, files, or decrypted backups.

## Security acceptance criteria

1. Cross-tenant tests cover every protected API and file operation.
2. Server-side authorization is mandatory on every protected endpoint.
3. No platform-admin role can read customer business data.
4. Secrets and encryption keys are never committed or logged.
5. Logs and telemetry are reviewed for accidental customer-content leakage.
6. Backup and restore tests prove tenant isolation.
7. Threat modeling and security review are completed before production claims.

This policy is a target architecture and acceptance requirement, not a claim that the current scaffold already satisfies it.
