# OpenRig Web Client

React + TypeScript web client. English is the default language; Persian is selectable and switches the interface to RTL.

## Run locally

```bash
cd frontend
npm install
npm run dev
```

By default the client expects the API at http://localhost:8000. Set VITE_API_URL to override it.

## Current scope

This is the first functional UI increment for account registration, sign-in, and organization creation/listing. Other operational navigation entries are placeholders. The PWA manifest is included as a foundation; service-worker registration, offline strategy, app icons, and production hosting still need to be completed.
