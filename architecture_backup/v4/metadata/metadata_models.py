"""
V4 Metadata Models

Production Architecture

Represents database models (tables) discovered from Odoo.
"""

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(slots=True)
class MetadataModel:

    model: str

    table: str

    label: str = ""

    fields: List[str] = field(default_factory=list)

    relations: List[str] = field(default_factory=list)

    indexes: List[str] = field(default_factory=list)

    statistics: Dict = field(default_factory=dict)

    def has_field(self, field_name: str) -> bool:

        return field_name in self.fields

    def add_field(self, field_name: str) -> None:

        if field_name not in self.fields:

            self.fields.append(field_name)

    def add_relation(self, relation_name: str) -> None:

        if relation_name not in self.relations:

            self.relations.append(relation_name)

    def add_index(self, index_name: str) -> None:

        if index_name not in self.indexes:

            self.indexes.append(index_name)
