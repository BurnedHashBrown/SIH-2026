import pytest
from app.models.rule import Rule
from app.ai.declaration_extractor import ExtractedDeclaration
from app.rules.engine import compliance_rule_engine
from app.services.scoring_service import scoring_service
from app.utils.constants import (
    DeclarationType,
    DeclarationStatus,
    ValidationType,
    RuleSeverity,
    RuleResult,
    InspectionStatus,
)


@pytest.fixture
def core_rules():
    return [
        Rule(
            id=1,
            rule_code="LM-001",
            name="Product Name",
            declaration_type=DeclarationType.PRODUCT_NAME,
            validation_type=ValidationType.PRESENCE,
            severity=RuleSeverity.HIGH,
            is_active=True,
        ),
        Rule(
            id=2,
            rule_code="LM-002",
            name="Net Quantity",
            declaration_type=DeclarationType.NET_QUANTITY,
            validation_type=ValidationType.UNIT,
            severity=RuleSeverity.CRITICAL,
            is_active=True,
        ),
        Rule(
            id=3,
            rule_code="LM-003",
            name="MRP",
            declaration_type=DeclarationType.MRP,
            validation_type=ValidationType.FORMAT,
            severity=RuleSeverity.CRITICAL,
            is_active=True,
        ),
        Rule(
            id=4,
            rule_code="LM-004",
            name="Date Information",
            declaration_type=DeclarationType.DATE_INFORMATION,
            validation_type=ValidationType.DATE,
            severity=RuleSeverity.HIGH,
            is_active=True,
        ),
        Rule(
            id=5,
            rule_code="LM-005",
            name="Manufacturer",
            declaration_type=DeclarationType.MANUFACTURER,
            validation_type=ValidationType.PRESENCE,
            severity=RuleSeverity.HIGH,
            is_active=True,
        ),
        Rule(
            id=6,
            rule_code="LM-006",
            name="Consumer Care",
            declaration_type=DeclarationType.CONSUMER_CARE,
            validation_type=ValidationType.CONTACT,
            severity=RuleSeverity.HIGH,
            is_active=True,
        ),
    ]


def test_compliance_engine_all_pass(core_rules):
    compliant_decls = [
        ExtractedDeclaration(DeclarationType.PRODUCT_NAME, "Premium Wheat Flour", 0.98, DeclarationStatus.DETECTED),
        ExtractedDeclaration(DeclarationType.NET_QUANTITY, "5 kg", 0.97, DeclarationStatus.DETECTED),
        ExtractedDeclaration(DeclarationType.MRP, "₹275", 0.96, DeclarationStatus.DETECTED),
        ExtractedDeclaration(DeclarationType.DATE_INFORMATION, "MFD: 07/2026", 0.95, DeclarationStatus.DETECTED),
        ExtractedDeclaration(DeclarationType.MANUFACTURER, "Golden Mills Ltd, Punjab", 0.94, DeclarationStatus.DETECTED),
        ExtractedDeclaration(DeclarationType.CONSUMER_CARE, "care@goldenmills.com, 1800-200-300", 0.95, DeclarationStatus.DETECTED),
    ]

    findings = compliance_rule_engine.evaluate_declarations(core_rules, compliant_decls)
    assert len(findings) == 6
    assert all(f.result == RuleResult.PASS for f in findings)

    score, status, summary = scoring_service.calculate_score(findings)
    assert score == 100.0
    assert status == InspectionStatus.COMPLIANT
    assert summary["passed"] == 6
    assert summary["violations"] == 0


def test_compliance_engine_missing_consumer_care(core_rules):
    decls = [
        ExtractedDeclaration(DeclarationType.PRODUCT_NAME, "ABC Premium Biscuits", 0.98, DeclarationStatus.DETECTED),
        ExtractedDeclaration(DeclarationType.NET_QUANTITY, "500 g", 0.97, DeclarationStatus.DETECTED),
        ExtractedDeclaration(DeclarationType.MRP, "₹199", 0.96, DeclarationStatus.DETECTED),
        ExtractedDeclaration(DeclarationType.DATE_INFORMATION, "MFD: 06/2026", 0.95, DeclarationStatus.DETECTED),
        ExtractedDeclaration(DeclarationType.MANUFACTURER, "ABC Foods Pvt. Ltd.", 0.94, DeclarationStatus.DETECTED),
        ExtractedDeclaration(DeclarationType.CONSUMER_CARE, None, 0.0, DeclarationStatus.MISSING),
    ]

    findings = compliance_rule_engine.evaluate_declarations(core_rules, decls)
    score, status, summary = scoring_service.calculate_score(findings)

    assert score == 83.3  # 5 out of 6 passed
    assert status == InspectionStatus.REQUIRES_REVIEW
    assert summary["passed"] == 5
    assert summary["review"] == 1

    care_finding = next((f for f in findings if f.declaration_type == "CONSUMER_CARE"), None)
    assert care_finding is not None
    assert care_finding.result == RuleResult.REVIEW
    assert "not found" in care_finding.reason.lower() or "not confidently detected" in care_finding.reason.lower()
