class RequestValidator:

    def validate(
        self,
        request
    ):

        required = [
            "question"
        ]

        missing = [
            field
            for field in required
            if field not in request
        ]

        return {
            "valid": len(missing) == 0,
            "missing": missing
        }
