import re
from typing import List, Dict, Any, Optional
from app.ai.ocr import OCRToken
from app.utils.constants import DeclarationType, DeclarationStatus
from app.schemas.image import BoundingBox


class ExtractedDeclaration:
    def __init__(
        self,
        decl_type: DeclarationType,
        value: Optional[str],
        confidence: float,
        status: DeclarationStatus,
        image_id: Optional[int] = None,
        bbox: Optional[BoundingBox] = None,
        raw_text: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.type = decl_type
        self.value = value
        self.confidence = confidence
        self.status = status
        self.image_id = image_id
        self.bbox = bbox
        self.raw_text = raw_text
        self.metadata = metadata or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type.value,
            "value": self.value,
            "confidence": round(self.confidence, 4),
            "status": self.status.value,
            "image_id": self.image_id,
            "bbox": self.bbox.model_dump() if self.bbox else None,
            "raw_text": self.raw_text,
            "metadata": self.metadata,
        }


class DeclarationExtractor:
    """
    Deterministic Legal Metrology Declaration Extraction Engine.
    Extracts, normalizes, and validates the 6 core declarations + metadata.
    """

    # --- Regex Patterns ---
    MRP_PATTERN = re.compile(
        r"(?:M\.?\s*R\.?\s*P\.?|MAX(?:IMUM)?\.?\s*RETAIL\s*PRICE|RETAIL\s*PRICE|MRP\s*Rs\.?|₹|Rs\.?)\s*[:\-\.]?\s*([₹Rs\.]*\s*[0-9]+(?:[\.,][0-9]{2})?(?:\s*/-|\s*incl.*)?)",
        re.IGNORECASE,
    )
    MRP_NUMERIC_PATTERN = re.compile(r"([0-9]+(?:\.[0-9]{2})?)")

    NET_QTY_PATTERN = re.compile(
        r"(?:NET\s*(?:QTY|QUANTITY|WT|WEIGHT|CONTENTS)|QUANTITY|NET\s*VOLUME)\s*[:\-\.]?\s*([0-9]+(?:\.[0-9]+)?\s*(?:g|gm|gms|grams?|kg|kilograms?|ml|milliliters?|l|liters?|ltr|pieces|piece|pcs|units?|N))\b",
        re.IGNORECASE,
    )
    STANDALONE_QTY_PATTERN = re.compile(
        r"\b([0-9]+(?:\.[0-9]+)?\s*(?:g|gm|kg|ml|l|L|pieces|pcs|N))\b",
        re.IGNORECASE,
    )

    DATE_PATTERN = re.compile(
        r"(?:MFD|PKD|MFG|PACKED|MANUFACTURED|DATE\s*OF\s*MFG|DATE\s*OF\s*PKD|USE\s*BY|BEST\s*BEFORE|EXPIRY|EXP)\s*[:\-\.]?\s*([0-9]{1,2}[\/\-\.][0-9]{2,4}|[A-Za-z]{3}[\/\-\.\s]+[0-9]{2,4})",
        re.IGNORECASE,
    )

    MFG_BY_PATTERN = re.compile(
        r"(?:MANUFACTURED\s*BY|MFD\s*BY|PRODUCED\s*BY|MANUFACTURED\s*AND\s*PACKED\s*BY)\s*[:\-\.]?\s*(.+)",
        re.IGNORECASE,
    )
    PACKED_BY_PATTERN = re.compile(
        r"(?:PACKED\s*BY|PKD\s*BY|PRE\-?PACKED\s*BY)\s*[:\-\.]?\s*(.+)",
        re.IGNORECASE,
    )
    IMPORTED_BY_PATTERN = re.compile(
        r"(?:IMPORTED\s*BY|IMP\s*BY)\s*[:\-\.]?\s*(.+)",
        re.IGNORECASE,
    )

    CONSUMER_CARE_KEYWORDS = [
        "consumer care",
        "customer care",
        "customer service",
        "consumer cell",
        "toll free",
        "contact us",
        "feedback",
        "helpline",
        "grievance",
    ]
    EMAIL_PATTERN = re.compile(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)")
    PHONE_PATTERN = re.compile(r"(?:1800|1860|0?[0-9]{2,4})[\-\s]?[0-9]{6,10}")

    ORIGIN_PATTERN = re.compile(
        r"(?:COUNTRY\s*OF\s*ORIGIN|MADE\s*IN)\s*[:\-\.]?\s*([A-Za-z\s]+)",
        re.IGNORECASE,
    )

    def extract_declarations(
        self,
        tokens_by_image: Dict[int, List[OCRToken]],
        expected_product_name: Optional[str] = None,
        expected_brand: Optional[str] = None,
    ) -> List[ExtractedDeclaration]:
        """
        Runs extraction across all image tokens and produces structured declarations.
        """
        extracted_map: Dict[DeclarationType, ExtractedDeclaration] = {}

        # Aggregate all tokens for sequential analysis
        for image_id, tokens in tokens_by_image.items():
            for i, token in enumerate(tokens):
                text = token.text.strip()
                if not text:
                    continue

                bbox = BoundingBox(
                    x=token.bbox_x,
                    y=token.bbox_y,
                    width=token.bbox_width,
                    height=token.bbox_height,
                )

                # 1. Product Name Detection
                if DeclarationType.PRODUCT_NAME not in extracted_map:
                    if expected_product_name and expected_product_name.lower() in text.lower():
                        extracted_map[DeclarationType.PRODUCT_NAME] = ExtractedDeclaration(
                            decl_type=DeclarationType.PRODUCT_NAME,
                            value=expected_product_name,
                            confidence=token.confidence,
                            status=DeclarationStatus.DETECTED,
                            image_id=image_id,
                            bbox=bbox,
                            raw_text=text,
                        )
                    elif expected_brand and expected_brand.lower() in text.lower():
                        extracted_map[DeclarationType.PRODUCT_NAME] = ExtractedDeclaration(
                            decl_type=DeclarationType.PRODUCT_NAME,
                            value=text,
                            confidence=token.confidence,
                            status=DeclarationStatus.DETECTED,
                            image_id=image_id,
                            bbox=bbox,
                            raw_text=text,
                        )

                # 2. MRP Extraction
                if DeclarationType.MRP not in extracted_map:
                    mrp_match = self.MRP_PATTERN.search(text)
                    if mrp_match:
                        raw_val = mrp_match.group(1).strip()
                        # Normalize to ₹ format
                        num_match = self.MRP_NUMERIC_PATTERN.search(raw_val)
                        norm_val = f"₹{num_match.group(1)}" if num_match else raw_val
                        extracted_map[DeclarationType.MRP] = ExtractedDeclaration(
                            decl_type=DeclarationType.MRP,
                            value=norm_val,
                            confidence=token.confidence,
                            status=DeclarationStatus.DETECTED,
                            image_id=image_id,
                            bbox=bbox,
                            raw_text=text,
                        )

                # 3. Net Quantity Extraction
                if DeclarationType.NET_QUANTITY not in extracted_map:
                    qty_match = self.NET_QTY_PATTERN.search(text)
                    if qty_match:
                        extracted_map[DeclarationType.NET_QUANTITY] = ExtractedDeclaration(
                            decl_type=DeclarationType.NET_QUANTITY,
                            value=qty_match.group(1).strip(),
                            confidence=token.confidence,
                            status=DeclarationStatus.DETECTED,
                            image_id=image_id,
                            bbox=bbox,
                            raw_text=text,
                        )
                    else:
                        standalone_match = self.STANDALONE_QTY_PATTERN.search(text)
                        if standalone_match and not any(kw in text.lower() for kw in ["mrp", "rs", "₹"]):
                            extracted_map[DeclarationType.NET_QUANTITY] = ExtractedDeclaration(
                                decl_type=DeclarationType.NET_QUANTITY,
                                value=standalone_match.group(1).strip(),
                                confidence=token.confidence * 0.9,
                                status=DeclarationStatus.DETECTED,
                                image_id=image_id,
                                bbox=bbox,
                                raw_text=text,
                            )

                # 4. Date Information
                if DeclarationType.DATE_INFORMATION not in extracted_map:
                    date_match = self.DATE_PATTERN.search(text)
                    if date_match:
                        extracted_map[DeclarationType.DATE_INFORMATION] = ExtractedDeclaration(
                            decl_type=DeclarationType.DATE_INFORMATION,
                            value=f"MFD: {date_match.group(1).strip()}",
                            confidence=token.confidence,
                            status=DeclarationStatus.DETECTED,
                            image_id=image_id,
                            bbox=bbox,
                            raw_text=text,
                        )

                # 5. Manufacturer / Packer / Importer
                if DeclarationType.MANUFACTURER not in extracted_map:
                    mfg_match = self.MFG_BY_PATTERN.search(text)
                    if mfg_match:
                        extracted_map[DeclarationType.MANUFACTURER] = ExtractedDeclaration(
                            decl_type=DeclarationType.MANUFACTURER,
                            value=mfg_match.group(1).strip(),
                            confidence=token.confidence,
                            status=DeclarationStatus.DETECTED,
                            image_id=image_id,
                            bbox=bbox,
                            raw_text=text,
                        )

                if DeclarationType.PACKER not in extracted_map:
                    packed_match = self.PACKED_BY_PATTERN.search(text)
                    if packed_match:
                        extracted_map[DeclarationType.PACKER] = ExtractedDeclaration(
                            decl_type=DeclarationType.PACKER,
                            value=packed_match.group(1).strip(),
                            confidence=token.confidence,
                            status=DeclarationStatus.DETECTED,
                            image_id=image_id,
                            bbox=bbox,
                            raw_text=text,
                        )

                # 6. Consumer Care Information
                if DeclarationType.CONSUMER_CARE not in extracted_map:
                    text_lower = text.lower()
                    has_kw = any(kw in text_lower for kw in self.CONSUMER_CARE_KEYWORDS)
                    email_match = self.EMAIL_PATTERN.search(text)
                    phone_match = self.PHONE_PATTERN.search(text)

                    if has_kw or email_match or phone_match:
                        details = []
                        if email_match:
                            details.append(email_match.group(1))
                        if phone_match:
                            details.append(phone_match.group(0))
                        val_str = text if not details else f"{text} ({', '.join(details)})"

                        extracted_map[DeclarationType.CONSUMER_CARE] = ExtractedDeclaration(
                            decl_type=DeclarationType.CONSUMER_CARE,
                            value=val_str,
                            confidence=token.confidence,
                            status=DeclarationStatus.DETECTED,
                            image_id=image_id,
                            bbox=bbox,
                            raw_text=text,
                        )

                # 7. Country of Origin
                if DeclarationType.COUNTRY_OF_ORIGIN not in extracted_map:
                    origin_match = self.ORIGIN_PATTERN.search(text)
                    if origin_match:
                        extracted_map[DeclarationType.COUNTRY_OF_ORIGIN] = ExtractedDeclaration(
                            decl_type=DeclarationType.COUNTRY_OF_ORIGIN,
                            value=origin_match.group(1).strip(),
                            confidence=token.confidence,
                            status=DeclarationStatus.DETECTED,
                            image_id=image_id,
                            bbox=bbox,
                            raw_text=text,
                        )

        # Fallback heuristic: If Product Name was not detected via OCR, but expected_product_name was supplied, or first token
        if DeclarationType.PRODUCT_NAME not in extracted_map:
            if expected_product_name:
                extracted_map[DeclarationType.PRODUCT_NAME] = ExtractedDeclaration(
                    decl_type=DeclarationType.PRODUCT_NAME,
                    value=expected_product_name,
                    confidence=0.5,
                    status=DeclarationStatus.REVIEW,
                )
            else:
                extracted_map[DeclarationType.PRODUCT_NAME] = ExtractedDeclaration(
                    decl_type=DeclarationType.PRODUCT_NAME,
                    value=None,
                    confidence=0.0,
                    status=DeclarationStatus.MISSING,
                )

        # Ensure all 6 primary declarations exist in the returned list
        primary_types = [
            DeclarationType.PRODUCT_NAME,
            DeclarationType.NET_QUANTITY,
            DeclarationType.MRP,
            DeclarationType.DATE_INFORMATION,
            DeclarationType.MANUFACTURER,
            DeclarationType.CONSUMER_CARE,
        ]

        for dtype in primary_types:
            if dtype not in extracted_map:
                extracted_map[dtype] = ExtractedDeclaration(
                    decl_type=dtype,
                    value=None,
                    confidence=0.0,
                    status=DeclarationStatus.MISSING,
                )

        return list(extracted_map.values())


declaration_extractor = DeclarationExtractor()
