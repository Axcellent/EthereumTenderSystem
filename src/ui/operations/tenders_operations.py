from ui.operations import (BlockchainOperation,
                                BlockchainUser,
                                BlockchainService)

from models.common import (uint,
                           addr,
                           pkey)

from services.tenders import *

class CreateTenderOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        tender_data: TenderCreateDTO
    ):
        super().__init__(service, user)
        self.tender_data = tender_data

    def execute(self) -> TxReceipt:
        return TendersService.create_tender(
            self.service,
            self.address,
            self.key,
            self.tender_data
        )

class CloseTenderOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        tender_id: uint
    ):
        super().__init__(service, user)
        self.tender_id = tender_id

    def execute(self) -> bool:        
        return TendersService.close_tender(
            self.service,
            self.address,
            self.key,
            self.tender_id
        )

class RevertTenderOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        tender_id: uint
    ):
        super().__init__(service, user)
        self.tender_id = tender_id

    def execute(self) -> TxReceipt:
        return TendersService.revert_tender(
            self.service,
            self.address,
            self.key,
            self.tender_id
        )

class LoadTendersOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        page: uint,
        count: uint
    ):     
        print('LoadTendersOperation __init__')   
        super().__init__(service, user)
        self.page = page
        self.count = count

    def execute(self) -> TxReceipt:
        print('LoadTendersOperation execute')   
        return TendersService.get_tenders_short(
            self.service,
            self.page,
            self.count
        )

class LoadUserTendersOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        address: addr
    ):        
        super().__init__(service, user)
        self.other_address = address

    def execute(self) -> TxReceipt:
        return TendersService.get_user_tenders(
            self.service,
            self.other_address            
        )

class LoadFullTenderOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        tender: uint
    ):        
        print("LoadFullTenderOperation")
        super().__init__(service, user)
        self.tender = tender

    def execute(self) -> TxReceipt:
        print("execute")
        return TendersService.get_tender_full(
            self.service,
            self.tender            
        )