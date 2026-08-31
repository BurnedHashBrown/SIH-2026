from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from app.models.inspection import Inspection
from app.models.declaration import Declaration
from app.models.violation import Violation
from app.models.rule import Rule
from app.ai.declaration_extractor import ExtractedDeclaration
from app.rules.engine import ComplianceFinding
from app.utils.constants import (
    RuleResult,
    ViolationType,
    ViolationStatus,
    DeclarationStatus,
)


class ComplianceService:
    @staticmethod
    def sync_declarations(
        db: Session,
        inspection_id: int,
        extracted_decls: List[ExtractedDeclaration],
    ) -> List[Declaration]:
        """Save/update declarations in database for this inspection."""
        # Clear previous AI-extracted declarations if any
        db.query(Declaration).filter(Declaration.inspection_id == inspection_id).delete()

        db_decls: List[Declaration] = []
        for decl in extracted_decls:
            db_decl = Declaration(
                inspection_id=inspection_id,
                image_id=decl.image_id,
                type=decl.type,
                value=decl.value,
                confidence=decl.confidence,
                status=decl.status,
                bbox_x=decl.bbox.x if decl.bbox else None,
                bbox_y=decl.bbox.y if decl.bbox else None,
                bbox_width=decl.bbox.width if decl.bbox else None,
                bbox_height=decl.bbox.height if decl.bbox else None,
            )
            db.add(db_decl)
            db_decls.append(db_decl)

        db.commit()
        for d in db_decls:
            db.refresh(d)
        return db_decls

    @staticmethod
    def sync_violations(
        db: Session,
        inspection_id: int,
        findings: List[ComplianceFinding],
        db_declarations: List[Declaration],
    ) -> List[Violation]:
        """Save potential violations generated from failed/review findings."""
        # Clear previous AI-generated violations that haven't been reviewed
        db.query(Violation).filter(
            Violation.inspection_id == inspection_id,
            Violation.status == ViolationStatus.AI_DETECTED,
        ).delete()

        decl_lookup = {d.type.value: d for d in db_declarations}
        db_violations: List[Violation] = []

        for f in findings:
            if f.result in [RuleResult.REVIEW, RuleResult.FAIL]:
                linked_decl = decl_lookup.get(f.declaration_type)
                
                v_type = ViolationType.MISSING_DECLARATION
                if linked_decl and linked_decl.value:
                    v_type = ViolationType.FORMAT

                violation = Violation(
                    inspection_id=inspection_id,
                    rule_id=f.rule.id,
                    declaration_id=linked_decl.id if linked_decl else None,
                    type=v_type,
                    description=f"{f.finding}: {f.reason} (Recommended Action: {f.recommended_action})",
                    severity=f.rule.severity,
                    confidence=f.confidence,
                    status=ViolationStatus.UNDER_REVIEW,
                    evidence_image_id=f.evidence_image_id,
                )
                db.add(violation)
                db_violations.append(violation)

        db.commit()
        for v in db_violations:
            db.refresh(v)
        return db_violations


compliance_service = ComplianceService()
