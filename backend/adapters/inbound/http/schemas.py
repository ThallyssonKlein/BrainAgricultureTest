from typing import List
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
    city: str
    state: str

class FarmerSchema(BaseModel):
    document: str = Field(..., pattern=r"^\d{11}|\d{14}$")
    name: str
    city: str
    state: str