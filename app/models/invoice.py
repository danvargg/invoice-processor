from pydantic import BaseModel
from typing import Optional

class Invoice(BaseModel):
    date: Optional[str]           = None
    supplier: Optional[str]       = None
    total: float                  = 0.0
    federal_tax: Optional[float]  = None
    provincial_tax: Optional[float] = None