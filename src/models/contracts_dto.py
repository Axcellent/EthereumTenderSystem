from pydantic import BaseModel, field_validator, ValidationError

from models.common import (uid,
                           unix_time,
                           addr,
                           ContractStatus)
import datetime

class AcceptingModeDTO(BaseModel):
    tender_id: uid
    acceptance: bool
    strict: bool

class ContractGetShortDTO(BaseModel):
    contract_id: uid
    status: ContractStatus

class ContractGetFullDTO(BaseModel):
    contract_id: uid
    tender_id: uid

    contractor: addr
    owner: addr

    amount: uid

    started: datetime.datetime
    deadline: datetime.datetime
    last_report_id: int

    status: ContractStatus

    @field_validator("started", "deadline", mode="before")
    def validate_deadline(cls, value: unix_time):
        try:
            new_value: datetime.datetime = datetime.datetime.fromtimestamp(value)
            return new_value
        except:
            raise ValidationError("Cannot convert from UNIX timestamp to Date-Time")