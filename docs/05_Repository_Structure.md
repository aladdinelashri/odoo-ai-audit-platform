# Repository Structure

Version: 1.0

Status: Living Document

---

# Purpose

This document describes the structure of the Git repository and the responsibility of every major directory.

The objective is to ensure that every developer understands where code belongs before implementing new functionality.

---

# Repository Overview

```text
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
├── .gitignore
├── CHANGELOG.md
├── PROJECT_STATUS.md
├── README.md
└── ROADMAP.md
```

---

# Root Files

## README.md

Entry point of the project.

Contains

* Project introduction
* Installation
* Quick start
* Documentation links

---

## ROADMAP.md

High-level implementation roadmap.

Contains

* Current phase
* Future phases
* Major milestones

---

## PROJECT_STATUS.md

Tracks project progress.

Contains

* Completed features
* Current feature
* Next feature
* Known issues

---

## CHANGELOG.md

Project history.

Every completed feature should appear here.

---

# Directories

---

## assets/

Purpose

Project assets.

Examples

Images

Logos

Architecture diagrams

Icons

Screenshots

---

## builder/

Purpose

Developer tools.

Responsibilities

Metadata generation

Model inspection

Schema discovery

Future code generation

---

## data/

Purpose

Static project data.

Examples

Reference tables

Business dictionaries

Templates

Sample datasets

---

## database/

Purpose

Everything related to Odoo integration.

Contains

Database connectivity

Metadata

Readers

XML-RPC

Future ORM helpers

---

Structure

```text
database/
│
├── core/
├── metadata/
└── cache/
```

---

## database/core/

Main implementation.

Contains

Configuration

Database layer

Odoo connectors

Readers

Authentication

Business interfaces

---

Structure

```text
database/core/
│
├── config/
└── odoo/
```

---

## database/core/odoo/

Main Odoo integration layer.

Structure

```text
database/core/odoo/
│
├── readers/
├── xmlrpc/
└── live/
```

---

### readers/

Contains one reader per Odoo model.

Examples

CompanyReader

ModelReader

POSOrderReader

AccountMoveReader

JournalReader

ProductReader

PartnerReader

InventoryReader

---

### xmlrpc/

Contains

Authentication

Object Service

Connection helpers

Future JSON-RPC support

---

### live/

Reserved for future live synchronization logic.

---

## metadata/

Stores cached metadata.

Examples

Model definitions

Field definitions

Relationships

Generated JSON

---

## docs/

Complete project documentation.

This directory becomes the official knowledge base of the project.

No implementation belongs here.

---

## mcp/

Future MCP integration.

Responsibilities

Agent communication

Tool registration

MCP resources

---

## prompts/

Prompt engineering.

Examples

Audit prompts

Context prompts

Reporting prompts

Reasoning prompts

---

## reports/

Generated reports.

Future contents

PDF

Excel

CSV

AI reports

Executive reports

---

## scripts/

Automation scripts.

Examples

Deployment

Maintenance

Database utilities

Migration

---

## sql/

SQL scripts.

Examples

Views

Indexes

Queries

Warehouse scripts

---

## tests/

Automated testing.

Future structure

```text
tests/
│
├── unit/
├── integration/
├── live/
└── fixtures/
```

---

### unit/

Fast isolated tests.

---

### integration/

Tests against project modules.

---

### live/

Tests against production read-only environment.

---

### fixtures/

Reusable test data.

---

# Future Directories

As the project grows, additional directories may be introduced.

Examples

```text
ai/
audit/
dashboards/
plugins/
scheduler/
notifications/
warehouse/
```

---

# Directory Rules

Every directory must have one responsibility.

Business logic must never appear inside XML-RPC modules.

Readers must never perform auditing.

Audit modules must never connect directly to Odoo.

Only the XML-RPC layer communicates with Odoo.

Every new feature should fit naturally into the existing architecture rather than creating new top-level folders.

---

# Repository Philosophy

The repository is organized around responsibilities instead of technologies.

This approach improves

Maintainability

Scalability

Developer onboarding

Testing

Long-term evolution

