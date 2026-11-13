# Platform and Distribution Strategy

## Product decision

OpenRig uses one shared backend/API and a common responsive application experience.

- Android: distribute an APK for direct installation. Produce an AAB when preparing a Google Play release.
- Windows: distribute a Tauri 2 desktop installer in EXE or MSI format.
- iPhone and iPad: use the responsive Web App as a Progressive Web App (PWA). Users open it in Safari and select Share, then Add to Home Screen. A separate native iOS/iPadOS application is not in the initial scope.
- Web: support modern desktop and mobile browsers.

## Shared application and API

Business rules and authorization must be enforced by the backend. Platform-specific clients must not implement separate business rules. All clients use the same versioned API and tenant authorization policy.

## Release assets

Each applicable GitHub Release should include a semantic version, release date, English release notes, changelog, Windows EXE/MSI installer, architecture, SHA-256 checksum, Android APK and (where applicable) AAB, known issues, upgrade instructions, and validation status. Early builds must be identified as alpha/beta pre-releases. Do not label a build stable until automated tests, security checks, installation tests, and upgrade tests pass.

## PWA requirements

- Responsive phone and tablet layouts
- Web app manifest with name, icons, theme color, and standalone display mode
- HTTPS deployment and service worker with controlled caching/update handling
- Clear authentication expiry and re-authentication behavior
- Touch-friendly navigation and forms
- Explicitly documented offline behavior; do not claim offline transactions unless safe queueing and synchronization are implemented

## Android requirements

- Reuse the shared application and API where practical
- Secure session/token handling and minimal device permissions
- Test installation, upgrades, authentication, uploads/downloads, and network interruption
- Produce APK for GitHub Releases and AAB for store distribution when needed

## Windows requirements

- Tauri 2 desktop packaging
- EXE/MSI installer with version and architecture metadata
- SHA-256 checksum for each published installer
- Code signing when a valid certificate is available
- Test clean installation, upgrade, uninstall, file handling, and update behavior

## Versioning

Use Semantic Versioning (MAJOR.MINOR.PATCH). During early development, use 0.x versions and mark releases as pre-release. Publish a release only when its artifacts and validation evidence are ready.
