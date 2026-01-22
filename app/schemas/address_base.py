from typing import Optional
from pydantic import BaseModel, Field


class AddressBase(BaseModel):
    name: str = Field(..., max_length=100)
    building: str = Field(..., max_length=255)
    area: str = Field(..., max_length=255)
    city: str = Field(..., max_length=100)
    postal_code: str = Field(..., min_length=5, max_length=10)
    country: str = Field(..., max_length=100)

    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
