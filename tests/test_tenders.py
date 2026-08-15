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
                        GOV,
                        COMP,
                        GOOD_COMP,
                        BAD_COMP,
                        GUY,
                        TENDER,
                        SUBTENDER
                        )

from tests_common import registered_users, created_tenders

import time

from constants import *


def test_tenders_chain(
    service,
    registered_users,
    tenders_data
):
    gov: LocalAccount = registered_users(GOV)
    comp: LocalAccount = registered_users(COMP)

    TendersManager.create_tender(
        service,
        gov.address,
        gov.key,
        tenders_data[TENDER])

    with pytest.raises(RuntimeError, match="Tender is not executing"):
        TendersManager.create_tender(
            service,
            comp.address,
            comp.key,
            tenders_data[SUBTENDER])

    tender = TendersManager.get_tender_full(service, 1)

    assert tender.description == tenders_data[TENDER].description
    assert tender.budget == tenders_data[TENDER].budget
    assert tender.deadline.timestamp() == tenders_data[TENDER].deadline

@pytest.mark.parametrize(
    "field_name, invalid_value, expected_error_substring",
    [        
        ("title", "ab", "String should have at least 3 characters"),
        ("title", "a" * 129, "String should have at most 128 characters"),

        ("description", "a" * 4097, "String should have at most 4096 characters"),

        ("budget", -1, "Input should be greater than 0"),

        ("deadline", "not a datetime", "Not datetime type"),
        ("deadline", 1234567890, "Not datetime type"),
        ("deadline", None, "Not datetime type"),

        ("bidding_deadline", "2025-01-01", "Not datetime type"),
        ("bidding_deadline", 1234567890, "Not datetime type"),
        ("bidding_deadline", None, "Not datetime type"),
    ]
)
def test_create_tender_validation(
    tenders_data,
    field_name, 
    invalid_value, 
    expected_error_substring
    ):
    data = tenders_data[0].model_dump()
    data[field_name] = invalid_value

    with pytest.raises(ValidationError) as exc_info:
        TenderCreateDTO(**data)

    assert expected_error_substring in str(exc_info.value)

