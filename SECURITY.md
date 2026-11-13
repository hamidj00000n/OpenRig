# Security Policy

## Project status

OpenRig is an early-stage project and has not undergone an independent security audit. Do not deploy it with sensitive production data or treat the current implementation as a certified or production-ready security solution.

## Reporting a vulnerability

Please do not disclose suspected vulnerabilities in public issues, discussions, or pull requests.

Use GitHub's **Private vulnerability reporting** feature for this repository, if it is enabled. If private reporting is unavailable, contact the repository maintainer privately through the contact method listed on the maintainer's GitHub profile and request a secure channel. Include:

- A concise description of the issue and its potential impact
- Affected version, commit, component, and configuration
- Reproduction steps or a proof of concept that does not expose real data
- Any suggested mitigation

Do not include passwords, access tokens, private keys, production database dumps, customer documents, or personal data in the report.

Please allow the maintainer reasonable time to investigate and coordinate a fix before public disclosure. This project does not currently publish a guaranteed response or remediation SLA.

## Security priorities

Reports involving the following areas are particularly important:

- Authentication, session handling, and password storage
- Organization membership, role authorization, and cross-tenant access
- API authorization and object-level access control
- File uploads, downloads, exports, and attachment isolation
- Secret management, encryption, and key handling
- Dependency vulnerabilities and unsafe deployment defaults

## Confidentiality requirement

The project aims to prevent platform operators and other parties outside a customer organization from accessing customer business information. This is a target architecture requirement, not a claim that the current code already provides that guarantee. See [Tenant Isolation and Security Requirements](docs/SECURITY-AND-TENANT-ISOLATION.md).
