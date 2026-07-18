import json


class ExportEngine:

    def export_json(
        self,
        data
    ):

        return json.dumps(
            data,
            indent=4,
            default=str
        )


    def export_dict(
        self,
        data
    ):

        return dict(data)
