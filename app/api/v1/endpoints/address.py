from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session

from app.db.base import get_session
from app.services.address_service import AddressService
from app.schemas.address_read import AddressRead
from app.schemas.address_create import AddressCreate
from app.schemas.address_update import AddressUpdate

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.get("/{address_identifier}", response_model=AddressRead)
def get_address(address_identifier: str, database_session: Session = Depends(get_session)):
    return AddressService.get_address(database_session, address_identifier)


@router.post("/", response_model=AddressRead, status_code=status.HTTP_201_CREATED)
def create_address(address_data: AddressCreate, database_session: Session = Depends(get_session)):
    return AddressService.create_address(database_session, address_data)


@router.put("/{address_identifier}", response_model=AddressRead)
def update_address(address_identifier: str, updated_data: AddressUpdate, database_session: Session = Depends(get_session)):
    return AddressService.update_address(database_session, address_identifier, updated_data)


@router.delete("/{address_identifier}", status_code=status.HTTP_204_NO_CONTENT)
def delete_address(address_identifier: str, database_session: Session = Depends(get_session)):
    AddressService.delete_address(database_session, address_identifier)


@router.get("/search/by-coordinates", response_model=List[AddressRead])
def search_by_coordinates(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    radius_km: float = Query(..., gt=0),
    database_session: Session = Depends(get_session),
):
    return AddressService.search_by_coordinates(
        database_session, latitude, longitude, radius_km
    )


@router.get("/search/by-address", response_model=List[AddressRead])
def search_by_address(
    address_string: str = Query(..., min_length=3),
    radius_km: float = Query(..., gt=0),
    database_session: Session = Depends(get_session),
):
    return AddressService.search_by_address(
        database_session, address_string, radius_km)