class QueryBuilder:

    def account_move_summary(self):

        return """
        SELECT

            COUNT(*) AS total_moves,

            SUM(amount_total) AS total_amount,

            AVG(amount_total) AS average_amount,

            MAX(amount_total) AS maximum_amount,

            MIN(amount_total) AS minimum_amount

        FROM account_move
        """

    def duplicate_payment_reference(self):

        return """
        SELECT

            payment_reference,

            COUNT(*) AS duplicates

        FROM account_move

        WHERE payment_reference IS NOT NULL

        GROUP BY payment_reference

        HAVING COUNT(*) > 1
        """

    def large_entries(self, limit=100000):

        return """
        SELECT

            id,

            name,

            amount_total,

            date

        FROM account_move

        WHERE amount_total > :limit
        """
