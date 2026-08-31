import pytest
from app.ai.ocr import OCRToken, MockOCREngine
from app.ai.declaration_extractor import declaration_extractor
from app.ai.readability import readability_analyzer
from app.ai.font_estimator import font_size_estimator
from app.utils.constants import DeclarationType, DeclarationStatus


def test_mock_ocr_returns_tokens_with_bboxes():
    engine = MockOCREngine()
    tokens = engine.extract_text("dummy_path.jpg")
    assert len(tokens) >= 5
    for t in tokens:
        assert isinstance(t.text, str)
        assert t.confidence > 0.8
        assert t.bbox_width > 0
        assert t.bbox_height > 0
        dict_rep = t.to_dict()
        assert "bbox" in dict_rep
        assert len(dict_rep["bbox"]) == 4


def test_declaration_extraction_mrp():
    tokens = [
        OCRToken("M.R.P. ₹249.00 (Inclusive of all taxes)", 0.95, 100, 200, 300, 40),
    ]
    decls = declaration_extractor.extract_declarations({1: tokens})
    mrp_decl = next((d for d in decls if d.type == DeclarationType.MRP), None)
    assert mrp_decl is not None
    assert mrp_decl.status == DeclarationStatus.DETECTED
    assert "₹249" in mrp_decl.value
    assert mrp_decl.bbox is not None


def test_declaration_extraction_net_quantity():
    tokens = [
        OCRToken("Net Quantity: 1 kg", 0.96, 100, 250, 200, 40),
    ]
    decls = declaration_extractor.extract_declarations({1: tokens})
    qty_decl = next((d for d in decls if d.type == DeclarationType.NET_QUANTITY), None)
    assert qty_decl is not None
    assert qty_decl.status == DeclarationStatus.DETECTED
    assert "1 kg" in qty_decl.value


def test_declaration_extraction_date_and_manufacturer():
    tokens = [
        OCRToken("MFD: 08/2026", 0.94, 100, 300, 180, 40),
        OCRToken("Manufactured by: Sunshine Bakers Pvt. Ltd., Okhla, New Delhi", 0.93, 100, 350, 400, 50),
    ]
    decls = declaration_extractor.extract_declarations({1: tokens})
    date_decl = next((d for d in decls if d.type == DeclarationType.DATE_INFORMATION), None)
    mfg_decl = next((d for d in decls if d.type == DeclarationType.MANUFACTURER), None)

    assert date_decl is not None and "08/2026" in date_decl.value
    assert mfg_decl is not None and "Sunshine Bakers" in mfg_decl.value


def test_declaration_extraction_consumer_care():
    tokens = [
        OCRToken("Consumer Care: feedback@sunshinefoods.com or Call 1800-11-2233", 0.95, 100, 400, 450, 45),
    ]
    decls = declaration_extractor.extract_declarations({1: tokens})
    care_decl = next((d for d in decls if d.type == DeclarationType.CONSUMER_CARE), None)
    assert care_decl is not None
    assert care_decl.status == DeclarationStatus.DETECTED
    assert "1800-11-2233" in care_decl.value or "feedback@sunshinefoods.com" in care_decl.value


def test_readability_analyzer():
    res_high = readability_analyzer.analyze_declaration_readability(ocr_confidence=0.95, image_quality_score=90.0)
    assert res_high["readability"] == "EXCELLENT"

    res_low = readability_analyzer.analyze_declaration_readability(ocr_confidence=0.35, image_quality_score=40.0)
    assert res_low["readability"] in ["POOR", "UNREADABLE"]
    assert res_low["status"] == DeclarationStatus.REVIEW


def test_font_size_estimator():
    result = font_size_estimator.estimate_font_size(
        bbox_height_px=40.0,
        image_height_px=1000,
        estimated_package_height_mm=200.0,
        required_min_height_mm=2.0,
    )
    assert result["label"] == "Estimated / AI-Assisted Measurement"
    assert result["estimated_size_mm"] == 8.0
    assert result["status"] == "PASS"
