from pydantic import BaseModel, Field

from models.common import (uid,
                           text,
                           addr,
                           DocStatus)

class ReviewGetDTO(BaseModel):
    contractId: uid
    review_from: addr
    review_to: addr
    rating: int = Field(le=-5,ge=5)
    comment: text
    status: DocStatus

class ReviewCreateDTO(BaseModel):
    tender_id: uid    
    contractor: bool
    rating: int = Field(le=-5,ge=5)
    comment: text