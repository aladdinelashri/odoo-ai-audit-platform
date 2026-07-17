# Relationship Reasoning

Purpose:

Automatically discover table relationships without manual joins.

Components:

- Graph
- PathFinder
- JoinReasoner

Responsibilities:

- Build relationship graph from catalog.
- Find shortest path between tables.
- Generate required joins automatically.
- Support multi-hop joins.
- Remove manual join definitions from planners.
