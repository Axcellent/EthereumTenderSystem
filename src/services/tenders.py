from services import TxReceipt, BlockchainService

from models.common import (addr, 
                           uint, 
                           pkey)
from models.tenders_dto import TenderGetFullDTO, TenderGetShortDTO, TenderCreateDTO

from constants import (CREATE_TENDER,
                       CLOSE_TENDER,
                       REVERT_TENDER,
                       GET_TENDER,
                       GET_TENDERS,
                       GET_USERS_TENDERS)

class TendersService():
    @staticmethod
    def create_tender(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        tender_data: TenderCreateDTO
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = CREATE_TENDER,
            args = tender_data.model_dump().values(),
        )

    @staticmethod
    def revert_tender(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        tender_id: uint
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = REVERT_TENDER,
            args = [tender_id]
        )

    @staticmethod
    def close_tender(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        tender_id: uint
    ) -> TxReceipt:
        return service.send_tx(
            address_from,
            key,
            function_name = CLOSE_TENDER,
            args = [tender_id],
            unsafe = True
        )
    
    @staticmethod
    def get_tender_full(
        service: BlockchainService,
        tender_id: uint
    ) -> TenderGetFullDTO:
        data = service.view(GET_TENDER, [tender_id])

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

    @staticmethod
    def get_short_tenders_by_ids(
        service: BlockchainService,
        tenders: list[int],
    ) -> list[TenderGetShortDTO]:
        data: list[TenderGetFullDTO] = []
        for tender_id in tenders:
            data.append(TendersService.get_tender_full(
                service,
                tender_id
            ))

        return [TenderGetShortDTO(
            creator=d.creator,
            title=d.title,
            budget=d.budget,
            deadline=d.deadline,
        ) for d in data]
    
    @staticmethod
    def get_tenders_short(
        service: BlockchainService,
        page: uint,
        count: uint
    ) -> list[TenderGetShortDTO]:
        print('get_tenders_short')   
        tenders_data = service.view(GET_TENDERS, [page, count])
        
        result = []
        for tender in tenders_data:
            result.append(TenderGetShortDTO(
                creator=tender[0],
                title=tender[1],
                budget=tender[3],
                deadline=tender[4],
            ))
        print(result)
        return result

    @staticmethod
    def get_user_tenders(
        service: BlockchainService,
        user: addr
    ) -> list[TenderGetShortDTO]:
        tenders = service.view(GET_USERS_TENDERS, [user])

        return TendersService.get_short_tenders_by_ids(service, tenders)