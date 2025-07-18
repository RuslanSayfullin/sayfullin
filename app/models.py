from pydantic import BaseModel, Field

class Machine(BaseModel):
    """Модель станка"""
    id: int = Field(..., gt=0)
    model: str = Field(..., min_length=2, max_length=30)
    serial_number: int = Field(..., gt=0)
    owner: str = Field(..., min_length=1, max_length=500)
    constructor: str = Field(..., min_length=1, max_length=500)
    programmer: str = Field(..., min_length=1, max_length=500)
    engineer: str = Field(..., min_length=1, max_length=500)
    description: str | None = None