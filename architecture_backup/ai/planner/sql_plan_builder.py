"""
SQL Plan Builder

Architecture V9

Combines all planners into a single logical SQL plan.
"""

from __future__ import annotations

from database.ai.query.business_query import BusinessQuery
from database.ai.planner.select_planner import SelectPlanner
from database.ai.planner.from_planner import FromPlanner
from database.ai.planner.where_planner import WherePlanner
from database.ai.planner.order_planner import OrderPlanner
from database.ai.planner.limit_planner import LimitPlanner


class SQLPlanBuilder:

    def __init__(self) -> None:

        self.select = SelectPlanner()
        self.from_ = FromPlanner()
        self.where = WherePlanner()
        self.order = OrderPlanner()
        self.limit = LimitPlanner()

    # ---------------------------------------------------------

    def build(self, query: BusinessQuery) -> dict:

        return {
            "select": self.select.build(query),
            "from": self.from_.build(query),
            "where": self.where.build(query),
            "order": self.order.build(query),
            "limit": self.limit.build(query),
        }
