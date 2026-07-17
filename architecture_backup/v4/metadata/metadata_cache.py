"""
V4 Metadata Cache

Production Architecture

Thread-safe in-memory cache for metadata objects.
"""

from __future__ import annotations

from threading import RLock


class MetadataCache:

    def __init__(self):

        self._lock = RLock()

        self._cache = {}

    # ---------------------------------------------------------

    def has(self, key: str) -> bool:

        with self._lock:

            return key in self._cache

    # ---------------------------------------------------------

    def get(self, key: str):

        with self._lock:

            return self._cache.get(key)

    # ---------------------------------------------------------

    def set(self, key: str, value):

        with self._lock:

            self._cache[key] = value

    # ---------------------------------------------------------

    def remove(self, key: str):

        with self._lock:

            self._cache.pop(key, None)

    # ---------------------------------------------------------

    def clear(self):

        with self._lock:

            self._cache.clear()

    # ---------------------------------------------------------

    def keys(self):

        with self._lock:

            return list(self._cache.keys())

    # ---------------------------------------------------------

    def values(self):

        with self._lock:

            return list(self._cache.values())

    # ---------------------------------------------------------

    def size(self):

        with self._lock:

            return len(self._cache)
