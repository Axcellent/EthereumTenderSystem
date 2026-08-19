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


GOV = 0
COMP = 1
GOOD_COMP = 2
BAD_COMP = 3
GUY = 4

MAIN_TENDER = 0
SUBTENDER = 1

EXPENSIVE_BID = 0
LONG_BID = 1
NORMAL_BID = 2
GOOD_BID = 3
BEST_BID = 4

REP_NOT_ACC = 0
REP_NOT_ACC_RESP = 1
REP_ACC = 2
REP_ACC_RESP = 3
REP_FINAL = 4
REP_FINAL_RESP = 5

@pytest.fixture(scope="session")
def existing_users():
    return [
        # GOV
        Account.from_key("0xbe4dcea404c36f180fa674dfdcdc2d110b91d6c279be2ba5049f9acf49afdc56"),
        # COMPANY
        Account.from_key("0x95b55973fd26e1d3bd180090115f1e0b3713ee0de39dd9b662f3ff57910e58e5"),
        # COOL COMPANY
        Account.from_key("0x55755a7e51ddf27a69141cb4bc66c65f0699a396859ff159f7bdc5637e7cf7eb"),
        # BAD COMPANY
        Account.from_key("0x06edbe7914611d36d959b3126af9b5651b4e57f133c5ac9c5feca4297152f87a"),
        # SOME GUY
        Account.from_key("0xdab74da3a95d08be2ec482e41456576b2a746706d8662576b3b7102953c65f2f"),
    ]

@pytest.fixture(scope="function")
def users_data() -> list[UserCreateDTO]:
    return [
        UserCreateDTO(
            title= "Government",
            description= "Russian Federation",
            cities= ["Moscow", "Saint-Petersburg"],
            telephones= ["+7 (900) 000-00-00"],
            emails= ["gov@gov.ru"]
        ),
        UserCreateDTO(
            title= "Stroy Podryad",
            description= "Not expensive. Every type of job",
            cities= ["Novosibirsk", "Saint-Petersburg"],
            telephones= ["89281074515"],
            emails= ["alferov@mail.ru"]
        ),
        UserCreateDTO(
            title= "OOO OOO",
            description= "Russian Federation",
            cities= ["Rostov-On-Don", "Saint-Petersburg"],
            telephones= ["+7 (928) 628-58-21", "+7 (938) 105-29-16"],
            emails= ["ooo@ooo.ru"]
        ),
        UserCreateDTO(
            title= "OAO AOA",
            description= "We need your money",
            cities= ["Moscow", "Saint-Petersburg"],
            telephones= ["+7 (928) 506-20-12"],
            emails= ["aoa@mail.ru", "aaa@mail.ru"]
        ),
        UserCreateDTO(
            title= "Denis Koghemyatko",
            description= "Chill guy",
            cities= ["Vladimir"],
            telephones= ["+7 (915) 147-22-09"],
            emails= ["dkghmtk@yandex.ru"]
        )
    ]


@pytest.fixture(scope="function")
def tenders_data() -> list[TenderCreateDTO]:
    import datetime
    return [
        TenderCreateDTO(
            title = "Big Tender",
            description = "Fix all roads in Russia",
            budget = 1_000_000_000,
            deadline = datetime.datetime.now() + datetime.timedelta(days= 1000),
            bidding_deadline =  datetime.datetime.now() + datetime.timedelta(seconds= 4),
            parent_id = 0
        ),
        TenderCreateDTO(
            title = "Subtender for #1",
            description = "Fix all roads in Saint-Petersburg",
            budget = 100_000_000,
            deadline = datetime.datetime.now() + datetime.timedelta(days= 100),
            bidding_deadline =  datetime.datetime.now() + datetime.timedelta(seconds= 4),
            parent_id = 1
        )
    ]

@pytest.fixture(scope="function")
def bids_data() -> list[BidCreateDTO]:
    import datetime
    return [
        BidCreateDTO(
            tender_id = 1,
            price = 1_000_000_000,
            deadline = datetime.datetime.now() + datetime.timedelta(days= 50),
        ),
        BidCreateDTO(
            tender_id = 1,
            price = 2_000_000,
            deadline = datetime.datetime.now() + datetime.timedelta(days= 1000),
        ),
        BidCreateDTO(
            tender_id = 1,
            price = 500_000_000,
            deadline = datetime.datetime.now() + datetime.timedelta(days= 500),
        ),
        BidCreateDTO(
            tender_id = 1,
            price = 200_000_000,
            deadline = datetime.datetime.now() + datetime.timedelta(days= 500),
        ),
        BidCreateDTO(
            tender_id = 1,
            price = 1_000_000,
            deadline = datetime.datetime.now() + datetime.timedelta(days= 100),
        ),
    ]

@pytest.fixture()
def reports_data():
    return [
        ReportCreateDTO(
            tender_id=1,
            description="We have done half of work! Photos are on: https://somesite.com",
            response=False
        ),
        ReportCreateDTO(
            tender_id=1,
            description="Nah, thats bad, remake part 2.4, 2.5, 3.1-3.5",
            response=True
        ),
        ReportCreateDTO(
            tender_id=1,
            description="Did that better! Check on prev link",
            response=False
        ),
        ReportCreateDTO(
            tender_id=1,
            description="Good! Waiting for another part",
            response=True
        ),
        ReportCreateDTO(
            tender_id=1,
            description="All done! We tried our best, check on https://somesite.com and ipfs://29safh30op12",
            response=False
        ),
        ReportCreateDTO(
            tender_id=1,
            description="Very good!! Thank you for all you've done!",
            response=True
        ),
    ]