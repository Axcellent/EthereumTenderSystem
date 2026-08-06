from api import TxReceipt, BlockchainService

from models.common import addr
from models.tenders_dto import TenderGetFullDTO, TenderGetShortDTO, CreateTenderDTO

from constants import CREATE_TENDER, CLOSE_TENDER, REVERT_TENDER, GET_TENDER, GET_TENDERS, GET_USERS_TENDERS

class TendersManager():
    def create_tender(
        service: BlockchainService,
        address_from: addr,
        key: str,
        tender_data: CreateTenderDTO
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = CREATE_TENDER,
            args = tender_data.model_dump().values(),
        )

    def revert_tender(
        service: BlockchainService,
        address_from: addr,
        key: str,
        tender_id: int
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = REVERT_TENDER,
            args = tender_id,            
        )

    def close_tender(
        service: BlockchainService,
        address_from: addr,
        key: str,
        tender_id: int
    ) -> bool:
        return service.send_tx(
            address_from,
            key,
            function_name = CLOSE_TENDER,
            args = tender_id,            
        )
    

    def get_tender_full(
        service: BlockchainService,
        tender_id: int
    ) -> TenderGetFullDTO:
        data = service.view(GET_TENDER, tender_id)

        return TenderGetFullDTO(
            creator=data[0],
            title=data[1],
            description=data[2],
            budget=data[3],
            deadline=data[4],
            bidding_deadline=data[5],
            parent_id=data[7],
            status=data[6]
        )

    def get_tenders_short(
        service: BlockchainService,
        page: int,
        count: int
    ) -> list[TenderGetShortDTO]:
        data = service.view(GET_TENDERS, page, count)

        return [TenderGetShortDTO(
            creator=d[0],
            title=d[1],
            budget=d[3],
            deadline=d[4],
        ) for d in data]

    def get_user_tenders(
        service: BlockchainService,
        user: addr
    ) -> list[TenderGetShortDTO]:
        data = service.view(GET_USERS_TENDERS, user)

        return [TenderGetShortDTO(
            creator=d[0],
            title=d[1],
            budget=d[3],
            deadline=d[4],
        ) for d in data]