# Localization and Language Policy

## Default language

**English is the default language of OpenRig.** A new user, a new browser profile, or a user without a saved language preference must see the application in English.

## Supported languages

- English (en) — default, left-to-right (LTR)
- Persian (fa) — optional, right-to-left (RTL)

## User preference

Users may switch language from the application interface. For authenticated users, the preference should be saved to the user's profile and synchronized across devices. For unauthenticated sessions, it may be stored locally in the browser. If no valid preference exists, use English.

## Implementation requirements

- Use translation keys; do not hard-code user-facing strings throughout components.
- Keep language selection independent from organization data and permissions.
- Set document language and text direction correctly using lang and dir attributes.
- Apply RTL-aware layout behavior rather than merely right-aligning text.
- Format dates, numbers, and currencies according to selected locale and organization settings.
- Ensure both languages have equivalent functional coverage.
- Avoid mixing English and Persian labels on the same screen unless a technical identifier must remain unchanged.

## Acceptance criteria

1. Fresh installation opens in English.
2. Clearing local preferences returns the application to English.
3. Persian can be selected and displays a complete RTL interface.
4. A saved user preference persists after sign-in on another device.
5. Language changes do not change data, permissions, or organization context.
