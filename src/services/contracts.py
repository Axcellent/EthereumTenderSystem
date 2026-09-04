from services import TxReceipt, BlockchainService

from models.common import (uid,
                           addr,
                           pkey)
from models.contracts_dto import ContractGetFullDTO, ContractGetShortDTO, AcceptingModeDTO

from constants import (OPEN_CONTRACT, 
                       FINANCE_CONTRACT, 
                       HAND_IN_JOB, 
                       ACCEPT_JOB, 
                       GET_TENDER_CONTRACT, 
                       GET_CONTRACT)

class ContractsService():
    @staticmethod
    def open_contract(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        tender_id: uid
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = OPEN_CONTRACT,
            args = [tender_id]
        )

    @staticmethod
    def finance_contract(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        tender_id: uid,
        amount: uid
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = FINANCE_CONTRACT,
            args = [tender_id],
            value = amount         
        )

    @staticmethod
    def hand_in_job(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        tender_id: uid
    ) -> TxReceipt:
        return service.send_tx(
            address_from,
            key,
            function_name = HAND_IN_JOB,
            args = [tender_id]
        )

    @staticmethod
    def review_job(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        mode: AcceptingModeDTO
    ) -> TxReceipt:
        return service.send_tx(
            address_from,
            key,
            function_name=ACCEPT_JOB,
            args=mode.model_dump().values()
        )

    def get_contract_full(
        service: BlockchainService,
        contract_id: uid
    ) -> ContractGetFullDTO:
        data = service.view(
            function_name=GET_CONTRACT,
            args=[contract_id]
        )

        return ContractGetFullDTO(
            contract_id=contract_id,
            tender_id=data[0],
            contractor=data[1],
            owner=data[2],
            amount=data[3],
            started=data[4],
            deadline=data[5],
            last_report_id=data[7],
            status=data[6]
        )


    def get_contract_short(
        service: BlockchainService,
        contract_id: uid
    ) -> ContractGetShortDTO:
        data = service.view(
            function_name=GET_CONTRACT,
            args=[contract_id]
        )

        return ContractGetShortDTO(
            contract_id=contract_id,
            status=data[7]
        )

    def get_tender_contract(
        service: BlockchainService,
        tender_id: uid
    ) -> ContractGetFullDTO:
        contract_id = service.view(
            function_name=GET_TENDER_CONTRACT,
            args=[tender_id]
        )

        data = ContractsService.get_contract_full(
            service,
            contract_id
        )

        return data