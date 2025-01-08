from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date

class CultureSchema(BaseModel):
    name: str


class CropSchema(BaseModel):
    date: date
    culture: CultureSchema


class FarmSchema(BaseModel):
    name: str
    arable_area: float
    vegetation_area: float
    total_area: float
    crops: List[CropSchema]


class FarmerSchema(BaseModel):
    document: str = Field(..., regex=r"^\d{11}$")
    name: str
    city: str
    state: str
    farms: List[FarmSchema]
