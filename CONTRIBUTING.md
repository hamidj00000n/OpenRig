# Contributing to OpenRig

Thank you for considering a contribution to OpenRig. The project is in an early development stage, so clear, focused contributions and reproducible feedback are especially valuable.

## Before you start

1. Read the [README](README.md), [roadmap](ROADMAP.md), and [implementation status](docs/IMPLEMENTATION-STATUS.md).
2. Search existing issues and pull requests to avoid duplicate work.
3. For a substantial feature or architectural change, open an issue first to discuss scope and compatibility.
4. Never use or submit real customer, employee, supplier, rig, financial, or operational data.

## Development setup

Use the setup instructions in the README. The backend requires Python 3.11+ and the frontend requires Node.js 22+.

## Branches and commits

- Create a focused branch from `main`.
- Keep pull requests small enough to review.
- Use descriptive commit messages, for example:
  - `feat: add equipment register API`
  - `fix: enforce organization scope on inventory queries`
  - `docs: clarify local development setup`
- Avoid unrelated formatting or generated-file changes.

## Before opening a pull request

Run the relevant checks:

```bash
# Backend
cd backend
pytest -v

# Frontend
cd ../frontend
npm ci
npm run build
```

For changes involving authorization, organization membership, or customer data, add tests for both authorized access and denied cross-organization access.

## Pull request checklist

- [ ] The change has a clear purpose and is linked to an issue when appropriate.
- [ ] Tests cover the changed behavior, including authorization boundaries.
- [ ] Backend tests pass locally.
- [ ] Frontend production build passes when frontend files change.
- [ ] API and user-facing documentation are updated where needed.
- [ ] No secrets, credentials, personal data, or customer data are included.
- [ ] New capabilities are not described as production-ready without evidence.

## Security-sensitive changes

Authentication, authorization, tenant isolation, cryptography, file access, exports, and audit logging require particular care. Explain the threat addressed, the trust boundary, and the tests added. Do not weaken tenant isolation to simplify a feature.

## Scope and expectations

The roadmap describes intended work, not a promise that every planned feature is already available. Discuss significant changes before implementing them so contributions align with the architecture and confidentiality requirements.
