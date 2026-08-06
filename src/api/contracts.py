from api import TxReceipt, BlockchainService

from pydantic import BaseModel, Field, field_validator, ValidationError

from models.common import uint, addr, pkey
from models.contracts_dto import ContractGetFullDTO, ContractGetShortDTO, AcceptingModeDTO

from constants import OPEN_CONTRACT, FINANCE_CONTRACT, HAND_IN_JOB, ACCEPT_JOB

class ContractsManager():
    def open_contract(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
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
        key: pkey,
        tender_id: uint,
        amount: uint
    ) -> TxReceipt:      
        return service.send_tx(
            address_from,
            key,
            function_name = FINANCE_CONTRACT,
            args = [tender_id],
            value = amount         
        )

    def hand_in_job(
        service: BlockchainService,
        address_from: addr,
        key: pkey,
        tender_id: uint
    ) -> TxReceipt:
        return service.send_tx(
            address_from,
            key,
            function_name = HAND_IN_JOB,
            args = [tender_id]
        )

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