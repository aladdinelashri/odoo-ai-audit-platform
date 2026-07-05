from database.discovery.inspector import SchemaInspector
from database.discovery.columns import ColumnDiscovery
from database.discovery.primary_keys import PrimaryKeyDiscovery
from database.discovery.foreign_keys import ForeignKeyDiscovery
from database.discovery.indexes import IndexDiscovery
from database.discovery.constraints import ConstraintDiscovery
from database.discovery.views import ViewDiscovery
from database.discovery.exporter import SchemaExporter


def run():

    print()
    print("=== Database Discovery ===")
    print()

    inspector = SchemaInspector()
    column_discovery = ColumnDiscovery()
    primary_key_discovery = PrimaryKeyDiscovery()
    foreign_key_discovery = ForeignKeyDiscovery()
    index_discovery = IndexDiscovery()
    constraint_discovery = ConstraintDiscovery()
    view_discovery = ViewDiscovery()

    exporter = SchemaExporter()

    print("Discovering tables...")
    tables = inspector.get_tables()
    exporter.export_tables(tables)

    print()

    print("Discovering columns...")
    columns = column_discovery.discover()
    exporter.export_columns(columns)

    print()

    print("Discovering primary keys...")
    primary_keys = primary_key_discovery.discover()
    exporter.export_primary_keys(primary_keys)

    print()

    print("Discovering foreign keys...")
    foreign_keys = foreign_key_discovery.discover()
    exporter.export_foreign_keys(foreign_keys)

    print()

    print("Discovering indexes...")
    indexes = index_discovery.discover()
    exporter.export_indexes(indexes)

    print()

    print("Discovering constraints...")
    constraints = constraint_discovery.discover()
    exporter.export_constraints(constraints)

    print()

    print("Discovering views...")
    views = view_discovery.discover()
    exporter.export_views(views)

    print()

    print("===================================")
    print(" Database Discovery Completed")
    print("===================================")
