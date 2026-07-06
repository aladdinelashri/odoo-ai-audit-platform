class RiskFactorBuilder:

    def calculate(self, table):

        score = 0

        score += len(table.get("columns", []))

        score += len(table.get("foreign_keys", [])) * 3

        score += len(table.get("indexes", []))

        score += len(table.get("constraints", []))

        score += len(table.get("sensitive_fields", [])) * 5

        return score
