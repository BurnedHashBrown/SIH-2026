from typing import List, Dict, Any, Optional
from app.models.rule import Rule
from app.models.declaration import Declaration
from app.ai.declaration_extractor import ExtractedDeclaration
from app.rules.validators import declaration_validator
from app.utils.constants import (
    RuleResult,
    ValidationType,
    ViolationType,
    ViolationStatus,
    RuleSeverity,
    DeclarationStatus,
)


class ComplianceFinding:
    def __init__(
        self,
        rule: Rule,
        declaration_type: str,
        result: RuleResult,
        finding: str,
        reason: str,
        confidence: float,
        evidence_image_id: Optional[int] = None,
        declaration_id: Optional[int] = None,
        recommended_action: str = "Manual verification required.",
    ):
        self.rule = rule
        self.declaration_type = declaration_type
        self.result = result
        self.finding = finding
        self.reason = reason
        self.confidence = confidence
        self.evidence_image_id = evidence_image_id
        self.declaration_id = declaration_id
        self.recommended_action = recommended_action


class ComplianceRuleEngine:
    """
    Evaluates Legal Metrology rules against extracted declarations.
    Produces explainable compliance findings and potential violations.
    """

    def evaluate_declarations(
        self,
        rules: List[Rule],
        declarations: List[ExtractedDeclaration],
        product_category: Optional[str] = "General",
    ) -> List[ComplianceFinding]:
        decl_map = {d.type: d for d in declarations}
        findings: List[ComplianceFinding] = []

        for rule in rules:
            if not rule.is_active:
                continue

            decl = decl_map.get(rule.declaration_type)
            val = decl.value if decl else None
            conf = decl.confidence if decl else 0.0
            image_id = decl.image_id if decl else None

            # Execute appropriate validator
            if rule.validation_type == ValidationType.UNIT:
                res, reason = declaration_validator.validate_net_quantity(val, conf)
            elif rule.validation_type == ValidationType.FORMAT:
                res, reason = declaration_validator.validate_mrp(val, conf)
            elif rule.validation_type == ValidationType.DATE:
                res, reason = declaration_validator.validate_date(val, conf)
            elif rule.validation_type == ValidationType.CONTACT:
                res, reason = declaration_validator.validate_contact(val, conf)
            else:
                res, reason = declaration_validator.validate_presence(val, conf)

            # Build explainable finding
            finding_name = rule.name
            confidence_score = conf if conf > 0 else 0.84  # 84% baseline confidence for missing declaration check

            if res == RuleResult.PASS:
                action = "Declaration verified compliant by AI check."
            elif res == RuleResult.REVIEW:
                action = "Manual verification required by authorized inspector."
            else:
                action = "Inspector inspection recommended for potential non-compliance."

            finding = ComplianceFinding(
                rule=rule,
                declaration_type=rule.declaration_type.value,
                result=res,
                finding=finding_name,
                reason=reason,
                confidence=confidence_score,
                evidence_image_id=image_id,
                recommended_action=action,
            )
            findings.append(finding)

        return findings


compliance_rule_engine = ComplianceRuleEngine()
