from pydantic import BaseModel, field_validator, ValidationError

from models.common import (uid,
                           unix_time,
                           addr)
import datetime


class BidGetDTO(BaseModel):
    bid_id: uid
    tender_id: uid
    bidder: addr
    price: uid
    deadline: datetime.datetime
    is_active: bool

    @field_validator("deadline", mode="before")
    def validate_deadline(cls, value: unix_time):
        try:
            new_value: datetime.datetime = datetime.datetime.fromtimestamp(value)
            return new_value
        except:
            raise ValueError("Cannot convert from UNIX timestamp to Date-Time")

class BidCreateDTO(BaseModel):
    tender_id: uid    
    price: uid
    deadline: unix_time

    @field_validator("deadline", mode="before")
    def validate_deadline(cls, value: datetime.datetime):
        if not isinstance(value, datetime.datetime):
            raise ValueError("Can receive only datetime.datetime")
        try:
            v: unix_time = int(value.timestamp())
            return v
        except:
            raise ValueError("Cannot convert from Date-Time timestamp to UNIX")
