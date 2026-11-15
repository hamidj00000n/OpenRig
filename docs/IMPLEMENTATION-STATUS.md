# Implementation Status

## Version 0.4.0 — Cross-platform client foundations

Implemented in this increment:

- Windows desktop wrapper configuration using Tauri 2, with NSIS/MSI bundle targets.
- Android wrapper configuration using Capacitor 7; Android native project generation is a documented local build step.
- Responsive installable PWA metadata for iPhone/iPad and mobile browsers.
- Service worker caches only the static application shell; API calls and customer data are excluded.
- Runtime API endpoint configuration through `frontend/public/openrig-config.js`.
- Shared API architecture across desktop, mobile and web clients.

Previously implemented:

- User registration and Argon2 password hashing
- Short-lived signed bearer access tokens
- Organization creation, membership and invitations
- Organization permission configuration API and initial audit events
- English and Persian RTL application shell

Not yet implemented:

- Published Windows installer and signed Android APK/AAB artifacts
- Native iOS application
- Offline operational records, secure local database and conflict-safe synchronization
- Secure platform-native token vault integration
- Customer-controlled encryption/decryption architecture
- Production database migrations, rate limiting, MFA and deployment hardening
- Complete operational modules and comprehensive audit coverage

This is a development-stage platform scaffold, not a production-ready application. Do not deploy with sensitive production data before security review and required controls are implemented.
