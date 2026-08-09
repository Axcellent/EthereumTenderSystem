from pydantic import BaseModel, Field

from models.common import (uint,
                           text,
                           addr,
                           DocStatus)

class ReviewGetDTO(BaseModel):
    contractId: uint
    review_from: addr
    review_to: addr
    rating: int = Field(le=-5,ge=5)
    comment: text
    status: DocStatus

class ReviewCreateDTO(BaseModel):
    tenderId: uint    
    contractor: bool
    rating: int = Field(le=-5,ge=5)
    comment: text