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

from api import BlockchainService
from api.tenders import TendersManager
from api.users import UsersManager
from api.bids import BidsManager
from api.contracts import ContractsManager
from api.reports import ReportsManager
from api.reviews import ReviewsManager

from test_data import (existing_users, 
                        users_data,
                        tenders_data,
                        bids_data,
                        GOV,
                        COMP,
                        GOOD_COMP,
                        BAD_COMP,
                        GUY,
                        TENDER,
                        SUBTENDER,
                        BEST_BID,
                        GOOD_BID,
                        LONG_BID,
                        NORMAL_BID,
                        EXPENSIVE_BID
                        )

from tests_common import registered_users, created_tenders, submitted_bids

import time

from constants import *

def test_contract_creating(
    service,
    registered_users,
    created_tenders,
    submitted_bids
):    
    gov: LocalAccount = registered_users(GOV)
    tender: TenderGetFullDTO = created_tenders(TENDER, GOV)

    bad_bid1 : BidGetDTO = submitted_bids(EXPENSIVE_BID, TENDER, BAD_COMP)
    bad_bid2 : BidGetDTO = submitted_bids(LONG_BID, TENDER, GUY)
    bad_bid3 : BidGetDTO = submitted_bids(NORMAL_BID, TENDER, COMP)
    best_bid : BidGetDTO = submitted_bids(BEST_BID, TENDER, GOOD_COMP)

    with pytest.raises(RuntimeError, match="Tender has to be in closed-bidding status"):
        ContractsManager.open_contract(
            service,
            gov.address,
            gov.key,
            best_bid.tender_id
        )



    with pytest.raises(RuntimeError, match="Tender has to be in closed-bidding status"):
        ContractsManager.open_contract(
            service,
            gov.address,
            gov.key,
            best_bid.tender_id
        )

    with pytest.raises(RuntimeError, match="Tender has to be in closed-bidding status"):
        ContractsManager.open_contract(
            service,
            gov.address,
            gov.key,
            best_bid.tender_id
        )

    raise RuntimeError("Here")
    import time
    time.sleep(5)

    TendersManager.close_tender(
        service,
        gov.address,
        gov.key,
        best_bid.tender_id
    )

    

    ContractsManager.open_contract(
        service,
        gov.address,
        gov.key,
        best_bid.tender_id
    )

    with pytest.raises(RuntimeError, match="COCI"):
        ContractsManager.open_contract(
            service,
            gov.address,
            gov.key,
            best_bid.tender_id
        )

    contract: ContractGetFullDTO = ContractsManager.get_contract_full(service, 1)

    assert contract.deadline == best_bid.deadline
    assert contract.amount == best_bid.price
    assert contract.status == ContractStatus.Pending

def test_submit_on_own_tender(
    service,
    registered_users,
    created_tenders,
    bids_data 
):    
    gov: LocalAccount = registered_users(GOV)
    tender: TenderGetFullDTO = created_tenders(TENDER, GOV)    

    with pytest.raises(RuntimeError, match="You are creator of this tender"):
        BidsManager.submit_bid(
            service,
            gov.address,
            gov.key,
            bids_data[EXPENSIVE_BID]
        )