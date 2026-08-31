import os
import sys
from datetime import datetime, timezone
from sqlalchemy.orm import Session

# Ensure app is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.config import settings
from app.database.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.product import Product
from app.models.inspection import Inspection
from app.models.rule import Rule
from app.models.declaration import Declaration
from app.models.violation import Violation
from app.utils.security import get_password_hash
from app.utils.constants import (
    UserRole,
    InspectionStatus,
    DeclarationType,
    DeclarationStatus,
    ValidationType,
    RuleSeverity,
    ViolationType,
    ViolationStatus,
)


def seed_database():
    """Seeds the database with initial users, rules, and demo data."""
    print("Ensuring tables are created...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # 1. Seed Users
        admin_user = db.query(User).filter(User.email == settings.SEED_ADMIN_EMAIL).first()
        if not admin_user:
            admin_user = User(
                name="Legal Metrology Admin",
                email=settings.SEED_ADMIN_EMAIL,
                employee_id="LM-ADM-001",
                password_hash=get_password_hash(settings.SEED_ADMIN_PASSWORD),
                role=UserRole.ADMIN,
                department="Directorate of Legal Metrology",
                is_active=True,
            )
            db.add(admin_user)
            print(f"Created Admin: {admin_user.email}")

        inspector_user = db.query(User).filter(User.email == settings.SEED_INSPECTOR_EMAIL).first()
        if not inspector_user:
            inspector_user = User(
                name="Sanjay Sharma (Senior Inspector)",
                email=settings.SEED_INSPECTOR_EMAIL,
                employee_id="LM-INS-104",
                password_hash=get_password_hash(settings.SEED_INSPECTOR_PASSWORD),
                role=UserRole.INSPECTOR,
                department="State Legal Metrology Enforcement Wing",
                is_active=True,
            )
            db.add(inspector_user)
            print(f"Created Inspector: {inspector_user.email}")

        db.commit()
        if inspector_user:
            db.refresh(inspector_user)

        # 2. Seed 6 Core Prototype Legal Metrology Rules
        prototype_rules = [
            {
                "rule_code": "LM-001",
                "name": "Generic or Common Name of Commodity",
                "description": "The packaging must clearly bear the common or generic name of the packaged commodity (Rule 6(1)(a) of Legal Metrology Packaged Commodities Rules 2011).",
                "category": "Identity",
                "declaration_type": DeclarationType.PRODUCT_NAME,
                "validation_type": ValidationType.PRESENCE,
                "severity": RuleSeverity.HIGH,
                "version": "1.0",
                "is_active": True,
            },
            {
                "rule_code": "LM-002",
                "name": "Net Quantity and Standard Unit Declaration",
                "description": "The net quantity of the commodity contained in the package must be declared in terms of standard units of weight, measure or number (Rule 6(1)(d)).",
                "category": "Quantity",
                "declaration_type": DeclarationType.NET_QUANTITY,
                "validation_type": ValidationType.UNIT,
                "severity": RuleSeverity.CRITICAL,
                "version": "1.0",
                "is_active": True,
            },
            {
                "rule_code": "LM-003",
                "name": "Maximum Retail Price (MRP) Declaration",
                "description": "Retail sale price of package must be declared as Maximum or Max. Retail Price inclusive of all taxes (Rule 6(1)(e)).",
                "category": "Pricing",
                "declaration_type": DeclarationType.MRP,
                "validation_type": ValidationType.FORMAT,
                "severity": RuleSeverity.CRITICAL,
                "version": "1.0",
                "is_active": True,
            },
            {
                "rule_code": "LM-004",
                "name": "Month and Year of Manufacture or Pre-packing",
                "description": "Month and year of manufacture, packing, or import must be prominently marked (Rule 6(1)(c)).",
                "category": "Date Information",
                "declaration_type": DeclarationType.DATE_INFORMATION,
                "validation_type": ValidationType.DATE,
                "severity": RuleSeverity.HIGH,
                "version": "1.0",
                "is_active": True,
            },
            {
                "rule_code": "LM-005",
                "name": "Name and Address of Manufacturer / Packer / Importer",
                "description": "The name and complete address of the manufacturer or packer or importer must be clearly declared (Rule 6(1)(b)).",
                "category": "Traceability",
                "declaration_type": DeclarationType.MANUFACTURER,
                "validation_type": ValidationType.PRESENCE,
                "severity": RuleSeverity.HIGH,
                "version": "1.0",
                "is_active": True,
            },
            {
                "rule_code": "LM-006",
                "name": "Consumer Care Details and Contact Information",
                "description": "Name, address, telephone number, and email of the consumer care cell or person to be contacted in case of consumer complaints (Rule 6(1)(n)).",
                "category": "Consumer Protection",
                "declaration_type": DeclarationType.CONSUMER_CARE,
                "validation_type": ValidationType.CONTACT,
                "severity": RuleSeverity.HIGH,
                "version": "1.0",
                "is_active": True,
            },
        ]

        for rule_data in prototype_rules:
            existing_rule = db.query(Rule).filter(Rule.rule_code == rule_data["rule_code"]).first()
            if not existing_rule:
                rule_obj = Rule(**rule_data)
                db.add(rule_obj)
                print(f"Created Rule: {rule_data['rule_code']} - {rule_data['name']}")

        db.commit()

        # 3. Seed Demo Product
        demo_product = db.query(Product).filter(Product.product_name == "ABC Premium Biscuits").first()
        if not demo_product:
            demo_product = Product(
                product_name="ABC Premium Biscuits",
                brand="ABC Foods",
                category="Food & Bakery",
                manufacturer="ABC Foods Pvt. Ltd., Industrial Estate, Andheri East, Mumbai 400093",
                packer="ABC Foods Pvt. Ltd.",
                batch_number="B240826",
            )
            db.add(demo_product)
            db.commit()
            db.refresh(demo_product)
            print(f"Created Demo Product: {demo_product.product_name}")

        # 4. Seed Demo Inspection
        demo_inspection = db.query(Inspection).filter(Inspection.inspection_id == "LM-2026-0248").first()
        if not demo_inspection and demo_product and inspector_user:
            demo_inspection = Inspection(
                inspection_id="LM-2026-0248",
                product_id=demo_product.id,
                inspector_id=inspector_user.id,
                location="Crawford Market, Mumbai",
                inspection_date=datetime.now(timezone.utc),
                status=InspectionStatus.REQUIRES_REVIEW,
                compliance_score=83.3,
                total_checks=6,
                passed_checks=5,
                review_count=1,
                violation_count=1,
            )
            db.add(demo_inspection)
            db.commit()
            db.refresh(demo_inspection)

            # Add declarations for demo inspection
            declarations = [
                Declaration(
                    inspection_id=demo_inspection.id,
                    type=DeclarationType.PRODUCT_NAME,
                    value="ABC Premium Biscuits",
                    confidence=0.98,
                    status=DeclarationStatus.DETECTED,
                    bbox_x=100.0,
                    bbox_y=150.0,
                    bbox_width=250.0,
                    bbox_height=50.0,
                ),
                Declaration(
                    inspection_id=demo_inspection.id,
                    type=DeclarationType.MRP,
                    value="₹199",
                    confidence=0.96,
                    status=DeclarationStatus.DETECTED,
                    bbox_x=120.0,
                    bbox_y=240.0,
                    bbox_width=200.0,
                    bbox_height=50.0,
                ),
                Declaration(
                    inspection_id=demo_inspection.id,
                    type=DeclarationType.NET_QUANTITY,
                    value="500 g",
                    confidence=0.97,
                    status=DeclarationStatus.DETECTED,
                    bbox_x=120.0,
                    bbox_y=300.0,
                    bbox_width=180.0,
                    bbox_height=45.0,
                ),
                Declaration(
                    inspection_id=demo_inspection.id,
                    type=DeclarationType.DATE_INFORMATION,
                    value="MFD: 06/2026",
                    confidence=0.95,
                    status=DeclarationStatus.DETECTED,
                    bbox_x=120.0,
                    bbox_y=360.0,
                    bbox_width=220.0,
                    bbox_height=45.0,
                ),
                Declaration(
                    inspection_id=demo_inspection.id,
                    type=DeclarationType.MANUFACTURER,
                    value="ABC Foods Pvt. Ltd., Industrial Estate, Andheri East, Mumbai 400093",
                    confidence=0.94,
                    status=DeclarationStatus.DETECTED,
                    bbox_x=80.0,
                    bbox_y=420.0,
                    bbox_width=320.0,
                    bbox_height=60.0,
                ),
                Declaration(
                    inspection_id=demo_inspection.id,
                    type=DeclarationType.CONSUMER_CARE,
                    value=None,
                    confidence=0.15,
                    status=DeclarationStatus.MISSING,
                ),
            ]
            db.add_all(declarations)
            db.commit()

            # Add potential violation
            consumer_rule = db.query(Rule).filter(Rule.rule_code == "LM-006").first()
            consumer_dec = db.query(Declaration).filter(
                Declaration.inspection_id == demo_inspection.id,
                Declaration.type == DeclarationType.CONSUMER_CARE,
            ).first()

            violation = Violation(
                inspection_id=demo_inspection.id,
                rule_id=consumer_rule.id if consumer_rule else None,
                declaration_id=consumer_dec.id if consumer_dec else None,
                type=ViolationType.MISSING_DECLARATION,
                description="Consumer care information was not confidently detected in the analyzed packaging images. Manual verification required.",
                severity=RuleSeverity.HIGH,
                confidence=0.84,
                status=ViolationStatus.UNDER_REVIEW,
            )
            db.add(violation)
            db.commit()
            print(f"Created Demo Inspection: {demo_inspection.inspection_id} with score {demo_inspection.compliance_score}%")

        print("Database seeding completed successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
