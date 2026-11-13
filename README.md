# OpenRig

Open-source, cross-platform drilling rig operations management platform.

## Platform delivery

| Platform | Delivery |
|---|---|
| Android | APK for direct installation; AAB for store distribution when applicable |
| Windows | EXE or MSI installer |
| iPhone and iPad | Responsive Web App / PWA, installable from Safari using Add to Home Screen |
| Desktop browsers | Responsive web application |

The initial iPhone/iPad strategy is PWA; a separate native iOS application is not in scope.

## Language

**English is the default application language.** Persian is optional. The interface supports English LTR and Persian RTL. If no saved preference exists, English is used.

## Core capabilities

- Secure authentication and session management
- Multi-organization tenancy with strict data isolation
- Organization structure, departments, operating sites, rigs, and projects
- User invitations, roles, and permission scopes
- Equipment, spare parts, warehouse, procurement, suppliers, and maintenance
- Reports, dashboards, attachments, and audit history

## Architecture direction

- Web: React, TypeScript, and Vite
- API: Python and FastAPI
- Data: PostgreSQL in production; SQLite for local development
- Windows desktop: Tauri 2
- Android: installable application package based on the shared application
- iPhone/iPad: PWA based on the shared responsive web client

See the documents in the docs folder for platform, identity, security, and localization requirements.

## Project status

OpenRig is in early-stage development. Roadmap items are planned work and must not be interpreted as completed or production-ready features.

## Releases

Installers and release notes will be published on the GitHub Releases page. Android APK/AAB and Windows EXE/MSI assets will be attached only after successful builds and validation. PWA updates are deployed through the web application.
