class ExecutionPlanner:

    def create_plan(self, context):

        return {
            "intent": context.get("intent"),
            "entities": context.get("entities", []),
            "table": None,
            "fields": ["*"],
            "filters": {}
        }
