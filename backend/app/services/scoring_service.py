from typing import List, Dict, Any, Tuple
from app.rules.engine import ComplianceFinding
from app.utils.constants import RuleResult, InspectionStatus


class ScoringService:
    @staticmethod
    def calculate_score(findings: List[ComplianceFinding]) -> Tuple[float, InspectionStatus, Dict[str, int]]:
        total_checks = len(findings)
        if total_checks == 0:
            return 0.0, InspectionStatus.REQUIRES_REVIEW, {"total": 0, "passed": 0, "review": 0, "violations": 0}

        passed_count = sum(1 for f in findings if f.result == RuleResult.PASS)
        review_count = sum(1 for f in findings if f.result == RuleResult.REVIEW)
        fail_count = sum(1 for f in findings if f.result == RuleResult.FAIL)

        score = round((passed_count / float(total_checks)) * 100.0, 1)

        # Determine preliminary AI inspection status
        if score == 100.0:
            status = InspectionStatus.COMPLIANT
        elif score >= 70.0:
            status = InspectionStatus.REQUIRES_REVIEW
        else:
            status = InspectionStatus.POTENTIAL_NON_COMPLIANCE

        summary = {
            "total_checks": total_checks,
            "passed": passed_count,
            "review": review_count,
            "violations": review_count + fail_count,
        }

        return score, status, summary


scoring_service = ScoringService()
