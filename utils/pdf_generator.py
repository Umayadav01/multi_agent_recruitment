# utils/pdf_generator.py
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph, SimpleDocTemplate, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from pathlib import Path
from typing import Dict, List

def _ensure_dir(p):
    Path(p).mkdir(parents=True, exist_ok=True)
    return Path(p)

def candidate_report_pdf(report: Dict, out_dir="outputs/reports/pdfs"):
    """
    Generate a clean PDF for a Talent Intelligence Report.
    report: dict produced by CandidateProfiler.build_report()
    """
    _ensure_dir(out_dir)
    name_safe = report["candidate"]["name"].replace(" ", "_")
    fname = Path(out_dir) / f"{name_safe}.pdf"

    doc = SimpleDocTemplate(str(fname), pagesize=A4,
                            rightMargin=20*mm, leftMargin=20*mm,
                            topMargin=20*mm, bottomMargin=20*mm)
    styles = getSampleStyleSheet()
    styleN = styles["Normal"]
    styleH = styles["Heading1"]
    styleH2 = styles["Heading2"]
    elements = []

    # Title
    elements.append(Paragraph(f"Talent Intelligence Report — {report['candidate']['name']}", styleH))
    elements.append(Spacer(1, 6))

    # Candidate basic info
    c = report["candidate"]
    info = f"<b>Role:</b> {c.get('role','-')} &nbsp;&nbsp; <b>Experience:</b> {c.get('experience_years','-')} years"
    elements.append(Paragraph(info, styleN))
    elements.append(Spacer(1, 8))

    # Career summary
    elements.append(Paragraph("Career Summary", styleH2))
    elements.append(Paragraph(report.get("career_summary","-"), styleN))
    elements.append(Spacer(1, 8))

    # Skills table
    elements.append(Paragraph("Detected Skills (with confidence)", styleH2))
    skills = report.get("skills", [])
    if skills:
        table_data = [["Skill", "Confidence"]]
        for s, conf in skills:
            table_data.append([s, str(conf)])
        t = Table(table_data, colWidths=[120*mm, 30*mm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#f0f0f0")),
            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
            ("LEFTPADDING", (0,0), (-1,-1), 6),
            ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ]))
        elements.append(t)
    else:
        elements.append(Paragraph("No skills detected.", styleN))
    elements.append(Spacer(1, 8))

    # Highlights
    elements.append(Paragraph("Highlights", styleH2))
    for h in report.get("highlights", []):
        elements.append(Paragraph(f"- {h}", styleN))
    elements.append(Spacer(1, 8))

    # Notes
    elements.append(Paragraph("Notes", styleH2))
    elements.append(Paragraph(report.get("notes",""), styleN))

    doc.build(elements)
    return str(fname)
