from typing import Optional
from pydantic import BaseModel, Field
from datetime import date

class CultureSchema(BaseModel):
    name: str = Field(..., min_length=1)
    old_name: Optional[str] = Field(None, min_length=1)

class ResumedCultureSchema(BaseModel):
    id: int

class CropSchema(BaseModel):
    date: date
    culture: ResumedCultureSchema

class FarmSchema(BaseModel):
    name: str = Field(..., min_length=1)
    arable_area: float
    vegetation_area: float
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)

class FarmerSchema(BaseModel):
    document: str = Field(..., pattern=r"^\d{11}|\d{14}$")
    name: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
