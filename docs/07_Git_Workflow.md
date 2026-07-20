# Git Workflow

Version: 1.0

Status: Living Document

---

# Purpose

This document defines the official Git strategy used by the Odoo AI Audit Platform.

Every contributor must follow these rules.

---

# Repository

Repository Name

```text id="jvxmds"
odoo-ai-audit-platform
```

Primary Repository

```text id="esz2bo"
https://github.com/aladdinelashri/odoo-ai-audit-platform
```

---

# Main Branches

## main

Purpose

Stable production-ready code.

Rules

Always deployable.

Protected branch.

Merged only after verification.

---

## develop

Purpose

Integration branch.

Future development may merge features here before main if required.

---

## Feature Branches

Every implementation begins from **main**.

Examples

```text id="5x04ww"
feature-live-xmlrpc-auth
feature-xmlrpc-login
feature-xmlrpc-object-service
feature-company-reader
feature-model-reader
feature-pos-order-reader
feature-account-reader
feature-journal-reader
```

---

# Branch Naming Convention

Pattern

```text id="agjlwm"
feature-short-description
```

Rules

* Lowercase.
* Hyphen separated.
* Short and descriptive.
* One feature only.

---

# Branch Lifecycle

```text id="gwlxt5"
main
 │
 ├── feature-xxxxx
 │        │
 │        ▼
 │   Development
 │        │
 │        ▼
 │     Testing
 │        │
 │        ▼
 │      Commit
 │        │
 │        ▼
 │       Push
 │        │
 │        ▼
 │      Merge
 │        │
 │        ▼
 └────── main
```

After merge

Delete the feature branch.

---

# Creating a Feature

```bash id="9hx2qb"
git checkout main
git pull origin main
git checkout -b feature-example
```

---

# Daily Development

Check status

```bash id="5gc9jn"
git status
```

Review changes

```bash id="c8sjaj"
git diff
```

Stage changes

```bash id="tqsrfi"
git add .
```

Commit

```bash id="b3txs5"
git commit -m "Add example feature"
```

Push

```bash id="kkn3k9"
git push -u origin feature-example
```

---

# Merge Procedure

Switch

```bash id="25xkgl"
git checkout main
```

Update

```bash id="jzs0dt"
git pull origin main
```

Merge

```bash id="ifjlwm"
git merge feature-example
```

Push

```bash id="zmttnh"
git push origin main
```

---

# Delete Feature Branch

Local

```bash id="exr0wf"
git branch -d feature-example
```

Remote

```bash id="th4s2m"
git push origin --delete feature-example
```

---

# Commit Messages

Format

```text id="5s6yhg"
Verb + Feature
```

Examples

```text id="lskrr0"
Add XML-RPC authentication foundation

Add XML-RPC login

Add XML-RPC object service foundation

Add company reader

Add model reader

Update project handbook

Remove temporary XML-RPC login test
```

Avoid

```text id="q7m5pf"
fix

update

changes

final

work

done
```

---

# Pull Requests

Every feature branch should create one Pull Request.

One Pull Request

↓

One Feature

↓

One Review

---

# Conflict Resolution

Always

Pull latest main.

Resolve locally.

Run tests again.

Commit merge resolution.

Push.

Never force-push to main.

---

# Tags

Future releases may use

```text id="f6xcm7"
v1.0.0
v1.1.0
v2.0.0
```

Semantic Versioning

Major

Minor

Patch

---

# Release Policy

Only merge tested features.

Every release must include

Updated documentation.

Updated changelog.

Passing tests.

Verified production compatibility.

---

# Repository Rules

Never commit

Passwords

Secrets

API keys

Environment files

Temporary test scripts

Local IDE settings

Generated cache

---

# Recommended Daily Routine

```text id="qd0qoc"
Pull latest main

↓

Create feature branch

↓

Implement

↓

Test

↓

Commit

↓

Push

↓

Review

↓

Merge

↓

Delete branch

↓

Update documentation
```

---

# Long-Term Goal

Maintain a clean Git history where every commit represents one verified improvement and every branch documents one completed feature.

The repository should remain understandable and maintainable throughout the lifetime of the project.

