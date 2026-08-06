from api import TxReceipt, BlockchainService

from models.common import addr, uint, pkey
from models.bids_dto import BidGetDTO, BidCreateDTO

from constants import SUBMIT_BID, REVERT_BID, GET_TENDER_BIDS, GET_USER_BIDS

class BidManager:
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

    def get_tender_bids(
        service: BlockchainService,
        tender_id: uint
    ) -> list[BidGetDTO]:
        data = service.view(GET_TENDER_BIDS, tender_id)
        return [BidGetDTO(
            tender_id=d[0],
            bidder=d[1],
            price=d[2],
            deadline=d[3],
            is_active=d[4]
        ) for d in data]

    def get_users_bids(
        service: BlockchainService,
        user: addr
    ) -> list[BidGetDTO]:
        data = service.view(GET_USER_BIDS, user)
        return [BidGetDTO(
            tender_id=d[0],
            bidder=d[1],
            price=d[2],
            deadline=d[3],
            is_active=d[4]
        ) for d in data]