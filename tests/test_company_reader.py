from database.core.odoo.readers.company_reader import CompanyReader


def test_company_reader_import():
    assert CompanyReader is not None


def test_company_reader_methods():
    reader = CompanyReader()

    assert hasattr(reader, "all")
    assert hasattr(reader, "first")
