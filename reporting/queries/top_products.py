def query(limit=20):

    return f"""
    SELECT

        pt.name AS product,

        SUM(pol.qty) AS quantity,

        SUM(pol.price_subtotal_incl) AS sales

    FROM pos_order_line pol

    JOIN product_product pp
        ON pol.product_id = pp.id

    JOIN product_template pt
        ON pp.product_tmpl_id = pt.id

    GROUP BY pt.name

    ORDER BY sales DESC

    LIMIT {limit};
    """
