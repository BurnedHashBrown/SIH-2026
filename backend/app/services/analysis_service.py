import logging
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.inspection import Inspection
from app.models.image import InspectionImage
from app.models.ocr_result import OCRResult
from app.models.rule import Rule
from app.schemas.inspection import AnalysisResponse, InspectionSummary
from app.schemas.declaration import DeclarationResponse
from app.schemas.violation import ViolationResponse
from app.schemas.image import BoundingBox
from app.services.inspection_service import inspection_service
from app.services.compliance_service import compliance_service
from app.services.scoring_service import scoring_service
from app.services.storage_service import storage_service
from app.services.audit_service import audit_service
from app.ai.preprocessing import image_preprocessor
from app.ai.ocr import ocr_service, OCRToken
from app.ai.declaration_extractor import declaration_extractor
from app.rules.engine import compliance_rule_engine
from app.utils.constants import AuditAction, InspectionStatus

logger = logging.getLogger("metrology.analysis")


class AnalysisService:
    @staticmethod
    def run_full_analysis(db: Session, inspection_id_or_str: str | int, user_id: int) -> AnalysisResponse:
        """
        Orchestrates end-to-end AI compliance analysis pipeline for an inspection.
        """
        # 1. Get inspection
        inspection = inspection_service.get_inspection_by_id(db, inspection_id_or_str)
        if not inspection:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"code": "INSPECTION_NOT_FOUND", "message": "Inspection not found."},
            )

        # 2. Get images
        images = db.query(InspectionImage).filter(InspectionImage.inspection_id == inspection.id).all()
        if not images:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "NO_IMAGES_UPLOADED",
                    "message": "Please upload at least one packaging image before initiating compliance analysis.",
                },
            )

        # Update inspection status to PROCESSING
        inspection.status = InspectionStatus.PROCESSING
        db.commit()

        tokens_by_image: Dict[int, List[OCRToken]] = {}

        try:
            # 3 & 4 & 5 & 6: Process images & Run OCR
            for img in images:
                file_path = storage_service.get_image_path(img.file_name)
                
                # Check quality / verify file
                quality_res = image_preprocessor.assess_quality(image_path=file_path)
                img.image_quality_score = quality_res.quality_score
                db.commit()

                # OCR Execution
                try:
                    tokens = ocr_service.extract_text(file_path)
                except Exception as ocr_err:
                    logger.error(f"OCR failed for image {img.id}: {ocr_err}")
                    tokens = []

                tokens_by_image[img.id] = tokens

                # Store OCR Results in Database
                db.query(OCRResult).filter(OCRResult.image_id == img.id).delete()
                for tok in tokens:
                    db_tok = OCRResult(
                        image_id=img.id,
                        text=tok.text,
                        confidence=tok.confidence,
                        bbox_x=tok.bbox_x,
                        bbox_y=tok.bbox_y,
                        bbox_width=tok.bbox_width,
                        bbox_height=tok.bbox_height,
                    )
                    db.add(db_tok)
                db.commit()

            # 7 & 8: Extract Declarations & Store in Database
            product_name = inspection.product.product_name if inspection.product else None
            brand_name = inspection.product.brand if inspection.product else None
            category = inspection.product.category if inspection.product else "General"

            extracted_decls = declaration_extractor.extract_declarations(
                tokens_by_image=tokens_by_image,
                expected_product_name=product_name,
                expected_brand=brand_name,
            )
            db_declarations = compliance_service.sync_declarations(db, inspection.id, extracted_decls)

            # 9 & 10: Select applicable rules & Run Compliance Engine
            active_rules = db.query(Rule).filter(Rule.is_active == True).all()
            findings = compliance_rule_engine.evaluate_declarations(
                rules=active_rules,
                declarations=extracted_decls,
                product_category=category,
            )

            # 11: Sync Potential Violations
            db_violations = compliance_service.sync_violations(db, inspection.id, findings, db_declarations)

            # 12 & 13: Calculate Compliance Score and Update Inspection Status
            score, final_status, summary_counts = scoring_service.calculate_score(findings)

            inspection.compliance_score = score
            inspection.status = final_status
            inspection.total_checks = summary_counts["total_checks"]
            inspection.passed_checks = summary_counts["passed"]
            inspection.review_count = summary_counts["review"]
            inspection.violation_count = summary_counts["violations"]
            db.commit()
            db.refresh(inspection)

            # 14. Audit Log & Return
            audit_service.log_event(
                db=db,
                action=AuditAction.ANALYSIS_COMPLETED,
                user_id=user_id,
                entity_type="Inspection",
                entity_id=str(inspection.id),
                metadata={"compliance_score": score, "status": final_status.value},
            )

            return AnalysisResponse(
                inspection_id=inspection.inspection_id,
                compliance_score=score,
                status=final_status,
                summary=InspectionSummary(
                    total_checks=summary_counts["total_checks"],
                    passed=summary_counts["passed"],
                    review=summary_counts["review"],
                    violations=summary_counts["violations"],
                ),
                declarations=[
                    DeclarationResponse(
                        id=d.id,
                        inspection_id=d.inspection_id,
                        type=d.type,
                        value=d.value,
                        confidence=d.confidence,
                        status=d.status,
                        image_id=d.image_id,
                        bbox=BoundingBox(
                            x=d.bbox_x or 0.0,
                            y=d.bbox_y or 0.0,
                            width=d.bbox_width or 0.0,
                            height=d.bbox_height or 0.0,
                        ) if d.bbox_x is not None else None,
                        created_at=d.created_at,
                        updated_at=d.updated_at,
                    )
                    for d in db_declarations
                ],
                violations=[
                    ViolationResponse(
                        id=v.id,
                        inspection_id=v.inspection_id,
                        rule_id=v.rule_id,
                        declaration_id=v.declaration_id,
                        type=v.type,
                        description=v.description,
                        severity=v.severity,
                        confidence=v.confidence,
                        status=v.status,
                        evidence_image_id=v.evidence_image_id,
                        declaration_type=v.declaration.type.value if v.declaration else None,
                        rule_code=v.rule.rule_code if v.rule else None,
                        reviews=[],
                        created_at=v.created_at,
                        updated_at=v.updated_at,
                    )
                    for v in db_violations
                ],
            )

        except Exception as e:
            db.rollback()
            logger.exception(f"Analysis orchestration failed: {e}")
            inspection.status = InspectionStatus.ANALYSIS_COMPLETE
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"code": "ANALYSIS_FAILED", "message": f"Compliance analysis pipeline encountered an error: {str(e)}"},
            )


analysis_service = AnalysisService()
