"""
V4 Metadata Statistics

Production Architecture

Stores statistical information used by the planner,
optimizer and AI engine.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class MetadataStatistics:

    table: str

    row_count: int = 0

    last_analyzed: str | None = None

    primary_key: str = "id"

    estimated_size: int = 0

    has_indexes: bool = False

    def is_large_table(self) -> bool:

        return self.row_count >= 100000

    def is_small_table(self) -> bool:

        return self.row_count < 10000
