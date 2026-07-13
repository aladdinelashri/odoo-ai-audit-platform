# Query Engine

## Purpose

Convert natural language into an executable query plan.

---

## Responsibilities

- Detect intent
- Detect entities
- Detect filters
- Detect dates
- Detect parameters
- Detect aggregate
- Build normalized query

---

## Inputs

Natural language

---

## Outputs

Normalized Query Object

---

## Internal Components

- intent_detector.py
- entity_detector.py
- filter_detector.py
- date_resolver.py
- parameter_detector.py
- aggregate_resolver.py
- query_parser.py

---

## Public API

QueryParser.parse(text)

---

## Validation

- Intent detected
- Entity detected
- Query valid

---

## Future Extensions

- Arabic NLP
- Synonyms
- AI reasoning
- Multi-language
