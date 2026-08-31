import random
from datetime import datetime, timezone
from typing import TypeVar, List, Dict, Any, Generic
from pydantic import BaseModel

T = TypeVar("T")


def generate_inspection_id() -> str:
    """Generate official inspection ID such as LM-2026-0248."""
    year = datetime.now(timezone.utc).year
    rand_num = random.randint(100, 9999)
    return f"LM-{year}-{rand_num:04d}"


def generate_report_number() -> str:
    """Generate official report ID such as REP-2026-0248."""
    year = datetime.now(timezone.utc).year
    rand_num = random.randint(100, 9999)
    return f"REP-{year}-{rand_num:04d}"


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    page: int
    limit: int
    total: int
    total_pages: int
