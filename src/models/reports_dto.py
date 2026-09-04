from pydantic import BaseModel

from models.common import (uid,
                           text,
                           addr,
                           DocStatus)

class ReportGetDTO(BaseModel):
    contract_id: uid
    reporter: addr
    description: text
    status: DocStatus

class ReportCreateDTO(BaseModel):
    tender_id: uid
    description: text
    response: bool