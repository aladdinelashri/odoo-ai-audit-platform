"""
Metadata Cache

Architecture V50
"""

from __future__ import annotations

from database.services.metadata_loader import MetadataLoader


class MetadataCache:

    def __init__(self) -> None:

        self.loader = MetadataLoader()

        self.companies = []
        self.pos_configs = []
        self.journals = []
        self.products = []
        self.partners = []
        self.warehouses = []

    # ---------------------------------------------------------

    def load(self) -> None:

        self.companies = self.loader.load_companies()
        self.pos_configs = self.loader.load_pos_configs()
        self.journals = self.loader.load_journals()
        self.products = self.loader.load_products()
        self.partners = self.loader.load_partners()
        self.warehouses = self.loader.load_warehouses()

    # ---------------------------------------------------------

    def _find_by_name(
        self,
        collection: list[dict],
        text: str,
    ) -> dict | None:

        text = text.lower()

        for item in collection:

            if item["name"].lower() == text:
                return item

        return None

    # ---------------------------------------------------------

    def find_company(
        self,
        text: str,
    ) -> dict | None:

        return self._find_by_name(
            self.companies,
            text,
        )

    # ---------------------------------------------------------

    def find_pos_config(
        self,
        text: str,
    ) -> dict | None:

        return self._find_by_name(
            self.pos_configs,
            text,
        )

    # ---------------------------------------------------------

    def find_journal(
        self,
        text: str,
    ) -> dict | None:

        return self._find_by_name(
            self.journals,
            text,
        )

    # ---------------------------------------------------------

    def find_product(
        self,
        text: str,
    ) -> dict | None:

        return self._find_by_name(
            self.products,
            text,
        )

    # ---------------------------------------------------------

    def find_partner(
        self,
        text: str,
    ) -> dict | None:

        return self._find_by_name(
            self.partners,
            text,
        )

    # ---------------------------------------------------------

    def find_warehouse(
        self,
        text: str,
    ) -> dict | None:

        return self._find_by_name(
            self.warehouses,
            text,
        )
