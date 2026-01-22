from typing import List, Optional
from sqlmodel import Session, select

from app.models.address_model import AddressModel
from app.schemas.address_create import AddressCreate
from app.schemas.address_update import AddressUpdate

class AddressRepository:
    """
    Repository layer responsible for database operations on AddressModel.
    """

    @staticmethod
    def create(database_session: Session, address_data: AddressCreate) -> AddressModel:
        """Create a new address record."""
        new_address = AddressModel(**address_data.model_dump())
        database_session.add(new_address)
        database_session.commit()
        database_session.refresh(new_address)
        return new_address

    @staticmethod
    def get_by_id(database_session: Session, address_identifier: str) -> Optional[AddressModel]:
        """Retrieve an address by its unique identifier."""
        return database_session.get(AddressModel, address_identifier)

    @staticmethod
    def get_all(database_session: Session) -> List[AddressModel]:
        """Retrieve all addresses."""
        query_statement = select(AddressModel)
        return database_session.exec(query_statement).all()

    @staticmethod
    def update(database_session: Session, address_identifier: str, updated_data: AddressUpdate) -> Optional[AddressModel]:
        """Update an existing address record."""
        existing_address = database_session.get(AddressModel, address_identifier)
        if not existing_address:
            return None

        update_fields = updated_data.model_dump(exclude_unset=True)
        for field_name, field_value in update_fields.items():
            setattr(existing_address, field_name, field_value)

        database_session.add(existing_address)
        database_session.commit()
        database_session.refresh(existing_address)
        return existing_address

    @staticmethod
    def delete(database_session: Session, address_identifier: str) -> bool:
        """Delete an address record by its unique identifier."""
        address_to_delete = database_session.get(AddressModel, address_identifier)
        if not address_to_delete:
            return False

        database_session.delete(address_to_delete)
        database_session.commit()
        return True

    @staticmethod
    def get_within_bounds(
        database_session: Session,
        minimum_latitude: float,
        maximum_latitude: float,
        minimum_longitude: float,
        maximum_longitude: float
    ) -> List[AddressModel]:
        """Get addresses within latitude and longitude bounds."""
        query_statement = select(AddressModel).where(
            AddressModel.latitude.between(minimum_latitude, maximum_latitude),
            AddressModel.longitude.between(minimum_longitude, maximum_longitude)
        )
        return database_session.exec(query_statement).all()
