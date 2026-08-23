from services import BlockchainService
from models.common import (addr,
                           pkey)

from abc import ABC, abstractmethod

class BlockchainUser():
    def __init__(
        self, 
        address: addr, 
        key: pkey
    ):
        self.address = address
        self.key = key

    address: addr
    key: pkey

class BlockchainOperation(ABC):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser 
    ):
        self.service = service
        self.address = user.address
        self.key = user.key

    @abstractmethod
    def execute(self):
        pass