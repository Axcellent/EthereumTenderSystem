from pydantic import BaseModel, field_validator, ValidationError

from models.common import (uint,
                           unix_time,
                           addr)
import datetime


class BidGetDTO(BaseModel):
    tender_id: uint
    bidder: addr
    price: uint
    deadline: datetime.datetime
    is_active: bool

    @field_validator("deadline", mode="before")
    def validate_deadline(cls, value: unix_time):
        try:
            new_value: datetime.datetime = datetime.datetime.fromtimestamp(value)
            return new_value
        except:
            raise ValidationError("Cannot convert from UNIX timestamp to Date-Time")

class BidCreateDTO(BaseModel):
    tender_id: uint    
    price: uint
    deadline: unix_time

    @field_validator("deadline", mode="before")
    def validate_deadline(cls, value: datetime.datetime):
        if not isinstance(value, datetime.datetime):
            raise ValidationError("Can receive only datetime.datetime")
        try:
            v: unix_time = value.timestamp()
            return v
        except:
            raise ValidationError("Cannot convert from Date-Time timestamp to UNIX")
