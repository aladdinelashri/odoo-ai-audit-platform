import pytest
from database.core.reporting.exports import export_excel, export_pdf, _normalize_rows, _get_columns
import sqlite3
from io import BytesIO
import openpyxl

def test_normalize_rows():
    # Simulate sqlite3.Row objects
    class MockRow(dict):
        def keys(self):
            return super().keys()
    row1 = MockRow({"a": 1, "b": 2})
    rows = [row1]
    normalized = _normalize_rows(rows)
    assert normalized == [{"a": 1, "b": 2}]

def test_get_columns():
    row = {"name": "Alice", "age": 30}
    rows = [row]
    cols = _get_columns(rows)
    assert cols == ["name", "age"]

def test_export_excel():
    rows = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    excel_bytes = export_excel(rows)
    wb = openpyxl.load_workbook(BytesIO(excel_bytes))
    ws = wb.active
    data = [list(row) for row in ws.iter_rows(values_only=True)]
    assert data[0] == ["name", "age"]
    assert data[1] == ["Alice", 30]
    assert data[2] == ["Bob", 25]

def test_export_pdf():
    rows = [{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}]
    pdf_bytes = export_pdf(rows)
    assert pdf_bytes.startswith(b'%PDF')
