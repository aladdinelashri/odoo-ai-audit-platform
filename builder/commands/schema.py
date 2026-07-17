from pathlib import Path
import json

from database.connection.postgres_connection import PostgreSQLConnection


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "database" / "schema"


def run(model_name):

    connection = PostgreSQLConnection().open()

    try:

        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT
                    model,
                    name,
                    ttype,
                    relation
                FROM ir_model_fields
                WHERE model = %s
                ORDER BY name
                """,
                (model_name,),
            )

            rows = cursor.fetchall()

        metadata = {
            "model": model_name,
            "table": model_name.replace(".", "_"),
            "fields": [
                {
                    "name": row[1],
                    "type": row[2],
                    "relation": row[3],
                }
                for row in rows
            ],
        }

        OUTPUT.mkdir(parents=True, exist_ok=True)

        output_file = OUTPUT / f"{model_name}.json"

        with open(output_file, "w", encoding="utf-8") as f:

            json.dump(
                metadata,
                f,
                indent=4,
                ensure_ascii=False,
            )

        print(f"Schema generated:\n{output_file}")

    finally:

        connection.close()
