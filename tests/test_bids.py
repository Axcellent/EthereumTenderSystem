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

from services.bids import BidsService

from test_data import *
from tests_common import *

from constants import *


@pytest.mark.parametrize(
    "field_name, invalid_value, expected_error_substring",
    [        
        ("tender_id", 0, "Input should be greater than 0"),

        ("price", "a", "Input should be a valid integer"),
        ("price", 0, "Input should be greater than 0"),

        ("deadline", "2025-01-01", "Can receive only datetime.datetime"),
        ("deadline", 1234567890, "Can receive only datetime.datetime"),
        ("deadline", None, "Can receive only datetime.datetime"),
    ]
)
def test_bid_validation(
    bids_data,
    field_name, 
    invalid_value, 
    expected_error_substring
    ):
    data = bids_data[0].model_dump()
    data[field_name] = invalid_value

    with pytest.raises(ValidationError) as exc_info:
        BidCreateDTO(**data)

    assert expected_error_substring in str(exc_info.value)

def test_bid_create_and_get(
    service,
    submitted_bids,
    registered_users,
    bids_data
):    
    comp = registered_users(GOOD_COMP)
    bid = submitted_bids(BEST_BID, MAIN_TENDER, GOOD_COMP)

    assert bid.deadline.timestamp() == bids_data[BEST_BID].deadline
    assert bid.price == bids_data[BEST_BID].price
    assert bid.bidder == comp.address

def test_second_bid(
    service,
    submitted_bids,
    registered_users,
    bids_data
):    
    comp = registered_users(GOOD_COMP)
    bid = submitted_bids(BEST_BID, MAIN_TENDER, GOOD_COMP)

    with pytest.raises(RuntimeError, match="You have already submitted a bid for this tender"):
        submitted_bids(BEST_BID, MAIN_TENDER, GOOD_COMP)        

def test_submit_on_own_tender(
    service,
    registered_users,
    created_tenders,
    submitted_bids,
    bids_data 
):      

    with pytest.raises(RuntimeError, match="You are creator of this tender"):
        submitted_bids(BEST_BID, MAIN_TENDER, GOV)  