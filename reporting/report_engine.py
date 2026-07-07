import importlib

from database.sql.executor import SQLExecutor
from database.reportbuilder.report_compiler import ReportCompiler


class ReportEngine:

    def __init__(self):

        self.db = SQLExecutor()

        self.compiler = ReportCompiler()

    # =====================================================

    def execute(self, sql):

        return self.db.execute(sql)

    # =====================================================

    def run(self, report_name):

        try:

            sql = self.compiler.compile(report_name)

        except Exception:

            module = importlib.import_module(

                f"reporting.queries.{report_name}"

            )

            sql = module.query()

        return self.execute(sql)

    # =====================================================
    # Accounting Reports
    # =====================================================

    def account_move_summary(self):

        return self.run("account_move_summary")

    def expenses_summary(self):

        return self.run("expenses_summary")

    def journal_risk(self):

        return self.run("journal_risk")

    def missing_partner(self):

        return self.run("missing_partner")

    # =====================================================
    # Sales Reports
    # =====================================================

    def sales_summary(self):

        return self.run("sales_summary")

    def top_products(self):

        return self.run("top_products")

    # =====================================================
    # Inventory Reports
    # =====================================================

    def inventory_summary(self):

        return self.run("inventory_summary")

    # =====================================================
    # POS Reports
    # =====================================================

    def pos_refunds(self):

        return self.run("pos_refunds")

    # =====================================================
    # Dynamic Reports
    # =====================================================

    def report(self, report_name):

        return self.run(report_name)
