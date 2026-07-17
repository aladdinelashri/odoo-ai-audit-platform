# Metadata Layer

## Purpose

Provide one unified metadata service for the entire platform.

---

## Responsibilities

- Load metadata
- Validate metadata
- Cache metadata
- Expose models
- Expose fields
- Expose relations
- Expose statistics

---

## Inputs

- metadata/*.json

---

## Outputs

- MetadataModel
- MetadataField
- MetadataRelation
- MetadataStatistics

---

## Internal Components

- metadata_loader.py
- metadata_models.py
- metadata_fields.py
- metadata_relations.py
- metadata_statistics.py
- metadata_cache.py
- metadata_engine.py

---

## Public API

```python
engine.all_models()

engine.model(name)

engine.table(model)

engine.fields(model)

engine.field(model, field)

engine.relations(model)

engine.statistics(model)
```

---

## Caching Strategy

- Load once
- Memory cache
- Read only

---

## Data Sources

database/metadata/

---

## Validation

- Model exists
- Table exists
- Fields exist
- Relations valid

---

## Future Extensions

- Live database metadata
- Auto refresh
- Incremental cache
- Multi database support
