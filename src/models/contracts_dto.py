from pydantic import BaseModel, Field, field_validator, ValidationError

from models.common import uint,\
                        text,\
                        string,\
                        unix_time,\
                        addr,\
                        ContractStatus
import datetime

class AcceptingModeDTO(BaseModel):
    tender_id: uint
    acceptance: bool
    strict: bool

class ContractGetShortDTO(BaseModel):
    contract_id: uint
    status: ContractStatus

class ContractGetFullDTO(BaseModel):
    contract_id: uint
    tenderId: uint

    contractor: addr
    owner: addr

    amount: uint

    started: datetime.datetime
    deadline: datetime.datetime
    last_report_id: uint

    status: ContractStatus

    @field_validator("started", "deadline", mode="before")
    def validate_deadline(cls, value: unix_time):
        try:
            new_value: datetime.datetime = datetime.datetime.fromtimestamp(value)
            return new_value
        except:
            raise ValidationError("Cannot convert from UNIX timestamp to Date-Time")