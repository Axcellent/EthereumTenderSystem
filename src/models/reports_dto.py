from pydantic import BaseModel

from models.common import (uint,
                           text,
                           DocStatus)

class ReportGetDTO(BaseModel):
    contract_id: uint
    description: text
    status: DocStatus

class ReportCreateDTO(BaseModel):
    tender_id: uint
    description: text
    response: bool