import os
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    KeepTogether,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from app.config import settings
from app.models.inspection import Inspection
from app.models.report import Report
from app.models.user import User
from app.utils.helpers import generate_report_number
from app.services.inspection_service import inspection_service


class ReportService:
    def __init__(self, reports_dir: str = settings.REPORT_DIR):
        self.reports_dir = reports_dir
        os.makedirs(self.reports_dir, exist_ok=True)

    def generate_pdf_report(self, db: Session, inspection_id_or_str: str | int, user_id: int) -> Report:
        inspection = inspection_service.get_inspection_by_id(db, inspection_id_or_str)
        if not inspection:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "INSPECTION_NOT_FOUND", "message": "Inspection not found."},
            )

        report_num = generate_report_number()
        pdf_filename = f"{report_num}.pdf"
        pdf_path = os.path.join(self.reports_dir, pdf_filename)

        # Build Document
        doc = SimpleDocTemplate(
            pdf_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36,
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Heading1"],
            fontSize=18,
            leading=22,
            textColor=colors.HexColor("#0f172a"),
            alignment=1,  # Center
        )
        subtitle_style = ParagraphStyle(
            "DocSubTitle",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#475569"),
            alignment=1,
        )
        h2_style = ParagraphStyle(
            "Heading2Custom",
            parent=styles["Heading2"],
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#1e293b"),
            spaceBefore=12,
            spaceAfter=6,
        )
        body_style = ParagraphStyle(
            "BodyCustom",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#334155"),
        )
        badge_pass = ParagraphStyle(
            "BadgePass",
            parent=styles["Normal"],
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#15803d"),
        )
        badge_review = ParagraphStyle(
            "BadgeReview",
            parent=styles["Normal"],
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#b45309"),
        )

        story = []

        # Header Title
        story.append(Paragraph("DIRECTORATE OF LEGAL METROLOGY", title_style))
        story.append(Paragraph("AI-Assisted Packaged Commodity Compliance Inspection Report", subtitle_style))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0284c7"), spaceAfter=15))

        # 1. Summary Block Table
        inspector_name = inspection.inspector.name if inspection.inspector else "N/A"
        date_str = inspection.inspection_date.strftime("%Y-%m-%d %H:%M UTC") if inspection.inspection_date else "N/A"

        meta_data = [
            [
                Paragraph("<b>Inspection ID:</b>", body_style),
                Paragraph(inspection.inspection_id, body_style),
                Paragraph("<b>Report Number:</b>", body_style),
                Paragraph(report_num, body_style),
            ],
            [
                Paragraph("<b>Inspection Date:</b>", body_style),
                Paragraph(date_str, body_style),
                Paragraph("<b>Inspector:</b>", body_style),
                Paragraph(inspector_name, body_style),
            ],
            [
                Paragraph("<b>Location:</b>", body_style),
                Paragraph(inspection.location, body_style),
                Paragraph("<b>AI Compliance Score:</b>", body_style),
                Paragraph(f"<b>{inspection.compliance_score:.1f}%</b> ({inspection.status.value})", body_style),
            ],
        ]
        meta_table = Table(meta_data, colWidths=[100, 160, 110, 170])
        meta_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        story.append(meta_table)
        story.append(Spacer(1, 12))

        # 2. Product Specifications
        story.append(Paragraph("1. Product Specifications", h2_style))
        product = inspection.product
        prod_data = [
            [
                Paragraph("<b>Product Name:</b>", body_style),
                Paragraph(product.product_name if product else "N/A", body_style),
                Paragraph("<b>Brand:</b>", body_style),
                Paragraph(product.brand or "N/A", body_style),
            ],
            [
                Paragraph("<b>Category:</b>", body_style),
                Paragraph(product.category or "Packaged Commodity", body_style),
                Paragraph("<b>Batch Number:</b>", body_style),
                Paragraph(product.batch_number or "N/A", body_style),
            ],
            [
                Paragraph("<b>Manufacturer:</b>", body_style),
                Paragraph(product.manufacturer or "N/A", body_style),
                Paragraph("<b>Packer / Importer:</b>", body_style),
                Paragraph(product.packer or product.importer or "N/A", body_style),
            ],
        ]
        prod_table = Table(prod_data, colWidths=[100, 160, 110, 170])
        prod_table.setStyle(
            TableStyle(
                [
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                    ("TOPPADDING", (0, 0), (-1, -1), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ]
            )
        )
        story.append(prod_table)
        story.append(Spacer(1, 12))

        # 3. Declaration Analysis Breakdown
        story.append(Paragraph("2. Packaging Declaration Analysis", h2_style))
        decl_headers = [
            Paragraph("<b>Declaration</b>", body_style),
            Paragraph("<b>Detected Value</b>", body_style),
            Paragraph("<b>Confidence</b>", body_style),
            Paragraph("<b>Status</b>", body_style),
        ]
        decl_rows = [decl_headers]
        for d in inspection.declarations:
            val = d.value if d.value else "<i>Not Detected</i>"
            conf = f"{d.confidence*100:.0f}%" if d.confidence else "N/A"
            status_style = badge_pass if d.status.value == "DETECTED" else badge_review
            decl_rows.append(
                [
                    Paragraph(d.type.value, body_style),
                    Paragraph(val, body_style),
                    Paragraph(conf, body_style),
                    Paragraph(d.status.value, status_style),
                ]
            )
        decl_table = Table(decl_rows, colWidths=[130, 240, 70, 100])
        decl_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e0f2fe")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ]
            )
        )
        story.append(decl_table)
        story.append(Spacer(1, 12))

        # 4. Potential Findings & Inspector Review
        story.append(Paragraph("3. Potential Findings & Inspector Verifications", h2_style))
        if not inspection.violations:
            story.append(Paragraph("No potential violations or review flags detected for this packaging.", body_style))
        else:
            v_headers = [
                Paragraph("<b>Rule Reference</b>", body_style),
                Paragraph("<b>Description & Action</b>", body_style),
                Paragraph("<b>Severity</b>", body_style),
                Paragraph("<b>Inspector Status</b>", body_style),
            ]
            v_rows = [v_headers]
            for v in inspection.violations:
                rule_code = v.rule.rule_code if v.rule else "LM-RULE"
                review_status = v.status.value
                reviews_text = ""
                if v.reviews:
                    latest = v.reviews[-1]
                    reviews_text = f"<br/><b>Review Remarks:</b> {latest.remarks or 'None'}"
                
                v_rows.append(
                    [
                        Paragraph(rule_code, body_style),
                        Paragraph(f"{v.description}{reviews_text}", body_style),
                        Paragraph(v.severity.value, badge_review),
                        Paragraph(review_status, body_style),
                    ]
                )
            v_table = Table(v_rows, colWidths=[90, 270, 70, 110])
            v_table.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#fee2e2")),
                        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
                        ("TOPPADDING", (0, 0), (-1, -1), 5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                    ]
                )
            )
            story.append(v_table)

        story.append(Spacer(1, 15))

        # Disclaimer Block
        disclaimer_text = (
            "<b>Disclaimer:</b> This document is an AI-assisted inspection report produced to assist "
            "authorized Legal Metrology inspectors. The compliance score and potential violations represent "
            "computational detections and do not constitute automatic penal action without verification by "
            "a designated metrology officer under the Legal Metrology Act, 2009."
        )
        disclaimer_table = Table([[Paragraph(disclaimer_text, subtitle_style)]], colWidths=[540])
        disclaimer_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
                    ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
                    ("TOPPADDING", (0, 0), (-1, -1), 6),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ]
            )
        )
        story.append(disclaimer_table)

        # Build PDF
        doc.build(story)

        # Record Report in Database
        report_record = Report(
            inspection_id=inspection.id,
            report_number=report_num,
            storage_url=f"/reports/{pdf_filename}",
            generated_by=user_id,
            generated_at=datetime.now(timezone.utc),
        )
        db.add(report_record)
        db.commit()
        db.refresh(report_record)

        return report_record


report_service = ReportService()
