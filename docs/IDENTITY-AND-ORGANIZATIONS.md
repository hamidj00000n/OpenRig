# Identity, Access Control, and Organizations

## Objective

OpenRig supports multiple independent organizations in one deployment. Each organization manages its own users, departments, operating sites, rigs, projects, equipment, inventory, procurement, maintenance records, attachments, and reports.

## Authentication requirements

- Sign-in and sign-out
- Secure password hashing
- Password reset through a verified recovery channel
- Forced password change for administrator-provisioned first-login credentials
- Session expiry, refresh, and revocation
- Optional multi-factor authentication
- Login throttling and protection against credential stuffing
- No default production passwords or hard-coded secrets

## Organization membership

A user may belong to one or more organizations only when explicitly invited and approved. Each request must be authorized against the authenticated user's active organization membership.

Suggested entities: Organization, OrganizationMembership, User, Role, Permission, RolePermission, Department, OperatingSite, Rig, Project, and AuditEvent.

## Organization hierarchy

Organization → Department / Business Unit → Operating Site → Rig → Equipment / Operations.

Projects may be associated with an organization, site, and one or more rigs. The hierarchy should be configurable by each organization without changing application code.

## Roles

- Organization Owner: manages the organization, settings, memberships, and organization-level roles.
- Organization Administrator: manages users, departments, sites, rigs, and master data within the organization.
- Rig Manager: manages assigned rigs and operational records.
- Department Manager: manages records within assigned departments and scope.
- Procurement: manages suppliers, RFQs, quotations, and purchase orders within granted scope.
- Warehouse: manages stock receipts, issues, transfers, and counts within granted scope.
- Maintenance: manages equipment and maintenance work orders within granted scope.
- Viewer / Auditor: read-only access to permitted records and reports.

Permissions must be enforced server-side and scoped to the organization and, where appropriate, department, site, rig, or project.

## Administrative separation

Platform operators may manage software deployment, service health, version rollout, and technical configuration. They must not receive an application role that permits reading customer business records. Technical maintenance must not provide a path to view customer records.

## Auditability

Record sign-in outcomes, invitations, membership and role changes, organization settings, approvals, exports, and changes to critical records. Audit records include actor, organization, action, target, and timestamp. Never log passwords, access tokens, encryption keys, or sensitive business payloads.

This document defines target requirements; it does not claim that all features are already implemented.
