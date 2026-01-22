from typing import Optional
from pydantic import BaseModel, Field


class AddressUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    building: Optional[str] = Field(None, max_length=255)
    area: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=100)
    postal_code: Optional[str] = Field(None, min_length=5, max_length=10)
    country: Optional[str] = Field(None, max_length=100)

    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
