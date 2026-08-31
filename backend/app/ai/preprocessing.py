import os
import cv2
import numpy as np
from typing import Tuple, List, Optional
from app.schemas.image import ImageQualityResult


class ImagePreprocessor:
    """
    OpenCV-based Image Quality Assessment & Preprocessing Engine.
    Preserves original evidence image at all times.
    """

    def assess_quality(self, image_path: Optional[str] = None, image_bytes: Optional[bytes] = None) -> ImageQualityResult:
        """
        Calculates image quality metrics using OpenCV:
        - Resolution sufficiency
        - Blur level via Laplacian variance
        - Brightness & contrast
        Returns a score (0 to 100) and actionable inspector warnings.
        """
        img = None
        if image_bytes is not None:
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        elif image_path and os.path.exists(image_path):
            img = cv2.imread(image_path)

        if img is None:
            return ImageQualityResult(
                quality_score=0.0,
                is_acceptable=False,
                warnings=["Unable to decode image data for quality analysis."],
            )

        h, w = img.shape[:2]
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        warnings: List[str] = []

        # 1. Resolution Check
        min_dim = min(h, w)
        res_score = min(100.0, (min_dim / 800.0) * 100.0)
        if min_dim < 400:
            warnings.append("Low image resolution. Text detection accuracy may be degraded.")

        # 2. Blur Detection (Laplacian Variance)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        # Normal range: >100 is generally sharp; <40 is blurry
        blur_score = min(100.0, (laplacian_var / 150.0) * 100.0)
        if laplacian_var < 50.0:
            warnings.append("Image appears blurry or out-of-focus.")

        # 3. Brightness Assessment (Mean intensity)
        mean_brightness = float(np.mean(gray))
        # Ideal range: 70 - 200
        if mean_brightness < 50:
            brightness_score = (mean_brightness / 50.0) * 70.0
            warnings.append("Image is underexposed/dark. Declarations might be obscured.")
        elif mean_brightness > 225:
            brightness_score = max(30.0, 100.0 - ((mean_brightness - 225) * 2.0))
            warnings.append("Image is overexposed/glare detected.")
        else:
            brightness_score = 100.0

        # 4. Contrast Assessment (Standard deviation of intensity)
        std_contrast = float(np.std(gray))
        # Ideal range: > 35
        contrast_score = min(100.0, (std_contrast / 50.0) * 100.0)
        if std_contrast < 25:
            warnings.append("Low contrast between text and packaging background.")

        # Aggregate weighted score
        overall_score = (
            0.25 * res_score +
            0.35 * blur_score +
            0.20 * brightness_score +
            0.20 * contrast_score
        )
        overall_score = round(max(0.0, min(100.0, overall_score)), 1)
        is_acceptable = overall_score >= 45.0

        return ImageQualityResult(
            quality_score=overall_score,
            is_acceptable=is_acceptable,
            warnings=warnings,
            blur_score=round(blur_score, 1),
            brightness_score=round(brightness_score, 1),
            contrast_score=round(contrast_score, 1),
        )

    def preprocess_for_ocr(self, img_input: np.ndarray | str) -> np.ndarray:
        """
        Produces an enhanced image copy for OCR text recognition.
        Does NOT alter or overwrite the pristine original image.
        """
        if isinstance(img_input, str):
            img = cv2.imread(img_input)
            if img is None:
                raise ValueError(f"Could not load image from {img_input}")
        else:
            img = img_input.copy()

        h, w = img.shape[:2]

        # 1. Resize if image is too small for character recognition
        if max(h, w) < 1000:
            scale = 1000.0 / max(h, w)
            img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_CUBIC)

        # 2. Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 3. CLAHE Contrast Enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # 4. Denoise with Bilateral Filter (preserves text edges)
        denoised = cv2.bilateralFilter(enhanced, d=7, sigmaColor=50, sigmaSpace=50)

        # 5. Sharpening kernel
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        sharpened = cv2.filter2D(denoised, -1, kernel)

        return sharpened


image_preprocessor = ImagePreprocessor()
