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

TENDER = 0
SUBTENDER = 1

EXPENSIVE_BID = 0
LONG_BID = 1
NORMAL_BID = 2
GOOD_BID = 3
BEST_BID = 4

@pytest.fixture(scope="session")
def existing_users():
    return [
        # GOV
        Account.from_key("0x2f6b3993e4d1271501e70fec047edc37dc020ab2189d098a1caf0bcf61ca1087"),
        # COMPANY
        Account.from_key("0xf329e22fee5c8737695393ed710f80f78d7a7abf3338efd6548c09a8669ab056"),
        # COOL COMPANY
        Account.from_key("0x93ac5e84f043607a9eb667ede85edd96bfcf778c10acc2f596cfbcaff641ff4f"),
        # BAD COMPANY
        Account.from_key("0xe277392baec1182f6d8666cb43fe1c2a86e7ebdc1c9eee2173ed8eb66b433862"),
        # SOME GUY
        Account.from_key("0x3a163bc13f1d335ad069b6501e50c6ade36599f5e492b2024bab6b30cb6d7731"),
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
            bidding_deadline =  datetime.datetime.now() + datetime.timedelta(seconds= 5),
            parent_id = 0
        ),
        TenderCreateDTO(
            title = "Subtender for #1",
            description = "Fix all roads in Saint-Petersburg",
            budget = 100_000_000,
            deadline = datetime.datetime.now() + datetime.timedelta(days= 100),
            bidding_deadline =  datetime.datetime.now() + datetime.timedelta(seconds= 5),
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
