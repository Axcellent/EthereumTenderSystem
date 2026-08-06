from api import TxReceipt, BlockchainService

from pydantic import BaseModel, Field, field_validator, ValidationError

from models.common import uint,\
                        text,\
                        string,\
                        unix_time,\
                        addr

from math import ceil
from models.common import TenderStatus

import datetime

CREATE_TENDER = 'createTender'
CLOSE_TENDER = 'closeTender'
REVERT_TENDER = 'revertTender'
GET_TENDER = 'tenders'
GET_TENDER = 'tenders'
GET_TENDERS = 'getTenders'
GET_USERS_TENDERS = 'getUsersTenders'

class CreateTenderDAO(BaseModel):
    title: string
    description: string
    budget: uint
    deadline: unix_time
    bidding_deadline: unix_time
    parent_id: int
    
    @field_validator("deadline", "bidding_deadline", mode="before")
    def validate_deadline(cls, value: datetime.datetime):
        if not isinstance(value, datetime.datetime):
            raise ValidationError("Not datetime type")
        try:
            new_value: unix_time = int(ceil(value.timestamp()))
            return new_value
        except:
            raise ValidationError("Cannot convert to UNIX timestamp")

class TenderGetFullDTO(BaseModel):
    creator: addr
    title: string
    description: string
    budget: uint
    deadline: datetime.datetime
    bidding_deadline: datetime.datetime
    status: TenderStatus
    parent_id: int

    
    
    @field_validator("deadline", "bidding_deadline", mode="before")
    def validate_deadline(cls, value: unix_time):
        try:
            new_value: datetime.datetime = datetime.datetime.fromtimestamp(value)
            return new_value
        except:
            raise ValidationError("Cannot convert from UNIX timestamp to Date-Time")

class TenderGetShortDTO(BaseModel):
    creator: addr
    title: string
    budget: uint
    deadline: datetime.datetime
    
    @field_validator("deadline", mode="before")
    def validate_deadline(cls, value: unix_time):
        try:
            new_value: datetime.datetime = datetime.datetime.fromtimestamp(value)
            return new_value
        except:
            raise ValidationError("Cannot convert from UNIX timestamp to Date-Time")


class TendersManager():
    def create_tender(
        service: BlockchainService,
        address_from: addr,
        key: str,
        tender_data: CreateTenderDAO
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = CREATE_TENDER,
            args = tender_data.model_dump().values(),
        )

    def revert_tender(
        service: BlockchainService,
        address_from: addr,
        key: str,
        tender_id: int
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = REVERT_TENDER,
            args = tender_id,            
        )

    def close_tender(
        service: BlockchainService,
        address_from: addr,
        key: str,
        tender_id: int
    ) -> bool:
        return service.send_tx(
            address_from,
            key,
            function_name = CLOSE_TENDER,
            args = tender_id,            
        )
    

    def get_tender_full(
        service: BlockchainService,
        tender_id: int
    ) -> TenderGetFullDTO:
        data = service.view(GET_TENDER, tender_id)

        return TenderGetFullDTO(
            creator=data[0],
            title=data[1],
            description=data[2],
            budget=data[3],
            deadline=data[4],
            bidding_deadline=data[5],
            parent_id=data[7],
            status=data[6]
        )

    def get_tenders_short(
        service: BlockchainService,
        page: int,
        count: int
    ) -> list[TenderGetShortDTO]:
        data = service.view(GET_TENDERS, page, count)

        return [TenderGetShortDTO(
            creator=d[0],
            title=d[1],
            budget=d[3],
            deadline=d[4],
        ) for d in data]

    def get_user_tenders(
        service: BlockchainService,
        user: addr
    ) -> list[TenderGetShortDTO]:
        data = service.view(GET_USERS_TENDERS, user)

        return [TenderGetShortDTO(
            creator=d[0],
            title=d[1],
            budget=d[3],
            deadline=d[4],
        ) for d in data]