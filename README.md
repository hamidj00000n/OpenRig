# OpenRig

**Open-source drilling rig operations management platform**

OpenRig is an early-stage project to build a cross-platform operations management system for land and offshore drilling rigs. Its intended users include drilling contractors and rig operations, maintenance, warehouse, and procurement teams.

> **Project maturity:** OpenRig is under active early-stage development. The current repository contains an initial identity and organization-management foundation. The broader operational modules described below are planned, not yet delivered. OpenRig is not production-ready.

[![CI](https://github.com/hamidj00000n/OpenRig/actions/workflows/ci.yml/badge.svg)](https://github.com/hamidj00000n/OpenRig/actions/workflows/ci.yml)

## Why OpenRig?

Drilling operations depend on connected workflows across equipment, maintenance, inventory, procurement, suppliers, and operational reporting. OpenRig aims to provide a coherent platform for these workflows, with a consistent data model and organization-level access controls.

## Current implementation

The current foundation includes:

- User registration and password hashing with Argon2
- Short-lived signed bearer access tokens
- Authenticated user profile endpoint
- Organization creation and membership listing
- Organization member listing and role administration
- Automated backend tests for authentication, organization visibility, and member-role authorization
- Initial React/TypeScript application shell with English and Persian language support

See [Implementation Status](docs/IMPLEMENTATION-STATUS.md) for the implemented scope and known gaps.

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

## Platform and technology

| Layer | Technology / direction |
|---|---|
| Web client | React, TypeScript, Vite |
| API | Python, FastAPI |
| ORM and data access | SQLAlchemy |
| Local development database | SQLite |
| Production database target | PostgreSQL |
| Windows desktop target | Tauri 2 (planned) |
| Android target | APK/AAB packaging (planned) |
| iPhone/iPad target | Responsive web app / PWA (planned) |

English is the default interface language. Persian is an optional RTL locale.

## Getting started

### Prerequisites

- Python 3.11 or newer
- Node.js 22 or newer (LTS recommended)
- npm

### Backend

From the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
Copy-Item .env.example .env
pytest -v
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000` and its interactive documentation at `http://127.0.0.1:8000/docs`.

For macOS/Linux, activate the environment with `source .venv/bin/activate`. Review [backend/README.md](backend/README.md) and [backend/.env.example](backend/.env.example) before running the API.

### Frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run build
npm run dev
```

Vite prints the local development URL when the server starts.

## Quality checks

Run backend tests:

```bash
cd backend
pytest -v
```

Build the frontend:

```bash
cd frontend
npm ci
npm run build
```

The GitHub Actions workflow runs the backend test suite and frontend production build on pushes and pull requests.

## Security and data confidentiality

Tenant isolation and customer confidentiality are core design requirements. The project security policy documents the intended controls and explicitly distinguishes requirements from implemented protections.

- Read [Security Policy](SECURITY.md) before reporting a vulnerability.
- Read [Tenant Isolation and Security Requirements](docs/SECURITY-AND-TENANT-ISOLATION.md).
- Do not use real customer, employee, supplier, operational, or other confidential data in development or issue reports.
- Do not commit secrets, credentials, private keys, production database exports, or customer documents.

The current application is an early development scaffold. It has not undergone an independent security audit and must not be deployed with sensitive production data.

## Contributing

Contributions, bug reports, and technical discussions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md), follow the project Code of Conduct, and open an issue before starting large or breaking changes.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned milestones and [docs/IMPLEMENTATION-STATUS.md](docs/IMPLEMENTATION-STATUS.md) for current implementation evidence.

## License

A license has not yet been selected for this repository. Until a license is added, do not assume that the code is available for reuse, redistribution, or modification. The maintainers must choose and approve the project license before OpenRig can be presented as an openly licensed software project.
