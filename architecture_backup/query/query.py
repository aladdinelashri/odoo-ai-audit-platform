from dataclasses import dataclass, field


@dataclass
class Query:

    model: str | None = None

    table: str | None = None

    fields: list = field(default_factory=list)

    filters: list = field(default_factory=list)

    joins: list = field(default_factory=list)

    group_by: list = field(default_factory=list)

    order_by: list = field(default_factory=list)

    aggregate: dict | None = None

    limit: int = 100
