def query():

    return """
    SELECT

        COUNT(*) AS total_products,

        COALESCE(SUM(quantity),0) AS total_quantity

    FROM stock_quant;
    """
