# Implementation Status

## Version 0.3.0 — Authentication and organization foundation

Implemented in this increment:

- User registration with email uniqueness validation
- Password hashing using the recommended Argon2 configuration from pwdlib
- Short-lived signed bearer access tokens
- Authenticated current-user endpoint
- Organization creation by an authenticated user
- Automatic owner membership for the creator
- Organization listing restricted to active memberships
- Initial automated tests for authentication requirements and organization visibility

Not yet implemented:

- Email verification and password reset
- Invitations, membership administration, and role/permission management
- Department, site, rig, and project hierarchy
- Database migrations
- Rate limiting, MFA, and production deployment hardening
- Customer-controlled encryption/decryption architecture

The implementation is an early development foundation, not a production-ready identity service. Review backend/README.md before running it.
