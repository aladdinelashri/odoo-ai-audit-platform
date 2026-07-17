class OdooFieldMapper:

    def map_field(self, field):
        return {
            "name": field.get("name"),
            "type": field.get("type"),
            "label": field.get("string")
        }
