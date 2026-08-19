import pytest
from web3 import Web3
from eth_account import Account
from eth_account.account import LocalAccount
from typing import Optional

from models.common import *
from models.tenders_dto import *
from models.users_dto import *
from models.bids_dto import *
from models.contracts_dto import *
from models.reports_dto import *
from models.reviews_dto import *

from services import BlockchainService
from services.tenders import TendersService
from services.users import UsersService
from services.bids import BidsService
from services.contracts import ContractsService
from services.reports import ReportsService
from services.reviews import ReviewsService

from test_data import (existing_users, 
                        users_data,
                        tenders_data,
                        bids_data,
                        reports_data,
                        GOV,
                        COMP,
                        GOOD_COMP,
                        BAD_COMP,
                        GUY,
                        MAIN_TENDER,
                        SUBTENDER,
                        BEST_BID,
                        GOOD_BID,
                        LONG_BID,
                        NORMAL_BID,
                        EXPENSIVE_BID,
                        REP_FINAL
                        )

from tests_common import registered_users, created_tenders, submitted_bids, opened_contracts

import time

from constants import *

def test_contract_creating(
    service,
    registered_users,
    created_tenders,
    submitted_bids
):    
    gov: LocalAccount = registered_users(GOV)
    tender: TenderGetFullDTO = created_tenders(MAIN_TENDER, GOV)

    bad_bid1 : BidGetDTO = submitted_bids(EXPENSIVE_BID, MAIN_TENDER, BAD_COMP)
    bad_bid2 : BidGetDTO = submitted_bids(LONG_BID, MAIN_TENDER, GUY)
    bad_bid3 : BidGetDTO = submitted_bids(NORMAL_BID, MAIN_TENDER, COMP)
    best_bid : BidGetDTO = submitted_bids(BEST_BID, MAIN_TENDER, GOOD_COMP)

    with pytest.raises(RuntimeError, match="Tender has to be in closed-bidding status"):
        ContractsService.open_contract(
            service,
            gov.address,
            gov.key,
            best_bid.tender_id
        )

    import time
    time.sleep(5)

    TendersService.close_tender(
        service,
        gov.address,
        gov.key,
        best_bid.tender_id
    )

    ContractsService.open_contract(
        service,
        gov.address,
        gov.key,
        best_bid.tender_id
    )

    with pytest.raises(RuntimeError, match="Tender has to be in closed-bidding status"):
        ContractsService.open_contract(
            service,
            gov.address,
            gov.key,
            best_bid.tender_id
        )

    contract: ContractGetFullDTO = ContractsService.get_contract_full(service, 1)

    assert contract.deadline == best_bid.deadline
    assert contract.amount == best_bid.price
    assert contract.status == ContractStatus.Pending
    assert contract.tender_id == best_bid.tender_id

def test_finance_contract(
    service,
    registered_users,
    opened_contracts
):
    gov: LocalAccount = registered_users(GOV)    
    comp: LocalAccount = registered_users(COMP)
    contract: ContractGetFullDTO = opened_contracts(BEST_BID, MAIN_TENDER, GOV, COMP)

    with pytest.raises(RuntimeError, match="Only tender creator can do this"):
        ContractsService.finance_contract(
            service,
            comp.address,
            comp.key,
            contract.tender_id,
            contract.amount
        )

    assert contract.status == ContractStatus.Pending    

    ContractsService.finance_contract(
        service,
        gov.address,
        gov.key,
        contract.tender_id,
        contract.amount
    )

    contract = ContractsService.get_contract_full(service, contract.contract_id)

    assert contract.status == ContractStatus.Executing    

def test_complete_job(
    service,
    registered_users,    
    opened_contracts,
    reports_data
):
    gov: LocalAccount = registered_users(GOV)    
    comp: LocalAccount = registered_users(GOOD_COMP)
    guy: LocalAccount = registered_users(GUY)
    contract: ContractGetFullDTO = opened_contracts(BEST_BID, MAIN_TENDER, GOV, GOOD_COMP)

    ContractsService.finance_contract(
        service,
        gov.address,
        gov.key,
        contract.tender_id,
        contract.amount
    )

    ReportsService.create_report(
        service,
        comp.address,
        comp.key,
        reports_data[REP_FINAL]
    )

    with pytest.raises(RuntimeError, match="You are not contractor of this contract"):
        ContractsService.hand_in_job(
            service,
            guy.address,
            guy.key,
            contract.tender_id
        )    

    ContractsService.hand_in_job(
        service,
        comp.address,
        comp.key,
        contract.tender_id
    )

    contract = ContractsService.get_contract_full(service, contract.contract_id)
    tender = TendersService.get_tender_full(service, contract.tender_id)

    assert contract.status == ContractStatus.Finished
    assert tender.status == TenderStatus.Executing

def test_accept_job(
    service,
    registered_users,    
    opened_contracts,
    reports_data
):
    gov: LocalAccount = registered_users(GOV)    
    comp: LocalAccount = registered_users(GOOD_COMP)
    guy: LocalAccount = registered_users(GUY)
    contract: ContractGetFullDTO = opened_contracts(BEST_BID, MAIN_TENDER, GOV, GOOD_COMP)

    ContractsService.finance_contract(
        service,
        gov.address,
        gov.key,
        contract.tender_id,
        contract.amount
    )

    ReportsService.create_report(
        service,
        comp.address,
        comp.key,
        reports_data[REP_FINAL]
    )

    with pytest.raises(RuntimeError, match="You are not contractor of this contract"):
        ContractsService.hand_in_job(
            service,
            guy.address,
            guy.key,
            contract.tender_id
        )    

    ContractsService.hand_in_job(
        service,
        comp.address,
        comp.key,
        contract.tender_id
    )

    ContractsService.review_job(
        service,
        gov.address,
        gov.key,
        AcceptingModeDTO(
            tender_id=contract.tender_id,
            acceptance=False,
            strict=False
        ))

    contract = ContractsService.get_contract_full(service, contract.contract_id)
    tender = TendersService.get_tender_full(service, contract.tender_id)

    assert contract.status == ContractStatus.Executing
    assert tender.status == TenderStatus.Executing

    ContractsService.hand_in_job(
        service,
        comp.address,
        comp.key,
        contract.tender_id
    )
    
    contract = ContractsService.get_contract_full(service, contract.contract_id)
    tender = TendersService.get_tender_full(service, contract.tender_id)

    assert contract.status == ContractStatus.Finished
    assert tender.status == TenderStatus.Executing

    ContractsService.review_job(
        service,
        gov.address,
        gov.key,
        AcceptingModeDTO(
            tender_id=contract.tender_id,
            acceptance=True,
            strict=False
        ))

    with pytest.raises(RuntimeError, match="This tender is not executing"):
        ContractsService.review_job(
            service,
            gov.address,
            gov.key,
            AcceptingModeDTO(
                tender_id=contract.tender_id,
                acceptance=False,
                strict=False
            ))

    contract = ContractsService.get_contract_full(service, contract.contract_id)
    tender = TendersService.get_tender_full(service, contract.tender_id)

    assert contract.status == ContractStatus.Completed
    assert tender.status == TenderStatus.Completed

