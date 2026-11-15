# Platform and Distribution Strategy

## Product decision

OpenRig uses one shared backend/API and a common responsive React application.

- Windows: Tauri 2 desktop shell; build NSIS EXE and MSI installers.
- Android: Capacitor 7 shell; generate the native Android project and distribute APK/AAB.
- iPhone and iPad: installable responsive PWA in Safari for the initial release. A native iOS shell can be added later if App Store distribution is required.
- Web: the same responsive client runs in modern desktop and mobile browsers.

## Shared application and API

Business rules and authorization are enforced by the backend. All clients use the same versioned API and tenant authorization policy. The clients do not own separate operational databases.

Configure the API URL at deployment through `frontend/public/openrig-config.js`:
```js
window.OPENRIG_CONFIG = { apiUrl: "https://api.your-domain.example" };
```
The same HTTPS API endpoint is used by Windows, Android, iOS/PWA and browser clients. Do not point a production client at localhost. The current application falls back to `http://localhost:8000` for local development only.

## Connectivity and offline behavior

- Online mode is the initial supported operating mode. Authentication and operational data require a reachable API.
- The PWA service worker caches only the application shell and static same-origin assets. API requests, authenticated responses, customer data and documents are never cached by this service worker.
- The shell may open while offline, but users cannot sign in or read/write server data without a connection.
- Offline transactions, local customer-data storage, conflict resolution and synchronization are not implemented. They require a separate security and data-consistency design before being enabled.

## Windows build

Prerequisites: Node.js LTS, Rust stable, and Windows build tools required by Tauri 2.
```powershell
cd frontend
npm install
npm run tauri:build
```
Installers are produced under `frontend/src-tauri/target/release/bundle/`. Validate installation, upgrade, uninstall, API connectivity and signing before distribution.

## Android build

Prerequisites: Node.js LTS, Android Studio, Android SDK and a supported JDK.
```powershell
cd frontend
npm install
npx cap add android
npm run mobile:sync
npm run mobile:android
```
The generated Android project is under `frontend/android`. Build an APK/AAB from Android Studio or Gradle after configuring the production API URL and signing key. Never commit signing keys.

## iPhone and iPad

Deploy the web client over HTTPS. Open the URL in Safari and choose Share, then Add to Home Screen. The initial iOS distribution is a PWA; no native iOS binary is included.

## Release assets

Each release should include version, notes, Windows EXE/MSI, architecture, SHA-256 checksum, Android APK/AAB where applicable, known issues, upgrade instructions and validation status. Early builds must be alpha/beta pre-releases. Do not label a build stable until automated tests, security checks, installation tests and upgrade tests pass.
