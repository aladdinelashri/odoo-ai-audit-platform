def query():

    return """
    SELECT

        po.name,

        po.date_order,

        pc.name AS pos,

        COALESCE(rp.name,'') AS customer,

        pol.full_product_name,

        pol.qty,

        ROUND(pol.price_subtotal,2) AS price_subtotal,

        pol.refunded_orderline_id

    FROM pos_order_line pol

    JOIN pos_order po
        ON po.id = pol.order_id

    LEFT JOIN pos_config pc
        ON pc.id = po.config_id

    LEFT JOIN res_partner rp
        ON rp.id = po.partner_id

    WHERE pol.refunded_orderline_id IS NOT NULL

    ORDER BY po.date_order DESC;
    """
