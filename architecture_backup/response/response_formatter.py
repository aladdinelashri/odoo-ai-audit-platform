class ResponseFormatter:

    def __init__(self):
        pass

    # ---------------------------------------------------------

    def format(self, rows):

        # -----------------------------------------
        # Error
        # -----------------------------------------

        if isinstance(rows, Exception):

            return {
                "success": False,
                "count": 0,
                "rows": [],
                "error": str(rows)
            }

        # -----------------------------------------
        # Empty
        # -----------------------------------------

        if rows is None:

            return {
                "success": True,
                "count": 0,
                "rows": []
            }

        if len(rows) == 0:

            return {
                "success": True,
                "count": 0,
                "rows": []
            }

        # -----------------------------------------
        # Aggregate
        # -----------------------------------------

        if len(rows) == 1:

            row = rows[0]

            if len(row.keys()) == 1:

                key = list(row.keys())[0]

                if key.lower() in (

                    "count",
                    "sum",
                    "avg",
                    "average",
                    "min",
                    "max"

                ):

                    return {

                        "success": True,

                        "count": 1,

                        "rows": rows,

                        "value": row[key]

                    }

        # -----------------------------------------
        # List
        # -----------------------------------------

        return {

            "success": True,

            "count": len(rows),

            "rows": rows

        }
