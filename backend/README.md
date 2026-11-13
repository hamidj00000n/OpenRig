# OpenRig API

Initial API foundation for user registration, authentication, and organization creation.

## Local setup

Python 3.11 or newer is required.

```bash
cd backend
python -m venv .venv
# Activate the virtual environment, then:
pip install -e ".[dev]"
cp .env.example .env
uvicorn app.main:app --reload
```

Set a unique random OPENRIG_SECRET_KEY before running outside local development. Do not use the development fallback in production.

API documentation is available at http://127.0.0.1:8000/docs.

## Initial endpoints

- POST /api/v1/auth/register
- POST /api/v1/auth/login
- GET /api/v1/auth/me
- GET /api/v1/organizations
- POST /api/v1/organizations
- GET /health

## Current limitations

- Email verification and password-reset delivery are not implemented.
- Organization invitation and role-management workflows are not implemented.
- Database bootstrap uses create_all for local development; production requires Alembic migrations.
- Production-grade tenant isolation, rate limiting, security headers, key management, and deployment hardening require further implementation and independent review.
- This foundation does not yet implement the customer-controlled encryption boundary required by the security policy.
