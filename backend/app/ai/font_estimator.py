from typing import Dict, Any, Optional


class FontSizeEstimator:
    """
    Provides estimated character height measurements.
    Labeled explicitly as 'Estimated / AI-Assisted Measurement'.
    """

    def estimate_font_size(
        self,
        bbox_height_px: float,
        image_height_px: int,
        estimated_package_height_mm: float = 200.0,
        required_min_height_mm: float = 2.0,
    ) -> Dict[str, Any]:
        """
        Estimates character height in millimeters based on relative pixel height.
        """
        if image_height_px <= 0 or bbox_height_px <= 0:
            return {
                "estimated_size_mm": None,
                "required_size_mm": required_min_height_mm,
                "label": "Estimated / AI-Assisted Measurement",
                "status": "REVIEW",
                "note": "Insufficient bounding box dimensions to estimate physical font size.",
            }

        # Estimate mm per pixel ratio based on typical packaging framing
        scale_ratio = estimated_package_height_mm / float(image_height_px)
        estimated_mm = round(bbox_height_px * scale_ratio, 2)

        # Standard margin check
        status = "PASS" if estimated_mm >= required_min_height_mm else "REVIEW"

        return {
            "estimated_size_mm": estimated_mm,
            "required_size_mm": required_min_height_mm,
            "label": "Estimated / AI-Assisted Measurement",
            "status": status,
            "note": "Calibration required for binding physical verification.",
        }


font_size_estimator = FontSizeEstimator()
