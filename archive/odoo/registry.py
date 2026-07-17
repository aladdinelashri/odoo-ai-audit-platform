from database.odoo.metadata_service import MetadataService
from database.odoo.knowledge_catalog import KnowledgeCatalog
from database.odoo.semantic_registry import SemanticRegistry
from database.odoo.business_registry import BusinessRegistry
from database.odoo.model_table_registry import ModelTableRegistry
from database.odoo.relation_registry import RelationRegistry
from database.odoo.field_registry import FieldRegistry

metadata_service = MetadataService()

knowledge_catalog = KnowledgeCatalog()

semantic_registry = SemanticRegistry()

business_registry = BusinessRegistry()

model_table_registry = ModelTableRegistry()

relation_registry = RelationRegistry()

field_registry = FieldRegistry()
