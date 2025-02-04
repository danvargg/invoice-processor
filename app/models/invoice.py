from typing import Optional

from pydantic import BaseModel


class Invoice(BaseModel):  # TODO: add category, desc
    date: Optional[str] = None
    supplier: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    total: float = 0.0
    federal_tax: Optional[float] = None
    provincial_tax: Optional[float] = None
