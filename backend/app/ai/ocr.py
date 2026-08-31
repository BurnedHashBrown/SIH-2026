import os
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import numpy as np

from app.config import settings

logger = logging.getLogger("metrology.ocr")


@dataclass
class OCRToken:
    text: str
    confidence: float
    bbox_x: float
    bbox_y: float
    bbox_width: float
    bbox_height: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "confidence": round(self.confidence, 4),
            "bbox": [self.bbox_x, self.bbox_y, self.bbox_width, self.bbox_height],
        }


class BaseOCREngine(ABC):
    @abstractmethod
    def extract_text(self, image_path: str) -> List[OCRToken]:
        """Extract text tokens with confidence and bounding boxes from image."""
        pass


class PaddleOCREngine(BaseOCREngine):
    """
    Production PaddleOCR engine implementation.
    """
    def __init__(self):
        self._ocr = None
        self._initialized = False

    def _initialize(self):
        if not self._initialized:
            try:
                from paddleocr import PaddleOCR
                # Initialize PaddleOCR (English/Hindi multilingual model)
                self._ocr = PaddleOCR(use_angle_cls=True, lang="en", show_log=False)
                self._initialized = True
                logger.info("PaddleOCR engine successfully initialized.")
            except Exception as e:
                logger.warning(f"Failed to initialize native PaddleOCR: {e}. Fallback may be used.")
                self._ocr = None

    def extract_text(self, image_path: str) -> List[OCRToken]:
        self._initialize()
        if not self._ocr:
            raise RuntimeError("PaddleOCR is not available in current environment.")

        results = self._ocr.ocr(image_path, cls=True)
        tokens: List[OCRToken] = []

        if not results or not results[0]:
            return tokens

        for line in results[0]:
            coords = line[0]  # [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            text, conf = line[1]

            xs = [pt[0] for pt in coords]
            ys = [pt[1] for pt in coords]
            min_x, max_x = min(xs), max(xs)
            min_y, max_y = min(ys), max(ys)

            tokens.append(
                OCRToken(
                    text=text.strip(),
                    confidence=float(conf),
                    bbox_x=round(float(min_x), 1),
                    bbox_y=round(float(min_y), 1),
                    bbox_width=round(float(max_x - min_x), 1),
                    bbox_height=round(float(max_y - min_y), 1),
                )
            )

        return tokens


class MockOCREngine(BaseOCREngine):
    """
    Deterministic Mock OCR engine for testing, CI pipelines, and dev setups.
    Returns standard Legal Metrology sample tokens.
    """
    def extract_text(self, image_path: str) -> List[OCRToken]:
        logger.info(f"Using MockOCREngine for image {image_path}")
        return [
            OCRToken("ABC Premium Biscuits", 0.98, 100.0, 150.0, 250.0, 50.0),
            OCRToken("M.R.P. ₹199 (Incl. of all taxes)", 0.96, 120.0, 240.0, 300.0, 45.0),
            OCRToken("Net Qty: 500 g", 0.97, 120.0, 300.0, 180.0, 40.0),
            OCRToken("MFD: 06/2026", 0.95, 120.0, 360.0, 160.0, 40.0),
            OCRToken("Manufactured by: ABC Foods Pvt. Ltd., Mumbai 400093", 0.94, 80.0, 420.0, 450.0, 55.0),
            OCRToken("Batch No: B240826", 0.92, 120.0, 490.0, 180.0, 35.0),
        ]


def get_ocr_engine() -> BaseOCREngine:
    """Factory function for retrieving the configured OCR engine."""
    if settings.OCR_ENGINE.lower() == "paddleocr":
        try:
            import paddleocr  # noqa
            return PaddleOCREngine()
        except ImportError:
            if settings.USE_MOCK_OCR_IF_UNAVAILABLE:
                logger.warning("PaddleOCR not installed; falling back to MockOCREngine.")
                return MockOCREngine()
            raise RuntimeError("PaddleOCR requested but not installed.")
    return MockOCREngine()


ocr_service = get_ocr_engine()
