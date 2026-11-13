# OpenRig — Open-source maintainer workflows

## Purpose

This document describes how the maintainers intend to use coding assistants, including Codex, to reduce routine maintenance work while keeping human maintainers responsible for decisions and releases.

## Intended workflows

1. **Pull request assistance:** summarize diffs, identify likely regressions, check API compatibility, and suggest focused tests. A human maintainer reviews and approves every change.
2. **Issue triage:** classify incoming issues by module, severity, reproducibility, and missing information. Do not automatically close or make commitments on behalf of maintainers.
3. **Test development:** propose unit, integration, authorization, and cross-tenant isolation tests for new behavior.
4. **Security review support:** inspect code for common vulnerabilities, unsafe defaults, authorization gaps, secret leakage, and dependency risks. Findings require human validation; automated review is not a security audit.
5. **Release preparation:** draft changelogs from merged pull requests, check version consistency, and prepare release notes for maintainer approval.
6. **Documentation maintenance:** keep setup guides, API descriptions, implementation status, and roadmap aligned with verified code.

## Guardrails

- No assistant or workflow may approve and merge its own changes.
- Human review is required for all changes affecting authentication, authorization, tenant boundaries, cryptography, data retention, or release publication.
- Never send production credentials, customer records, personal data, private documents, or production database contents to coding assistants or CI.
- Use synthetic fixtures and isolated test databases.
- CI permissions should remain least-privilege and read-only unless a specific workflow demonstrably requires more.
- Do not claim that a security scan or AI review proves the application secure.
- Do not use Codex API credits until the project has been approved for the relevant program benefit and the applicable terms have been reviewed.

## Current state

These are proposed maintainer workflows. OpenRig currently has GitHub Actions checks for backend tests and frontend builds. It does not yet have an automated Codex-powered PR reviewer, issue triage bot, or release automation. Those integrations will be added only after their permissions, data handling, costs, and human approval steps are documented.
