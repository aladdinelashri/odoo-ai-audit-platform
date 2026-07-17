import re

from database.ai.ai_context import AIContext
from database.ai.primary_entity_resolver import PrimaryEntityResolver


class EntityDetector:

    def __init__(self):

        self.context = AIContext()

        self.resolver = PrimaryEntityResolver()

    # ---------------------------------------------------------

    def detect(self, text):

        self.context.initialize()

        entities = {

            "models": [],
            "tables": [],
            "fields": []

        }

        lowered = text.lower()

        # -------------------------------------------------
        # Detect Models
        # -------------------------------------------------

        aliases = sorted(

            self.context.business.aliases().items(),

            key=lambda x: len(x[0]),

            reverse=True

        )

        consumed = lowered

        for alias, model in aliases:

            if alias in consumed:

                if model not in entities["models"]:

                    entities["models"].append(model)

                consumed = consumed.replace(alias, " ")

        # -------------------------------------------------
        # Rank Primary Entity
        # -------------------------------------------------

        entities["models"] = self.resolver.rank(

            entities["models"]

        )

        entities["tables"] = []

        for model in entities["models"]:

            table = self.context.table(model)

            if table:

                entities["tables"].append(table)

        # -------------------------------------------------
        # Detect Fields
        # -------------------------------------------------

        words = re.findall(

            r"[A-Za-z0-9_]+",

            text

        )

        scanned_models = entities["models"][:]

        if not scanned_models:

            scanned_models = list(

                self.context.metadata.all_models().keys()

            )

        seen = set()

        for model in scanned_models:

            fields = self.context.fields(model)

            for word in words:

                if word not in fields:
                    continue

                key = (model, word)

                if key in seen:
                    continue

                seen.add(key)

                entities["fields"].append(

                    {

                        "model": model,

                        "field": word,

                        "semantic": self.context.semantic_role(

                            model,

                            word

                        )

                    }

                )

        return entities
