"""Downloadable report generation for PDF, Excel, HTML, and JSON outputs."""
from __future__ import annotations

from io import BytesIO
from html import escape
from typing import Any, Dict, Iterable, List
from zipfile import ZIP_DEFLATED, ZipFile

from sqlalchemy.orm import Session

from app.models.estimation_models import Estimate
from app.models.project_models import Project
from app.models.scenario_models import Resource, Risk, Scenario


def build_project_report_payload(db: Session, project_id: int) -> Dict[str, Any]:
    """Collect all project data needed for a professional estimation report."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise ValueError("Project not found")

    estimates = db.query(Estimate).filter(Estimate.project_id == project_id).all()
    risks = db.query(Risk).filter(Risk.project_id == project_id).all()
    scenarios = db.query(Scenario).filter(Scenario.project_id == project_id).all()
    resources = db.query(Resource).filter(Resource.project_id == project_id).all()

    total_risk_exposure = sum((risk.probability or 0) * (risk.impact or 0) for risk in risks)
    latest_estimate = estimates[-1] if estimates else None
    return {
        "project": {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "status": project.status.value if hasattr(project.status, "value") else str(project.status),
            "budget": project.budget,
            "team_size": project.team_size,
            "client_name": project.client_name,
            "project_manager": project.project_manager,
            "department": project.department,
            "start_date": project.start_date.isoformat() if project.start_date else None,
            "end_date": project.end_date.isoformat() if project.end_date else None,
        },
        "summary": {
            "estimate_count": len(estimates),
            "risk_count": len(risks),
            "scenario_count": len(scenarios),
            "resource_count": len(resources),
            "total_risk_exposure": round(total_risk_exposure, 3),
            "latest_estimated_effort_hours": latest_estimate.estimated_effort_hours if latest_estimate else None,
            "latest_estimated_duration_months": latest_estimate.estimated_duration_months if latest_estimate else None,
            "latest_estimated_cost": latest_estimate.estimated_cost if latest_estimate else None,
            "latest_confidence_level": latest_estimate.confidence_level if latest_estimate else None,
        },
        "estimates": [
            {
                "method": estimate.estimation_method,
                "status": estimate.status.value if hasattr(estimate.status, "value") else str(estimate.status),
                "effort_hours": estimate.estimated_effort_hours,
                "duration_months": estimate.estimated_duration_months,
                "cost": estimate.estimated_cost,
                "team_size": estimate.estimated_team_size,
                "confidence": estimate.confidence_level,
                "actual_effort_hours": estimate.actual_effort_hours,
                "actual_duration_months": estimate.actual_duration_months,
                "actual_cost": estimate.actual_cost,
                "notes": estimate.notes,
            }
            for estimate in estimates
        ],
        "risks": [
            {
                "category": risk.category,
                "description": risk.description,
                "probability": risk.probability,
                "impact": risk.impact,
                "exposure": round((risk.probability or 0) * (risk.impact or 0), 3),
                "mitigation": risk.mitigation_strategy,
                "owner": risk.owner,
                "status": risk.status,
            }
            for risk in risks
        ],
        "scenarios": [
            {
                "name": scenario.name,
                "type": scenario.scenario_type,
                "effort": scenario.estimated_effort,
                "duration": scenario.estimated_duration,
                "cost": scenario.estimated_cost,
            }
            for scenario in scenarios
        ],
        "resources": [
            {
                "role": resource.role,
                "allocation_percentage": resource.allocation_percentage,
                "hourly_rate": resource.hourly_rate,
                "skills": resource.skills,
                "availability": resource.availability,
            }
            for resource in resources
        ],
    }


def render_html_report(payload: Dict[str, Any]) -> str:
    project = payload["project"]
    summary = payload["summary"]
    return f"""
