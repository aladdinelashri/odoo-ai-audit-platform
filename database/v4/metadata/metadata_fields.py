"""
V4 Metadata Fields

Production Architecture

Represents a database field discovered from Odoo.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class MetadataField:

    model: str

    table: str

    name: str

    label: str

    data_type: str

    relation: str | None = None

    semantic_role: str = "other"

    required: bool = False

    indexed: bool = False

    readonly: bool = False

    stored: bool = True

    searchable: bool = True

    sortable: bool = True

    aggregatable: bool = False

    def is_relation(self) -> bool:

        return self.relation is not None

    def is_numeric(self) -> bool:

        return self.data_type in {

            "integer",

            "float",

            "monetary",

            "numeric"

        }

    def is_date(self) -> bool:

        return self.data_type in {

            "date",

            "datetime"

        }
