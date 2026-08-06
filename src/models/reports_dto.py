from pydantic import BaseModel, Field, field_validator, ValidationError
from models.common import *
import datetime

from pydantic import BaseModel, Field, field_validator, ValidationError

from models.common import uint,\
                        text,\
                        string,\
                        unix_time,\
                        addr,\
                        TenderStatus


class ReportGetDTO(BaseModel):
    contract_id: uint
    description: text
    status: DocStatus

class ReportCreateDTO(BaseModel):
    tenderId: uint
    description: text
    response: bool