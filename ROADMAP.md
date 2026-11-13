# OpenRig Roadmap

This roadmap describes planned work. A checklist item is complete only when implementation and validation evidence are available.

## 0.1.x — Project foundation
- [x] Initial repository and project definition
- [x] Document cross-platform delivery strategy
- [x] Document identity, organization, and tenant-isolation requirements
- [x] Define English as the default application language
- [x] Publish contribution, security, and community conduct guidance
- [x] Add automated GitHub Actions checks for backend tests and frontend build
- [x] Select and publish Apache License 2.0

## 0.2.x — Cross-platform foundation
- [ ] Responsive web application
- [ ] PWA service worker and validated iPhone/iPad home-screen installation
- [ ] Tauri 2 Windows packaging pipeline
- [ ] Android APK/AAB packaging pipeline
- [ ] Versioned release notes and artifact checksums

## 0.3.x — Identity and organizations
- [x] User registration and password hashing
- [x] Short-lived bearer access tokens
- [x] Organization creation and membership listing
- [x] Organization member listing and initial role administration API
- [ ] Email verification and password reset
- [ ] Invitations and membership lifecycle management
- [ ] Granular role- and scope-based permissions
- [ ] Database migrations
- [ ] Rate limiting and MFA
- [ ] Comprehensive tenant-isolation tests and audit trail

## 0.4.x — Organization structure and rig register
- [ ] Departments, sites, projects, and rig hierarchy
- [ ] Land and offshore rig register
- [ ] Equipment register and attachments

## 0.5.x — Warehouse and procurement
- [ ] Item master and categories
- [ ] Warehouse locations and stock transactions
- [ ] Suppliers, RFQs, quotations, and purchase orders
- [ ] Approval workflows

## 0.6.x — Maintenance
- [ ] Preventive maintenance plans
- [ ] Corrective maintenance and work orders
- [ ] Equipment history and downtime records

## 0.7.x — Reporting and operations
- [ ] Operational dashboards
- [ ] Inventory, procurement, and maintenance reports
- [ ] Export and scheduled reporting

## 1.0.0 — Stable release
- [ ] Customer-controlled encryption/decryption architecture independently reviewed
- [ ] Independent security review and production deployment guide
- [ ] Tested backup and restore
- [ ] Validated Windows installer
- [ ] Validated Android package
- [ ] Validated production PWA
- [ ] User and administrator documentation
- [ ] Release acceptance checklist completed
