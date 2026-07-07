def query():

    return """
    SELECT

        am.id,

        am.name,

        am.date,

        aj.name->>'ar_001' AS journal,

        am.move_type,

        ROUND(am.amount_total,2) AS total

    FROM account_move am

    LEFT JOIN account_journal aj
           ON aj.id = am.journal_id

    WHERE
        am.state = 'posted'
        AND am.partner_id IS NULL
        AND am.move_type IN (
            'out_invoice',
            'out_refund',
            'in_invoice',
            'in_refund'
        )

    ORDER BY
        am.date DESC;
    """
