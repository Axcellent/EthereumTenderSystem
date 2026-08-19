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
                        REP_NOT_ACC,
                        REP_NOT_ACC_RESP,
                        REP_ACC,
                        REP_ACC_RESP,
                        REP_FINAL,
                        REP_FINAL_RESP,
                        )

from tests_common import registered_users, created_tenders, opened_contracts, submitted_bids

import time

from constants import *

def test_report_flow(
    service,
    registered_users,
    opened_contracts,
    reports_data
):
    gov: LocalAccount = registered_users(GOV)
    comp: LocalAccount = registered_users(GOOD_COMP)

    owner = gov.address
    contractor = comp.address
    
    contract: ContractGetFullDTO = opened_contracts(BEST_BID, MAIN_TENDER, GOV, GOOD_COMP)
    tender_id = contract.tender_id
    contract_id = contract.contract_id
    
    report_data: ReportGetDTO = reports_data[REP_NOT_ACC]

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
        report_data
    )
    
    reports = ReportsService.get_contract_reports(service, contract_id)
    assert len(reports) == 1
    report = reports[0]
    assert report.description == report_data.description
    assert report.status == DocStatus.Pending
    
    report_counter = service.view('reportCounter')
    report_id = report_counter

    contract = ContractsService.get_contract_full(
        service,
        contract.contract_id
    )
    assert contract.last_report_id == report_id
    
    ReportsService.review_report(
        service,
        owner,
        gov.key,
        report_id,
        False
    )
    
    report_updated = ReportsService.get_report(service, report_id)
    assert report_updated.status == DocStatus.Rejected
    
    with pytest.raises(RuntimeError, match="This report is not pending"):
        ReportsService.review_report(
            service,
            owner,
            gov.key,
            report_id,
            True
        )

    guy: LocalAccount = registered_users(GUY)
    with pytest.raises(RuntimeError, match="You are not the perfomer of contract to create report"):
        ReportsService.create_report(
            service,
            guy.address,
            guy.key,
            report_data
        )
    
    report_data2: ReportGetDTO = reports_data[REP_NOT_ACC_RESP]

    ReportsService.create_report(
        service,
        owner,
        gov.key,
        report_data2
    )
    
    reports = ReportsService.get_contract_reports(service, contract_id)
    assert len(reports) == 2    
    assert any(r.description == report_data2.description for r in reports)

