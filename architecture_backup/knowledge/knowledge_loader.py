"""
Knowledge Loader

Architecture V26
"""

from __future__ import annotations

from database.executor.postgres_executor import PostgreSQLExecutor
from database.knowledge.model_dictionary import ModelDictionary
from database.knowledge.field_dictionary import FieldDictionary


class KnowledgeLoader:

    def __init__(
        self,
        executor: PostgreSQLExecutor,
    ) -> None:

        self.executor = executor

    # ---------------------------------------------------------

    def load_models(self) -> ModelDictionary:

        dictionary = ModelDictionary()

        rows = self.executor.execute(
            """
            SELECT model, name
            FROM ir_model
            ORDER BY model;
            """
        )

        for model, name in rows:
            dictionary.add(
                model=model,
                display_name=name,
            )

        return dictionary

    # ---------------------------------------------------------

    def load_fields(self) -> FieldDictionary:

        dictionary = FieldDictionary()

        rows = self.executor.execute(
            """
            SELECT model, name, field_description
            FROM ir_model_fields
            ORDER BY model, name;
            """
        )

        for model, field, label in rows:
            dictionary.add(
                model=model,
                field=field,
                label=label,
            )

        return dictionary

    # ---------------------------------------------------------

    def load_translations(self) -> list[dict]:

        rows = self.executor.execute(
            """
            SELECT tablename
            FROM pg_tables
            WHERE schemaname = 'public';
            """
        )

        tables = {row[0] for row in rows}

        if "ir_translation" in tables:

            rows = self.executor.execute(
                """
                SELECT
                    lang,
                    type,
                    name,
                    src,
                    value
                FROM ir_translation
                WHERE value IS NOT NULL
                  AND value <> '';
                """
            )

            return [
                {
                    "lang": lang,
                    "type": type_,
                    "name": name,
                    "src": src,
                    "value": value,
                }
                for lang, type_, name, src, value in rows
            ]

        if "mail_message_translation" in tables:

            rows = self.executor.execute(
                """
                SELECT *
                FROM mail_message_translation;
                """
            )

            return [
                {
                    "row": row,
                }
                for row in rows
            ]

        return []
