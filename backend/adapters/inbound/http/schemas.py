from enum import Enum
from pydantic import BaseModel, Field
from datetime import date

class CultureSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name must be between 1 and 255 characters")

class ResumedCultureSchema(BaseModel):
    id: int

class CropSchema(BaseModel):
    date: date
    culture: ResumedCultureSchema

class BrazilianState(str, Enum):
    AC = "AC"
    AL = "AL"
    AP = "AP"
    AM = "AM"
    BA = "BA"
    CE = "CE"
    DF = "DF"
    ES = "ES"
    GO = "GO"
    MA = "MA"
    MT = "MT"
    MS = "MS"
    MG = "MG"
    PA = "PA"
    PB = "PB"
    PR = "PR"
    PE = "PE"
    PI = "PI"
    RJ = "RJ"
    RN = "RN"
    RS = "RS"
    RO = "RO"
    RR = "RR"
    SC = "SC"
    SP = "SP"
    SE = "SE"
    TO = "TO"

class FarmSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Name must be between 1 and 255 characters")
    arable_area: float = Field(..., gt=0, description="Arable area must be greater than 0")
    vegetation_area: float = Field(..., gt=0, description="Vegetation area must be greater than 0")
    city: str = Field(..., min_length=1, max_length=255, description="City must be between 1 and 255 characters")
    state: BrazilianState

class FarmerSchema(BaseModel):
    document: str = Field(..., pattern=r"^\d{11}|\d{14}$")
    name: str = Field(..., min_length=1)
    city: str = Field(..., min_length=1)
    state: str = Field(..., min_length=1)
