from api import TxReceipt, BlockchainService

from pydantic import BaseModel, Field, field_validator, ValidationError

from models.common import uint, addr
from models.contracts_dto import ContractGetFullDTO, ContractGetShortDTO, AcceptingModeDTO

from constants import OPEN_CONTRACT, FINANCE_CONTRACT, HAND_IN_JOB, ACCEPT_JOB

class ContractsManager():
    def open_contract(
        service: BlockchainService,
        address_from: addr,
        key: str,
        tender_id: uint
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = OPEN_CONTRACT,
            args = [tender_id]
        )

    def finance_contract(
        service: BlockchainService,
        address_from: addr,
        key: str,
        tender_id: int
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = FINANCE_CONTRACT,
            args = tender_id,            
        )

    def hand_in_job(
        service: BlockchainService,
        address_from: addr,
        key: str,
        tender_id: int
    ) -> bool:
        return service.send_tx(
            address_from,
            key,
            function_name = HAND_IN_JOB,
            args = tender_id,            
        )