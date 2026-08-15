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

from tests_common import registered_users, created_tenders

import time

from constants import *

@pytest.mark.parametrize("bid_id, user_id", [(EXPENSIVE_BID, BAD_COMP)])
def test_bid_creating(
    service,
    registered_users,
    created_tenders,
    bids_data,
    bid_id,
    user_id
):    
    comp: LocalAccount = registered_users(user_id)
    tender: TenderGetFullDTO = created_tenders(TENDER, GOV)

    BidsManager.submit_bid(
        service,
        comp.address,
        comp.key,
        bids_data[bid_id]
    )

    with pytest.raises(RuntimeError, match="You have already submitted a bid for this tender"):
        BidsManager.submit_bid(
            service,
            comp.address,
            comp.key,
            bids_data[bid_id]
        )

    bid = BidsManager.get_bid(service, 1)

    assert bid.deadline.timestamp() == bids_data[bid_id].deadline
    assert bid.price == bids_data[bid_id].price
    assert bid.bidder == comp.address

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