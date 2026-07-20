# Development Workflow

Version: 1.0

Status: Living Document

---

# Purpose

This document defines the official development workflow for the Odoo AI Audit Platform.

Every contributor must follow this workflow.

No implementation should bypass these rules.

---

# Development Philosophy

The platform is developed using small, isolated, verifiable features.

Every feature is implemented independently.

Every feature must be:

* Designed
* Implemented
* Tested
* Reviewed
* Merged
* Documented

before moving to the next feature.

---

# Feature Development Cycle

```text id="1u4l3x"
Planning
    │
    ▼
Create Feature Branch
    │
    ▼
Implementation
    │
    ▼
Unit Testing
    │
    ▼
Live Testing (when applicable)
    │
    ▼
Commit
    │
    ▼
Push
    │
    ▼
Review
    │
    ▼
Merge
    │
    ▼
Delete Feature Branch
    │
    ▼
Update Documentation
```

---

# Branch Strategy

Every new feature begins from:

```text id="0mq6y9"
main
```

Example:

```bash id="j5r8f4"
git checkout main
git pull origin main
git checkout -b feature-example
```

---

# One Feature Per Branch

Each branch contains exactly one logical feature.

Correct examples:

```text id="8azl0q"
feature-xmlrpc-login
feature-company-reader
feature-model-reader
feature-pos-order-reader
feature-account-move-reader
```

Incorrect examples:

```text id="n9xk7d"
feature-everything
feature-fixes
feature-final
```

---

# Implementation Rules

Each feature should:

Modify only the required files.

Avoid unrelated refactoring.

Remain backward compatible whenever possible.

Keep business logic separated from infrastructure.

---

# Testing

Every feature must be tested.

Testing levels include:

Unit tests

Integration tests

Live Odoo tests

Regression tests

Production verification (read-only)

---

# Commit Policy

One feature = one logical commit.

Commit messages should be concise and descriptive.

Examples:

```text id="j1g8hv"
Add XML-RPC authentication foundation

Add XML-RPC object service

Add company reader

Add model reader
```

---

# Push Policy

After a successful commit:

```bash id="1ijb5h"
git push -u origin feature-name
```

---

# Review

Before merging, verify:

* Feature works.
* Tests pass.
* Documentation updated.
* No temporary files remain.
* No secrets committed.

---

# Merge Process

Merge only after verification.

Example:

```bash id="k3d8xn"
git checkout main
git merge feature-example
git push origin main
```

---

# Branch Cleanup

After merging:

Delete the local branch:

```bash id="f2w7ra"
git branch -d feature-example
```

Delete the remote branch:

```bash id="v0y8hc"
git push origin --delete feature-example
```

---

# Documentation Rule

Every completed feature requires updates to:

* CHANGELOG.md
* PROJECT_STATUS.md
* PROJECT_HANDBOOK.md (or relevant handbook section)

Documentation is part of the feature definition.

A feature is not complete until its documentation is updated.

---

# Coding Standards

* Follow PEP 8.
* Use descriptive names.
* Prefer composition over duplication.
* Write reusable components.
* Add docstrings to public classes and methods.
* Keep functions focused on a single responsibility.

---

# Error Handling

Every external interaction (Odoo, database, filesystem, network) should:

* Detect failures.
* Raise meaningful exceptions.
* Avoid silent failures.
* Preserve useful diagnostic information.

---

# Security Rules

Never commit:

* Passwords
* API keys
* Tokens
* Secrets
* Production credentials

Store configuration only through environment variables.

Use read-only accounts whenever possible.

---

# Live Environment Rules

Production is used only for:

* Read-only authentication.
* Metadata retrieval.
* Data verification.

Never perform write operations against the production environment.

---

# Definition of Done

A feature is considered complete only when all of the following are true:

* Code implemented.
* Tests pass.
* Live verification completed (if applicable).
* Commit created.
* Branch pushed.
* Branch merged.
* Branch deleted.
* Documentation updated.

Only then may development continue to the next feature.

---

# Guiding Principle

The project advances through many small, verified improvements rather than large, risky changes.

This workflow maximizes quality, traceability, maintainability, and long-term stability.

