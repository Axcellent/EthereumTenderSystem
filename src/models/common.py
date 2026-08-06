from pydantic import Field
from enum import IntEnum
from typing import Annotated

pkey = Annotated[str, Field(pattern=r'^0x[a-fA-F0-9]{64}$')]
addr = Annotated[str, Field(pattern=r'^0x[a-fA-F0-9]{40}$')]

uint = Annotated[int, Field(gt=0)]
unix_time = Annotated[int, Field(gt=0)]
string = Annotated[str, Field(min_length=3,max_length=128)]
text = Annotated[str, Field(min_length=0,max_length=4096)]

class TenderStatus(IntEnum):
    Opened = 0
    Closed = 1
    Processed = 2
    Executing = 3
    Completed = 4
    Denied = 5

    @property
    def display_name(self) -> str:
        return self.name

class DocStatus(IntEnum):
    Pending = 0
    Accepted = 1
    Rejected = 2

    @property
    def display_name(self) -> str:
        return self.name

class ContractStatus(IntEnum):
    Pending = 0
    Executing = 1
    Finished = 2
    Completed = 3
    Judging = 4
    Failed = 5

    @property
    def display_name(self) -> str:
        return self.name
