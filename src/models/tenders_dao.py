from pydantic import BaseModel, Field, field_validator, ValidationError
from models.common import *
import datetime


class TenderGet(BaseModel):
    creator: addr
    title: string
    description: text
    budget: uint
    deadline: datetime.datetime
    biddingDeadline: datetime.datetime
    status: TenderStatus
    parentTenderId: uint

    @classmethod
    @field_validator(deadline, mode="before")
    def validate_deadline(cls, value_from_chain):
        try:
            return datetime.datetime.fromtimestamp(value_from_chain, tz=datetime.timezone.utc)
        except:
            raise ValidationError("Deadline is not correct")

    @classmethod
    @field_validator(biddingDeadline, mode="before")
    def validate_bidding_deadline(cls, value_from_chain):
        try:
            return datetime.datetime.fromtimestamp(value_from_chain, tz=datetime.timezone.utc)
        except:
            raise ValidationError("Bidding deadline is not correct")

    @classmethod
    @field_validator(creator, mode="before")
    def validate_creator(cls, value_from_chain):
        try:
            return int(value_from_chain, 16)
        except:
            raise ValidationError("Address is not correct")

class TenderCreate(BaseModel):
    title: string
    description: text
    budget: uint
    deadline: datetime.datetime
    biddingDeadline: datetime.datetime
    parentTenderId: uint

    @classmethod
    @field_validator(deadline, mode="before")
    def validate_deadline(cls, value_from_chain):
        try:
            return datetime.datetime.fromtimestamp(value_from_chain, tz=datetime.timezone.utc)
        except:
            raise ValidationError("Deadline is not correct")

    @classmethod
    @field_validator(biddingDeadline, mode="before")
    def validate_bidding_deadline(cls, value_from_chain):
        try:
            return datetime.datetime.fromtimestamp(value_from_chain, tz=datetime.timezone.utc)
        except:
            raise ValidationError("Bidding deadline is not correct")