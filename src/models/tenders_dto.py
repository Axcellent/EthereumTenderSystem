from pydantic import BaseModel, field_validator

from models.common import (uid,
                           string,
                           text,
                           unix_time,
                           addr,
                           TenderStatus)

from math import ceil

import datetime
class TenderCreateDTO(BaseModel):
    title: string
    description: text
    budget: uid
    deadline: unix_time
    bidding_deadline: unix_time
    parent_id: int
    
    @field_validator("deadline", "bidding_deadline", mode="before")
    def validate_deadline(cls, value: datetime.datetime):
        if not isinstance(value, datetime.datetime):
            raise ValueError("Not datetime type")
        try:
            new_value: unix_time = int(ceil(value.timestamp()))
            return new_value
        except:
            raise ValueError("Cannot convert to UNIX timestamp")

class TenderGetFullDTO(BaseModel):
    creator: addr
    title: string
    description: text
    budget: uid
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
            raise ValueError("Cannot convert from UNIX timestamp to Date-Time")

class TenderGetShortDTO(BaseModel):
    tender_id: uid
    creator: addr
    title: string
    budget: uid
    deadline: datetime.datetime
    
    @field_validator("deadline", mode="before")
    def validate_deadline(cls, value: unix_time):
        try:
            new_value: datetime.datetime = datetime.datetime.fromtimestamp(value)
            return new_value
        except:
            raise ValueError("Cannot convert from UNIX timestamp to Date-Time")

