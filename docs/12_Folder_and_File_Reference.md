# Folder and File Reference

Version: 1.0

Status: Living Document

---

# Purpose

This document is the master reference for the repository structure.

Its objectives are to:

* Explain every folder.
* Explain every important file.
* Define the responsibility of each component.
* Help new developers understand the project quickly.
* Prevent duplicate implementations.

Every new file added to the project should also be documented here.

---

# Repository Overview

```text id="5m34r2"
odoo-ai-audit-platform/
│
├── .github/
├── assets/
├── builder/
├── data/
├── database/
├── docs/
├── mcp/
├── prompts/
├── reports/
├── scripts/
├── sql/
├── tests/
│
├── README.md
├── CHANGELOG.md
├── PROJECT_STATUS.md
├── ROADMAP.md
└── .gitignore
```

---

# Root Files

## README.md

Purpose

Project entry point.

Audience

Everyone.

Contains

* Introduction
* Installation
* Quick Start
* Documentation links

---

## ROADMAP.md

Purpose

Overall implementation roadmap.

Audience

Project Manager

Lead Developer

---

## PROJECT_STATUS.md

Purpose

Current implementation status.

Updated after every completed feature.

---

## CHANGELOG.md

Purpose

Historical list of completed features.

Updated after every merge into main.

---

## .gitignore

Purpose

Defines files that must never be committed.

Examples

* Virtual environments
* Cache
* Temporary files
* Environment files

---

# assets/

Purpose

Static project assets.

Examples

* Logos
* Diagrams
* Images
* Icons
* Screenshots

Future

Architecture diagrams.

---

# builder/

Purpose

Developer tooling.

Responsibilities

* Metadata discovery
* Model inspection
* Schema generation

Examples

builder.py

Future

Automatic code generation.

---

# data/

Purpose

Reference data.

Examples

Business dictionaries

Configuration templates

Lookup tables

Sample data

---

# database/

Purpose

Everything related to Odoo integration.

Contains

* XML-RPC
* Readers
* Metadata
* Database helpers

---

## database/core/

Purpose

Core implementation.

---

## database/core/config/

Purpose

Configuration handling.

Examples

Environment loader

Configuration classes

Future profile support

---

## database/core/odoo/

Purpose

Main Odoo integration layer.

---

### xmlrpc/

Purpose

Communication with Odoo.

Responsibilities

Authentication

Object service

Connection helpers

Future JSON-RPC support

---

Current Files

```text id="5eqvzm"
auth.py
object_service.py
```

---

### readers/

Purpose

Read business objects from Odoo.

Rule

One reader per business model.

Current

ModelReader

CompanyReader

Planned

PartnerReader

UserReader

ProductReader

POSOrderReader

POSSessionReader

POSPaymentReader

AccountMoveReader

AccountJournalReader

AccountReader

InventoryReader

TaxReader

PaymentReader

---

### live/

Purpose

Reserved for future live synchronization.

---

# metadata/

Purpose

Local metadata cache.

Examples

Model JSON

Field JSON

Relationship JSON

Future schema cache

---

# docs/

Purpose

Official project documentation.

No implementation code belongs here.

---

Current Documents

```text id="9j2dcs"
01_Project_Vision.md

02_Project_Objectives.md

03_Business_Requirements.md

04_System_Architecture.md

05_Repository_Structure.md

06_Development_Workflow.md

07_Git_Workflow.md

08_Implementation_Roadmap.md

09_Completed_Work.md

10_Current_Project_Status.md

11_Project_Timeline.md

12_Folder_and_File_Reference.md
```

Future documents will continue numbering sequentially.

---

# mcp/

Purpose

Model Context Protocol integration.

Future

Tool registration

Resource definitions

AI interoperability

---

# prompts/

Purpose

Prompt engineering.

Examples

Audit prompts

Report prompts

Reasoning prompts

Context templates

---

# reports/

Purpose

Generated output.

Future

PDF reports

Excel exports

CSV exports

Executive summaries

AI reports

---

# scripts/

Purpose

Automation.

Examples

Deployment

Maintenance

Utilities

Migration

Health checks

---

# sql/

Purpose

Database-related SQL.

Examples

Views

Indexes

Reporting queries

Warehouse scripts

---

# tests/

Purpose

Automated verification.

Structure

```text id="ktx53d"
tests/
├── unit/
├── integration/
├── live/
└── fixtures/
```

---

## unit/

Fast isolated tests.

Current focus.

---

## integration/

Component interaction tests.

---

## live/

Read-only tests against production Odoo.

---

## fixtures/

Reusable test data.

---

# Future Top-Level Directories

The following directories are planned but not yet implemented:

```text id="4jg4s5"
ai/
audit/
dashboards/
notifications/
plugins/
scheduler/
warehouse/
```

---

# File Ownership Rules

Each file should have:

* One responsibility.
* One logical owner.
* Clear dependencies.
* No duplicate functionality.

---

# Naming Rules

Files

snake_case.py

Classes

PascalCase

Functions

snake_case

Constants

UPPER_CASE

Feature branches

feature-name

---

# Maintenance Rules

Whenever a new file is created:

1. Place it in the correct directory.
2. Add tests if applicable.
3. Document it in this reference.
4. Update PROJECT_STATUS.md if it introduces a new capability.

---

# Guiding Principle

The repository should remain understandable even to a developer joining the project months later.

This document is the central map that makes that possible.

