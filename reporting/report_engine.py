from database.sql.executor import SQLExecutor


class ReportEngine:

    def __init__(self):

        self.db = SQLExecutor()

    def execute(self, sql):

        return self.db.execute(sql)

    # -------------------------------------------------------
    # ACCOUNT MOVE SUMMARY
    # -------------------------------------------------------

    def account_move_summary(self):

        sql = """
        SELECT
            COUNT(*) AS total_moves,
            SUM(amount_total) AS total_amount,
            AVG(amount_total) AS average_amount,
            MAX(amount_total) AS maximum_amount,
            MIN(amount_total) AS minimum_amount
        FROM account_move;
        """

        return self.execute(sql)

    # -------------------------------------------------------
    # SALES SUMMARY
    # -------------------------------------------------------

    def sales_summary(self):

        sql = """
        SELECT
            COUNT(*) AS total_orders,
            COALESCE(SUM(amount_total),0) AS total_sales,
            COALESCE(AVG(amount_total),0) AS average_order
        FROM pos_order;
        """

        return self.execute(sql)

    # -------------------------------------------------------
    # TOP SELLING PRODUCTS
    # -------------------------------------------------------

    def top_products(self, limit=20):

        sql = f"""
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

        return self.execute(sql)

    # -------------------------------------------------------
    # INVENTORY SUMMARY
    # -------------------------------------------------------

    def inventory_summary(self):

        sql = """
        SELECT
            COUNT(*) AS total_products,
            COALESCE(SUM(quantity),0) AS total_quantity
        FROM stock_quant;
        """

        return self.execute(sql)
