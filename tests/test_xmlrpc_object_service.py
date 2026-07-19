from database.core.odoo.xmlrpc.object_service import XMLRPCObjectService


def test_object_service_can_be_imported():
    assert XMLRPCObjectService is not None


def test_object_service_has_execute():
    assert hasattr(XMLRPCObjectService, "execute")


def test_object_service_has_search():
    assert hasattr(XMLRPCObjectService, "search")


def test_object_service_has_search_read():
    assert hasattr(XMLRPCObjectService, "search_read")
