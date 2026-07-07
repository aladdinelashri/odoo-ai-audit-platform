def query():

    return """
    SELECT
        COUNT(*) AS total_orders,
        COALESCE(SUM(amount_total),0) AS total_sales,
        COALESCE(AVG(amount_total),0) AS average_order
    FROM pos_order;
    """
