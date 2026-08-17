from pydantic import BaseModel

from models.common import (uint,
                           text,
                           addr,
                           DocStatus)

class ReportGetDTO(BaseModel):
    contract_id: uint
    reporter: addr
    description: text
    status: DocStatus

class ReportCreateDTO(BaseModel):
    tender_id: uint
    description: text
    response: bool