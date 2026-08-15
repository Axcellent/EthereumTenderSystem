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

from test_data import existing_users, users_data, tenders_data

@pytest.fixture
def registered_users(
    service: BlockchainService,
    existing_users : list[LocalAccount],
    users_data : list[UserCreateDTO]
    ):
    def _register_user(
            user_id: int,
            use_default: bool = True,
            user_data: Optional[UserCreateDTO] = None
            ) -> LocalAccount:
        exists = False
        try:
            user = UsersManager.get_user_short(service, existing_users[user_id].address)
            exists = True
        except:
            pass

        if not exists:
            UsersManager.register(
                service,
                existing_users[user_id].address,
                existing_users[user_id].key,
                users_data[user_id] if use_default or user_data is None else user_data
                )
        
        return existing_users[user_id]
    return _register_user

@pytest.fixture
def created_tenders(
    service: BlockchainService,
    registered_users : list[LocalAccount],
    tenders_data : list[TenderCreateDTO]
    ):
    def _create_tender(
            tender_no: int,
            user_id: int,
            use_default: bool = True,
            tender_data: Optional[TenderCreateDTO] = None
            ) -> LocalAccount:    

        exists = False
        try:
            tender = TendersManager.get_tender_full(service, tender_no + 1)
            exists = True
        except:
            pass

        if not exists:
            user = registered_users(user_id)
            TendersManager.create_tender(
                service,
                user.address,
                user.key,
                tenders_data[tender_no] if use_default or tender_data == None else tender_data
                )
            
        return TendersManager.get_tender_full(service, tender_no + 1)
    return _create_tender

@pytest.fixture
def submitted_bids(
    service: BlockchainService,
    registered_users : list[LocalAccount],
    created_tenders : list[TenderCreateDTO],
    bids_data : list[BidCreateDTO]
    ):
    def _create_bid(
            bid_no: int,
            tender_id: int,
            user_id: int,
            use_default: bool = True,
            bid_data: Optional[BidCreateDTO] = None
            ) -> LocalAccount:
        user = registered_users(user_id)
        tender = created_tenders(tender_id, user_id)

        if use_default or bid_data is None:
            bid_data = bids_data[bid_no]
            bid_data.tender_id = tender_id + 1

        BidsManager.submit_bid(
            service,
            user.address,
            user.key,
            bid_data
            )
        return BidsManager.get_bid(service, BlockchainService.view(service, "bidCounter"))
    return _create_bid