class JoinBuilder:

    def build(self, joins):

        if not joins:
            return ""

        statements = []

        for join in joins:
            statements.append(
                f" JOIN {join['table']} ON {join['condition']}"
            )

        return "".join(statements)
