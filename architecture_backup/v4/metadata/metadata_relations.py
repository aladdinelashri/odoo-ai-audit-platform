"""
V4 Metadata Relations

Production Architecture

Represents a relationship between two Odoo models.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class MetadataRelation:

    source_model: str

    source_table: str

    source_field: str

    target_model: str

    target_table: str

    target_field: str = "id"

    relation_type: str = "many2one"

    required: bool = False

    def join_sql(self) -> str:

        return (
            f"LEFT JOIN {self.target_table} "
            f"ON {self.target_table}.{self.target_field} = "
            f"{self.source_table}.{self.source_field}"
        )
