import json
from pathlib import Path


class Localization:

    def __init__(self, language="en"):

        self.language = language

        self.base = Path("locales")

        self.cache = {}

    def load(self, file_name):

        key = f"{self.language}/{file_name}"

        if key in self.cache:
            return self.cache[key]

        path = self.base / self.language / file_name

        if not path.exists():
            return {}

        with open(path, encoding="utf-8") as f:

            data = json.load(f)

        self.cache[key] = data

        return data

    def text(self, file_name, key):

        data = self.load(file_name)

        return data.get(key, key)
