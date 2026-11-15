# OpenRig

**Open-source drilling rig operations management platform**

OpenRig is an early-stage cross-platform operations management system for land and offshore drilling rigs. Its intended users include drilling contractors and rig operations, maintenance, warehouse, and procurement teams.

> **Project maturity:** OpenRig is under active early-stage development. The current repository contains an identity and organization-management foundation plus cross-platform client scaffolding. The broader operational modules are still under development. OpenRig is not production-ready.

[![CI](https://github.com/hamidj00000n/OpenRig/actions/workflows/ci.yml/badge.svg)](https://github.com/hamidj00000n/OpenRig/actions/workflows/ci.yml)

## Platform architecture

OpenRig uses one central API and database shared by all clients:

- Windows desktop: Tauri 2 (NSIS EXE/MSI)
- Android: Capacitor 7 (APK/AAB; native project generated locally)
- iPhone/iPad: installable PWA in Safari for the initial release
- Web: responsive React/TypeScript client

The Windows and mobile applications are installed locally, but operational data is held centrally and accessed through the same HTTPS API. Offline operational data entry and synchronization are not implemented. The PWA caches only its static application shell, never API responses or customer records.

See [Platform Strategy](docs/PLATFORM-STRATEGY.md) for build instructions and API configuration.

## Current implementation

- User registration and password hashing with Argon2
- Short-lived signed bearer access tokens
- Organization creation, membership and invitations
- Organization permission configuration API and initial audit events
- React/TypeScript application shell with English and Persian language support
- Tauri desktop and Capacitor Android project configuration
- Installable PWA metadata and conservative static-shell service worker

See [Implementation Status](docs/IMPLEMENTATION-STATUS.md) for implemented scope and known gaps.

## Planned product areas

- Rig, site, department, and project registers
- Land and offshore rig operations
- Equipment register and technical records
- Spare parts and warehouse inventory
- Procurement, RFQs, quotations, and purchase orders
- Preventive and corrective maintenance
- Supplier management
- Dashboards, reports, exports, and audit history

These are roadmap goals and must not be interpreted as existing features.

## Technology

| Layer | Technology |
|---|---|
| Desktop shell | Tauri 2 |
| Android shell | Capacitor 7 |
| iOS initial distribution | PWA |
| Frontend | React, TypeScript, Vite |
| API | Python, FastAPI |
| Local development DB | SQLite |
| Production DB target | PostgreSQL |

English is the default interface language. Persian is an optional RTL locale.

## Development

Backend:
```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
pytest -v
uvicorn app.main:app --reload
```

Frontend:
```powershell
cd frontend
npm install
npm run build
npm run dev
```

Windows desktop build prerequisites: Node.js, Rust stable and Tauri Windows build tools. Run `npm run tauri:build`.

Android build prerequisites: Node.js, Android Studio, Android SDK and JDK. Run `npx cap add android`, then `npm run mobile:sync` and `npm run mobile:android`.

## Security and data confidentiality

Tenant isolation and customer confidentiality are core requirements. The current application is an early development foundation, has not undergone an independent security audit, and must not be deployed with sensitive production data. Server-side encryption at rest alone does not satisfy the customer-controlled confidentiality requirement. See [SECURITY.md](SECURITY.md) and [Tenant Isolation and Security Requirements](docs/SECURITY-AND-TENANT-ISOLATION.md).

## License

Apache License 2.0. See [LICENSE](LICENSE).
