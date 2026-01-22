from datetime import datetime
from pydantic import BaseModel
from app.schemas.address_base import AddressBase


class AddressRead(AddressBase):
    id: str
    created_at: datetime
    updated_at: datetime
