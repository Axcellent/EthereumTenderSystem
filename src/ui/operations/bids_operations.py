from ui.operations import (BlockchainOperation,
                                BlockchainUser,
                                BlockchainService)

from models.common import (uid,
                           addr,
                           pkey)

from services.bids import *

class SubmitBidOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        data: BidCreateDTO
    ):
        super().__init__(service, user)
        self.bid = data

    def execute(self) -> TxReceipt:
        return BidsService.submit_bid(
            self.service,
            self.address,
            self.key,
            self.bid
        )

class RevertBidOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        id: uid
    ):
        super().__init__(service, user)
        self.bid_id = id

    def execute(self) -> TxReceipt:
        return BidsService.revert_bid(
            self.service,
            self.address,
            self.key,
            self.bid_id
        )

class GetBidOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        id: uid
    ):
        super().__init__(service, user)
        self.bid_id = id

    def execute(self) -> TxReceipt:
        return BidsService.get_bid(
            self.service,
            self.bid_id
        )

class GetTenderBidsOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        tender_id: uid
    ):
        super().__init__(service, user)
        self.tender_id = tender_id

    def execute(self) -> TxReceipt:
        return BidsService.get_tender_bids(
            self.service,            
            self.tender_id
        )

class GetUserBidOperation(BlockchainOperation):
    def __init__(
        self,
        service: BlockchainService,
        user: BlockchainUser,
        other_user: BidCreateDTO
    ):
        super().__init__(service, user)
        self.other_user = other_user

    def execute(self) -> TxReceipt:
        return BidsService.get_users_bids(
            self.service,
            self.other_user
        )