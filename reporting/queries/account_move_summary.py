def query():

    return """
    SELECT

        COUNT(*) AS total_moves,

        SUM(amount_total) AS total_amount,

        AVG(amount_total) AS average_amount,

        MAX(amount_total) AS maximum_amount,

        MIN(amount_total) AS minimum_amount

    FROM account_move;
    """
