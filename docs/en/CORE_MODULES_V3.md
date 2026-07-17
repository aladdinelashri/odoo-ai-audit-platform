# Odoo AI Audit Platform

# Core Modules V3

Status: Official

Architecture Version: V3

---

# Purpose

This document defines the official implementation modules of Architecture V3.

Only the modules listed here are allowed to evolve during V3 development.

Any duplicate implementation outside these modules is considered Legacy.

---

# Core Layer 1 — Metadata

Responsible for understanding Odoo.

Components

* MetadataService
* KnowledgeCatalog
* BusinessRegistry
* SemanticRegistry
* RelationRegistry
* ModelTableRegistry

Responsibilities

* Load metadata
* Resolve models
* Resolve fields
* Resolve relations
* Resolve business aliases

---

# Core Layer 2 — AI

Responsible for Natural Language Understanding.

Components

* QueryParser
* IntentDetector
* EntityDetector
* ParameterDetector
* FilterDetector
* AggregateResolver
* DateResolver
* JoinResolver
* PrimaryEntityResolver

Responsibilities

* Parse user requests
* Detect business entities
* Detect filters
* Detect aggregations
* Produce normalized query objects

---

# Core Layer 3 — Planning

Components

* ExecutionPlanner

Responsibilities

* Convert AI output into execution plans
* Generate joins
* Generate ordering
* Generate grouping
* Select default fields

---

# Core Layer 4 — SQL

Components

* SQLBuilder
* SQLValidator
* SQLExecutor

Responsibilities

* Generate SQL
* Validate SQL
* Execute SQL

---

# Core Layer 5 — Response

Components

* ResponseFormatter

Responsibilities

* Normalize SQL results
* Format aggregate results
* Format list results
* Format empty results
* Format errors

---

# Core Layer 6 — Reporting

Components

* ReportParser
* ReportCompiler
* ReportValidator

Responsibilities

* Report templates
* Report execution
* Dashboard generation

---

# Core Layer 7 — Audit

Components

* Audit Rules
* ISA Rules
* Risk Engine
* Fraud Detection

Responsibilities

* Accounting validation
* Compliance
* Risk scoring

---

# Core Layer 8 — Integration

Components

* REST API
* Telegram
* n8n
* Hermes
* OpenClaw

Responsibilities

* External communication
* Scheduling
* Notifications
* AI agents

---

# Legacy Modules

Existing duplicate implementations remain in the repository temporarily.

They must not be modified.

They will be removed after V3 reaches functional parity.

---

# Development Rule

Every new feature must belong to exactly one Core Module.

Cross-module responsibilities are prohibited.

