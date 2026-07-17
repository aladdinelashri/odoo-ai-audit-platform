"""
Translation Registry

Architecture V26

Stores and resolves multilingual business terms.
"""

from __future__ import annotations


class TranslationRegistry:

    def __init__(self) -> None:

        self._translations: dict[str, str] = {}

    # ---------------------------------------------------------

    def register(
        self,
        term: str,
        model: str,
    ) -> None:

        self._translations[term.lower()] = model

    # ---------------------------------------------------------

    def lookup(
        self,
        term: str,
    ) -> str | None:

        return self._translations.get(term.lower())

    # ---------------------------------------------------------

    def count(self) -> int:

        return len(self._translations)
