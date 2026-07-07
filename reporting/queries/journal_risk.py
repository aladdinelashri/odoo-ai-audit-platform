def query():

    return """
    SELECT

        am.id,

        am.name,

        am.date,

        aj.name->>'ar_001' AS journal,

        rp.name AS partner,

        ROUND(am.amount_total,2) AS total,

        CASE

            WHEN am.amount_total >= 100000 THEN 'HIGH'

            WHEN am.amount_total >= 50000 THEN 'MEDIUM'

            ELSE 'LOW'

        END AS risk

    FROM account_move am

    LEFT JOIN account_journal aj
           ON aj.id = am.journal_id

    LEFT JOIN res_partner rp
           ON rp.id = am.partner_id

    WHERE am.state='posted'

    ORDER BY
        am.amount_total DESC

    LIMIT 100;
    """
