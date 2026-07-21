from dataclasses import dataclass


@dataclass(frozen=True)
class BusinessUnit:
    """
    Logical operational unit used by the audit engine.

    A Business Unit is an abstraction.

    Depending on the customer's Odoo implementation it may represent:

    - Branch
    - POS Category
    - Store
    - Warehouse
    - Department
    - Restaurant
    - Outlet
    - Production Line
    - Custom implementation

    The audit engine never depends on the actual source.
    """

    id: int | None

    code: str | None

    name: str

    source: str
