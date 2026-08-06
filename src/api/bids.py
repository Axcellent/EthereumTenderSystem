from api import TxReceipt, BlockchainService

from models.common import addr
from models.bids_dto import BidGetDTO, BidCreateDTO

class BidManager:
    def submit_bid(
        service: BlockchainService,
        address_from: addr,
        key: str,
        bid: BidCreateDTO       
    ) -> TxReceipt:
        return service.send_tx(
            address_from,
            key,
            function_name="submitBid",
            args=bid.model_dump().values(),
        )

    def revert_bid(
            service: BlockchainService,
            address_from: addr,
            key: str,
            bid_id: int
        ) -> TxReceipt:
            return service.send_tx(
                address_from,
                key,
                function_name="withdrawBid",
                args=[bid_id]
            )

    def get_tender_bids(
        service: BlockchainService,
        tender_id: int
    ) -> list[BidGetDTO]:
        data = service.view("getTenderBids", tender_id)
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
        data = service.view("getUsersBids", user)
        return [BidGetDTO(
            tender_id=d[0],
            bidder=d[1],
            price=d[2],
            deadline=d[3],
            is_active=d[4]
        ) for d in data]