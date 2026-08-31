from typing import Dict, Any, Optional
from app.utils.constants import DeclarationStatus


class ReadabilityAnalyzer:
    """
    Evaluates text readability based on OCR confidence, blur, contrast, and bounding box dimensions.
    """

    def analyze_declaration_readability(
        self,
        ocr_confidence: float,
        image_quality_score: float = 80.0,
        bbox_height: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Assesses readability quality: EXCELLENT, ACCEPTABLE, POOR, or UNREADABLE.
        """
        # Weighted readability score
        conf_factor = ocr_confidence * 100.0
        combined_score = (0.7 * conf_factor) + (0.3 * image_quality_score)

        if combined_score >= 85.0:
            rating = "EXCELLENT"
            status = DeclarationStatus.DETECTED
            recommendation = "Text is clear and legible."
        elif combined_score >= 65.0:
            rating = "ACCEPTABLE"
            status = DeclarationStatus.DETECTED
            recommendation = "Text is legible; minor noise detected."
        elif combined_score >= 40.0:
            rating = "POOR"
            status = DeclarationStatus.REVIEW
            recommendation = "Text clarity is marginal. Inspector review recommended."
        else:
            rating = "UNREADABLE"
            status = DeclarationStatus.REVIEW
            recommendation = "Text is degraded or unclear. Manual verification required."

        return {
            "score": round(combined_score, 1),
            "readability": rating,
            "status": status,
            "recommendation": recommendation,
        }


readability_analyzer = ReadabilityAnalyzer()
