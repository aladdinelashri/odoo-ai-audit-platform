# System Architecture

Version: 1.0

Status: Living Document

---

# Introduction

This document describes the technical architecture of the Odoo AI Audit Platform.

The architecture is modular by design.

Every component has a single responsibility.

Components communicate through well-defined interfaces.

---

# High-Level Architecture

```text
                    +---------------------------+
                    |        End User           |
                    +-------------+-------------+
                                  |
                                  v
                    +---------------------------+
                    |      AI Audit Platform    |
                    +-------------+-------------+
                                  |
        +-------------------------+-------------------------+
        |                         |                         |
        v                         v                         v
+----------------+      +----------------+      +------------------+
| XML-RPC Layer  |      | Metadata Layer |      | AI Context Layer |
+----------------+      +----------------+      +------------------+
        |                         |                         |
        +-------------------------+-------------------------+
                                  |
                                  v
                    +---------------------------+
                    |      Business Readers     |
                    +-------------+-------------+
                                  |
                                  v
                    +---------------------------+
                    |      Audit Engine         |
                    +-------------+-------------+
                                  |
                                  v
                    +---------------------------+
                    | Reporting & Dashboards    |
                    +---------------------------+
                                  |
                                  v
                    +---------------------------+
                    |      Odoo Production      |
                    +---------------------------+
```

---

# Architectural Principles

## Modular

Every module performs one responsibility.

Modules should never depend on implementation details of other modules.

---

## Read-Only

No production data is modified.

Every connector uses read-only operations.

---

## Layered

Presentation

↓

Business Logic

↓

Readers

↓

Connectors

↓

Odoo

---

## Extensible

Every layer should support future extensions without redesign.

---

# Core Layers

---

## 1. Configuration Layer

Responsibilities

Environment variables

Project configuration

Secrets

Connection settings

Future configuration profiles

---

Directory

```text
database/core/config
```

---

## 2. XML-RPC Layer

Responsibilities

Authentication

Connection management

execute_kw wrappers

Object service

Future JSON-RPC compatibility

---

Directory

```text
database/core/odoo/xmlrpc
```

---

## 3. Readers Layer

Responsibilities

Read one business model.

No business logic.

No reporting.

No AI.

Only data retrieval.

Examples

Company Reader

POS Reader

Journal Reader

Account Reader

Tax Reader

Inventory Reader

Partner Reader

---

Directory

```text
database/core/odoo/readers
```

---

## 4. Metadata Layer

Responsibilities

Model discovery

Field discovery

Relationship discovery

Metadata cache

Schema inspection

---

Directory

```text
database/metadata
```

---

## 5. Audit Engine

Responsibilities

Business rules

Risk rules

Exception detection

Accounting validation

Future AI integration

---

Directory

```text
audit/
```

(Currently planned)

---

## 6. AI Context Layer

Responsibilities

Collect evidence

Build prompts

Summarize data

Prepare AI requests

Support explainability

---

Directory

```text
ai/
```

(Currently planned)

---

## 7. Reporting Layer

Responsibilities

Audit reports

Executive summaries

Dashboards

Exports

PDF

Excel

CSV

---

Directory

```text
reports/
```

(Currently planned)

---

# Odoo Integration

Current

XML-RPC

Future

JSON-RPC

REST (if available)

MCP

---

# Database Integration

Current

Live Odoo PostgreSQL

Metadata cache

Future

Warehouse

Analytics database

Historical snapshots

---

# AI Integration

Current

Prompt architecture

Context preparation

Future

OpenAI

Local LLMs

Multi-agent workflows

Reasoning engine

---

# Security Model

Environment variables

Read-only users

Least privilege

Credential isolation

No hardcoded secrets

No production modifications

---

# Folder Responsibilities

```text
database/
```

Database integration

Metadata

Connectors

Readers

---

```text
docs/
```

Project documentation

Architecture

Workflow

Standards

---

```text
tests/
```

Testing

Unit tests

Integration tests

Future live tests

---

```text
scripts/
```

Utility scripts

Automation

Maintenance

---

```text
builder/
```

Metadata generation

Model inspection

Development utilities

---

# Future Architecture

Future versions will introduce

Audit Engine

Rule Engine

AI Engine

Dashboard Engine

Plugin System

Notification System

Background Scheduler

API Layer

MCP Integration

n8n Integration

---

# Architecture Goals

Security

Maintainability

Scalability

Modularity

Extensibility

Testability

Production readiness
