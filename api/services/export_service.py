"""Export service for report data."""
import io
import json
from typing import List, Dict, Any
from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import text
from api.models.models import Report
from api.core.ast_validator import validate_query_ast, ast_to_sql
from api.services.report_service import get_report, _serialize_datetime_fields


def export_report(db: Session, sqlite_db: Session, report_id: int, format: str, user_id: int):
    """Export report data in specified format."""
    report = get_report(db, report_id, user_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Validate and execute AST
    query_ast = report.query_ast
    validate_query_ast(query_ast)
    sql, params = ast_to_sql(query_ast)
    
    result = sqlite_db.execute(text(sql), params)
    rows = result.mappings().all()
    data = [dict(row) for row in rows]
    
    # Serialize datetime fields
    data = [_serialize_datetime_fields(row) for row in data]
    
    if format == "json":
        return _export_json(data, report.name)
    elif format == "excel":
        return _export_excel(data, report.name)
    elif format == "pdf":
        return _export_pdf(data, report.name)
    else:
        raise HTTPException(status_code=400, detail="Invalid format")


def _export_json(data: List[Dict[str, Any]], report_name: str):
    """Export as JSON."""
    output = io.BytesIO()
    output.write(json.dumps(data, indent=2, default=str).encode("utf-8"))
    output.seek(0)
    
    filename = f"{report_name.replace(' ', '_')}.json"
    return StreamingResponse(
        output,
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


def _export_excel(data: List[Dict[str, Any]], report_name: str):
    """Export as Excel (XLSX)."""
    try:
        import pandas as pd
    except ImportError:
        raise HTTPException(status_code=500, detail="pandas not installed")
    
    df = pd.DataFrame(data)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Report")
    output.seek(0)
    
    filename = f"{report_name.replace(' ', '_')}.xlsx"
    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


def _export_pdf(data: List[Dict[str, Any]], report_name: str):
    """Export as PDF."""
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import letter, landscape
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
    except ImportError:
        raise HTTPException(status_code=500, detail="reportlab not installed")
    
    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=landscape(letter))
    
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"<b>{report_name}</b>", styles["Title"]))
    elements.append(Spacer(1, 12))
    
    if data:
        headers = list(data[0].keys())
        table_data = [headers]
        for row in data:
            table_data.append([str(row.get(h, "")) for h in headers])
        
        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 10),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(table)
    
    doc.build(elements)
    output.seek(0)
    
    filename = f"{report_name.replace(' ', '_')}.pdf"
    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
