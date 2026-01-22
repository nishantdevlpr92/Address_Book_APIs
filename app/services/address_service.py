from datetime import datetime
from math import cos, radians
from typing import List, Tuple

from sqlmodel import Session

from app.models.address_model import AddressModel
from app.repositories.address_repository import AddressRepository
from app.services.location_service import LocationService
from app.schemas.address_create import AddressCreate
from app.schemas.address_update import AddressUpdate

class AddressService:
    """
    Service layer responsible for address-related business logic.
    """

    @staticmethod
    def create_address(database_session: Session, address_data: AddressCreate) -> AddressModel:
        """
        Create and persist a new address record.
        """
        if address_data.latitude is None or address_data.longitude is None:
            full_address_string = f"{address_data.building}, {address_data.area}, {address_data.city}, {address_data.country}"
            geocoded_coords = LocationService.geocode_address(full_address_string)
            if geocoded_coords is None:
                raise ValueError("Unable to geocode address")
            address_data.latitude = geocoded_coords[0]
            address_data.longitude = geocoded_coords[1]

        return AddressRepository.create(database_session, address_data)

    @staticmethod
    def get_address(database_session: Session, address_identifier: str) -> AddressModel:
        """
        Retrieve a single address by its unique identifier.
        """
        found_address = AddressRepository.get_by_id(database_session, address_identifier)
        if not found_address:
            raise ValueError("Address not found")
        return found_address

    @staticmethod
    def update_address(
        database_session: Session,
        address_identifier: str,
        updated_data: AddressUpdate,
    ) -> AddressModel:
        """
        Update an existing address record.
        """
        existing_address = AddressRepository.get_by_id(database_session, address_identifier)
        if not existing_address:
            raise ValueError("Address not found")

        update_fields = updated_data.model_dump(exclude_unset=True)
        for field_name, field_value in update_fields.items():
            setattr(existing_address, field_name, field_value)

        if existing_address.latitude is None or existing_address.longitude is None:
            full_address_string = f"{existing_address.building}, {existing_address.area}, {existing_address.city}, {existing_address.country}"
            geocoded_coords = LocationService.geocode_address(full_address_string)
            if geocoded_coords is not None:
                existing_address.latitude = geocoded_coords[0]
                existing_address.longitude = geocoded_coords[1]

        existing_address.updated_at = datetime.utcnow()
        return AddressRepository.update(database_session, address_identifier, updated_data)

    @staticmethod
    def delete_address(database_session: Session, address_identifier: str) -> None:
        """
        Delete an address record by its unique identifier.
        """
        if not AddressRepository.delete(database_session, address_identifier):
            raise ValueError("Address not found")

    @staticmethod
    def get_addresses_within_radius(
        database_session: Session,
        center_latitude: float,
        center_longitude: float,
        search_radius_km: float,
    ) -> List[AddressModel]:
        """
        Retrieve all addresses within a specified radius from a given location.
        """
        if search_radius_km <= 0:
            raise ValueError("Radius must be greater than zero")

        latitude_delta = search_radius_km / 111 *1.1
        longitude_delta = search_radius_km / (111 * cos(radians(center_latitude))) * 1.1

        nearby_addresses = AddressRepository.get_within_bounds(
            database_session,
            center_latitude - latitude_delta,
            center_latitude + latitude_delta,
            center_longitude - longitude_delta,
            center_longitude + longitude_delta
        )

        filtered_results = [
            address_record for address_record in nearby_addresses
            if LocationService.calculate_distance(
                center_latitude, center_longitude, 
                address_record.latitude, address_record.longitude
            ) <= search_radius_km
        ]
        return filtered_results
    
    @staticmethod
    def search_by_coordinates(
        database_session: Session,
        latitude: float,
        longitude: float,
        radius_km: float
    ) -> List[AddressModel]:
        if radius_km <= 0:
            raise ValueError("Radius must be greater than zero")

        return AddressService.get_addresses_within_radius(
            database_session, latitude, longitude, radius_km
        )

    @staticmethod
    def search_by_address(
        database_session: Session,
        address_string: str,
        radius_km: float
    ) -> List[AddressModel]:
        if not address_string:
            raise ValueError("Address string must be provided")

        geocoded_coords = LocationService.geocode_address(address_string)
        if geocoded_coords is None:
            raise ValueError("Unable to geocode provided address")

        latitude, longitude = geocoded_coords

        return AddressService.get_addresses_within_radius(
            database_session, latitude, longitude, radius_km
        )