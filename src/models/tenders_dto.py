from pydantic import BaseModel, field_validator, ValidationError

from models.common import (uint,
                           string,
                           unix_time,
                           addr,
                           TenderStatus)

from math import ceil

import datetime
class CreateTenderDTO(BaseModel):
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

