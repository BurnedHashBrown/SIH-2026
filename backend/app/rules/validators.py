import re
from typing import Tuple, Optional
from app.utils.constants import RuleResult, ValidationType


class DeclarationValidator:
    """
    Validates individual extracted declaration values against Legal Metrology Rules.
    """

    @staticmethod
    def validate_presence(value: Optional[str], confidence: float) -> Tuple[RuleResult, str]:
        if not value or value.strip() == "":
            return RuleResult.REVIEW, "Required declaration was not confidently detected on the packaging."
        if confidence < 0.60:
            return RuleResult.REVIEW, f"Declaration detected with low confidence ({confidence*100:.0f}%). Visual confirmation recommended."
        return RuleResult.PASS, "Declaration present and legible."

    @staticmethod
    def validate_net_quantity(value: Optional[str], confidence: float) -> Tuple[RuleResult, str]:
        if not value:
            return RuleResult.REVIEW, "Net quantity declaration not found on package."
        
        # Valid unit list according to Legal Metrology Rules (g, kg, ml, l, N, pieces)
        valid_units = re.compile(r"^[0-9]+(?:\.[0-9]+)?\s*(?:g|gm|gms|grams?|kg|kilograms?|ml|milliliters?|l|liters?|ltr|pieces|piece|pcs|units?|N)$", re.IGNORECASE)
        if not valid_units.match(value.strip()):
            return RuleResult.REVIEW, f"Net quantity '{value}' contains non-standard unit notation. Inspector review required."
        
        if confidence < 0.65:
            return RuleResult.REVIEW, f"Net quantity text detected with low confidence ({confidence*100:.0f}%)."

        return RuleResult.PASS, f"Valid standard net quantity: {value}"

    @staticmethod
    def validate_mrp(value: Optional[str], confidence: float) -> Tuple[RuleResult, str]:
        if not value:
            return RuleResult.REVIEW, "Maximum Retail Price (MRP) declaration not found."
        
        # Check if numeric price exists
        has_number = any(ch.isdigit() for ch in value)
        if not has_number:
            return RuleResult.REVIEW, f"MRP text '{value}' is missing a valid numeric price."

        if confidence < 0.65:
            return RuleResult.REVIEW, f"MRP detected with marginal confidence ({confidence*100:.0f}%)."

        return RuleResult.PASS, f"Valid MRP declaration: {value}"

    @staticmethod
    def validate_date(value: Optional[str], confidence: float) -> Tuple[RuleResult, str]:
        if not value:
            return RuleResult.REVIEW, "Date of manufacture or pre-packing declaration not found."
        
        if confidence < 0.60:
            return RuleResult.REVIEW, f"Date information detected with low confidence ({confidence*100:.0f}%)."

        return RuleResult.PASS, f"Date declaration present: {value}"

    @staticmethod
    def validate_contact(value: Optional[str], confidence: float) -> Tuple[RuleResult, str]:
        if not value:
            return RuleResult.REVIEW, "Consumer care details (phone/email/address) not found on packaging."

        if confidence < 0.60:
            return RuleResult.REVIEW, "Consumer care information detected with low confidence. Manual check required."

        return RuleResult.PASS, f"Consumer care contact detected: {value}"


declaration_validator = DeclarationValidator()
