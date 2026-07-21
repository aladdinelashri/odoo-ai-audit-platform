from .model_loader_service import ModelLoaderService


class ObjectTraverser:

    def __init__(self):

        self.loader = ModelLoaderService()

    def traverse(self, start_model, start_record, path):

        current_record = start_record

        for step in path:

            field = step["field"]
            next_model = step["model"]

            value = current_record.get(field)

            if value is None:
                return None

            if isinstance(value, list):

                if not value:
                    return None

                record_id = value[0]

            else:

                record_id = value

            current_record = self.loader.load(
                next_model,
                record_id,
            )

            if current_record is None:
                return None

        return current_record