<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>{escape(project['name'])} Estimation Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #162622; }}
    h1 {{ color: #216a5e; }}
    table {{ border-collapse: collapse; width: 100%; margin: 18px 0; }}
    th, td {{ border: 1px solid #d7cab0; padding: 8px; text-align: left; }}
    th {{ background: #ede2cc; }}
    .card {{ background: #f8f2e8; padding: 16px; border-radius: 12px; margin: 12px 0; }}
  </style>
</head>
<body>
  <h1>{escape(project['name'])}</h1>
  <p>{escape(project.get('description') or 'No project description recorded.')}</p>
  <div class="card">
    <strong>Status:</strong> {escape(project.get('status') or '')}<br>
    <strong>Budget:</strong> {project.get('budget') or 0}<br>
    <strong>Latest effort:</strong> {summary.get('latest_estimated_effort_hours') or 'N/A'} hours<br>
    <strong>Latest cost:</strong> {summary.get('latest_estimated_cost') or 'N/A'}<br>
    <strong>Risk exposure:</strong> {summary.get('total_risk_exposure')}
  </div>
  <h2>Estimates</h2>
  {render_html_table(payload['estimates'])}
  <h2>Risks</h2>
  {render_html_table(payload['risks'])}
  <h2>Scenarios</h2>
  {render_html_table(payload['scenarios'])}
  <h2>Resources</h2>
  {render_html_table(payload['resources'])}
</body>
</html>
"""


def render_html_table(rows: List[Dict[str, Any]]) -> str:
    if not rows:
        return "<p>No records available.</p>"
    headers = list(rows[0].keys())
    head = "".join(f"<th>{escape(str(header).replace('_', ' ').title())}</th>" for header in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{escape(str(row.get(header) if row.get(header) is not None else ''))}</td>" for header in headers) + "</tr>"
        for row in rows
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def render_text_lines(payload: Dict[str, Any]) -> List[str]:
    project = payload["project"]
    summary = payload["summary"]
    lines = [
        f"CASE Tool Estimation Report: {project['name']}",
        f"Status: {project.get('status')} | Client: {project.get('client_name') or 'N/A'}",
        f"Budget: {project.get('budget') or 0} | Team size: {project.get('team_size') or 'N/A'}",
        f"Latest effort: {summary.get('latest_estimated_effort_hours') or 'N/A'} hours",
        f"Latest duration: {summary.get('latest_estimated_duration_months') or 'N/A'} months",
        f"Latest cost: {summary.get('latest_estimated_cost') or 'N/A'}",
        f"Confidence: {summary.get('latest_confidence_level') or 'N/A'}%",
        f"Risk exposure: {summary.get('total_risk_exposure')}",
        "",
        "Important Risks:",
    ]
    for risk in payload["risks"][:8]:
        lines.append(f"- {risk['category']}: exposure {risk['exposure']} | {risk['description'][:92]}")
    lines.append("")
    lines.append("Estimation Methods:")
    for estimate in payload["estimates"][:8]:
        lines.append(f"- {estimate['method']}: {estimate['effort_hours']}h, {estimate['duration_months']}m, cost {estimate['cost']}")
    return lines


def render_pdf_report(payload: Dict[str, Any]) -> bytes:
    """Render a compact valid PDF using standard PDF text operators."""
    lines = render_text_lines(payload)[:45]
    stream_lines = ["BT", "/F1 11 Tf", "50 790 Td", "14 TL"]
    for line in lines:
        safe_line = str(line).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        stream_lines.append(f"({safe_line[:110]}) Tj")
        stream_lines.append("T*")
    stream_lines.append("ET")
    stream = "\n".join(stream_lines).encode("latin-1", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    pdf = BytesIO()
    pdf.write(b"%PDF-1.4\n")
    offsets = []
    for index, obj in enumerate(objects, start=1):
        offsets.append(pdf.tell())
        pdf.write(f"{index} 0 obj\n".encode())
        pdf.write(obj)
        pdf.write(b"\nendobj\n")
    xref_offset = pdf.tell()
    pdf.write(f"xref\n0 {len(objects) + 1}\n".encode())
    pdf.write(b"0000000000 65535 f \n")
    for offset in offsets:
        pdf.write(f"{offset:010d} 00000 n \n".encode())
    pdf.write(f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF".encode())
    return pdf.getvalue()


def _sheet_xml(rows: Iterable[Iterable[Any]]) -> str:
    body = []
    for row_number, row in enumerate(rows, start=1):
        cells = []
        for value in row:
            if isinstance(value, (int, float)) and value is not None:
                cells.append(f"<c><v>{value}</v></c>")
            else:
                cells.append(f"<c t=\"inlineStr\"><is><t>{escape(str(value if value is not None else ''))}</t></is></c>")
        body.append(f"<row r=\"{row_number}\">{''.join(cells)}</row>")
    return "<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?><worksheet xmlns=\"http://schemas.openxmlformats.org/spreadsheetml/2006/main\"><sheetData>" + "".join(body) + "</sheetData></worksheet>"


def render_xlsx_report(payload: Dict[str, Any]) -> bytes:
    sheets = {
        "Summary": [
            ["Metric", "Value"],
            ["Project", payload["project"]["name"]],
            ["Status", payload["project"]["status"]],
            ["Budget", payload["project"].get("budget") or 0],
            ["Latest Effort Hours", payload["summary"].get("latest_estimated_effort_hours") or ""],
            ["Latest Duration Months", payload["summary"].get("latest_estimated_duration_months") or ""],
            ["Latest Cost", payload["summary"].get("latest_estimated_cost") or ""],
            ["Risk Exposure", payload["summary"].get("total_risk_exposure") or 0],
        ],
        "Estimates": _rows_from_dicts(payload["estimates"]),
        "Risks": _rows_from_dicts(payload["risks"]),
        "Scenarios": _rows_from_dicts(payload["scenarios"]),
        "Resources": _rows_from_dicts(payload["resources"]),
    }
    workbook_sheets = "".join(
        f"<sheet name=\"{escape(name)}\" sheetId=\"{index}\" r:id=\"rId{index}\"/>"
        for index, name in enumerate(sheets.keys(), start=1)
    )
    workbook_rels = "".join(
        f"<Relationship Id=\"rId{index}\" Type=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet\" Target=\"worksheets/sheet{index}.xml\"/>"
        for index in range(1, len(sheets) + 1)
    )
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as archive:
        archive.writestr("[Content_Types].xml", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
""" + "".join(f'<Override PartName="/xl/worksheets/sheet{index}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for index in range(1, len(sheets) + 1)) + "</Types>")
        archive.writestr("_rels/.rels", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>""")
        archive.writestr("xl/workbook.xml", f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>{workbook_sheets}</sheets></workbook>""")
        archive.writestr("xl/_rels/workbook.xml.rels", f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">{workbook_rels}</Relationships>""")
        for index, rows in enumerate(sheets.values(), start=1):
            archive.writestr(f"xl/worksheets/sheet{index}.xml", _sheet_xml(rows))
    return buffer.getvalue()


def _rows_from_dicts(rows: List[Dict[str, Any]]) -> List[List[Any]]:
    if not rows:
        return [["No records"]]
    headers = list(rows[0].keys())
    return [headers] + [[row.get(header) for header in headers] for row in rows]
