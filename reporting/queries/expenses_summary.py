def query():

    return """
    SELECT

        aa.code_store->>'en_US' AS account_code,

        aa.name->>'ar_001' AS account_name,

        COUNT(aml.id) AS entries,

        ROUND(SUM(aml.debit),2) AS total_expense

    FROM account_move_line aml

    JOIN account_account aa
         ON aml.account_id = aa.id

    WHERE aml.debit > 0

    GROUP BY
        aa.code_store,
        aa.name

    ORDER BY
        total_expense DESC

    LIMIT 20;
    """
