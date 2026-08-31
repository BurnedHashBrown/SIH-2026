from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.utils.constants import DeclarationType, ValidationType, RuleSeverity


class RuleBase(BaseModel):
    rule_code: str
    name: str
    description: Optional[str] = None
    category: str = "General"
    declaration_type: DeclarationType
    validation_type: ValidationType = ValidationType.PRESENCE
    severity: RuleSeverity = RuleSeverity.HIGH
    version: str = "1.0"
    is_active: bool = True
    effective_from: Optional[datetime] = None
    effective_to: Optional[datetime] = None


class RuleCreate(RuleBase):
    pass


class RuleResponse(RuleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

