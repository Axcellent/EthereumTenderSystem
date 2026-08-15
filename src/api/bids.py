from api import TxReceipt, BlockchainService

from models.common import (addr,
                           uint,
                           pkey)
from models.bids_dto import BidGetDTO, BidCreateDTO

from constants import (SUBMIT_BID,
                       REVERT_BID,
                       GET_TENDER_BIDS,
                       GET_USER_BIDS,
                       GET_BID)

class BidsManager:
    @staticmethod
    def submit_bid(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        bid: BidCreateDTO       
    ) -> TxReceipt:
        return service.send_tx(
            address_from,
            key,
            function_name=SUBMIT_BID,
            args=bid.model_dump().values(),
        )

    @staticmethod
    def revert_bid(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        bid_id: uint
    ) -> TxReceipt:
        return service.send_tx(
            address_from,
            key,
            function_name=REVERT_BID,
            args=[bid_id]
        )

    @staticmethod
    def get_bid(
        service: BlockchainService,
        bid_id: uint
    ) -> BidGetDTO:
        data = service.view(
            function_name=GET_BID,
            args=[bid_id]
        )

        return BidGetDTO(
            tender_id=data[0],
            bidder=data[1],
            price=data[2],
            deadline=data[3],
            is_active=data[4]
        )
    
    @staticmethod
    def get_tender_bids(
        service: BlockchainService,
        tender_id: uint
    ) -> list[BidGetDTO]:

        bids = service.view(GET_TENDER_BIDS, tender_id)

        data = []
        for bid_id in bids:
            data.append(BidsManager.get_bid(
                service,
                bid_id
            ))

        return data

    @staticmethod
    def get_users_bids(
        service: BlockchainService,
        user: addr
    ) -> list[BidGetDTO]:
        bids = service.view(GET_USER_BIDS, user)

        data = []
        for bid_id in bids:
            data.append(BidsManager.get_bid(
                service,
                bid_id
            ))

        return data