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
                        GOV,
                        COMP,
                        GOOD_COMP,
                        BAD_COMP,
                        GUY
                        )

from tests_common import registered_users

import time

from constants import *

@pytest.mark.parametrize(
    "field_name, invalid_value, expected_error_substring",
    [
        ("title", "ab", "String should have at least 3 characters"),
        ("title", "ab" * 65, "String should have at most 128 characters"),

        ("telephones", "+7 (999) 999-99-99", "Uncorrect input format (expected array)"),
        ("telephones", ["123456"], "need +7 (xxx) xxx-xx-xx or 8xxxxxxxxxx"),
        ("telephones", ["+7 (999) 999 99 99"], "need +7 (xxx) xxx-xx-xx or 8xxxxxxxxxx"),
        ("telephones", ["8999999999"], "need +7 (xxx) xxx-xx-xx or 8xxxxxxxxxx"),
        ("telephones", ["+7 (999) 999-99-99"] * 6, "Too many telephones"),     

        ("emails", "valid-12dom@mail.ru", "Uncorrect input format (expected array)"),
        ("emails", ["invalid-12dom@12mail.ru"], "need your-email@some-domain.only-ru"),
        ("emails", ["invalid-12dom@mail.com"], "need your-email@some-domain.only-ru"),

        ("cities", "Moscow", "Uncorrect input format (expected array)"),
        ("cities", ["Moscow123"], "need Rostov-On-Don like"),
        ("cities", ["Moscow!"], "need Rostov-On-Don like"),    
    ]
)
def test_user_create_validation(
    users_data,
    field_name,
    invalid_value,
    expected_error_substring
    ):
    data = users_data[0].model_dump()
    data[field_name] = invalid_value

    with pytest.raises(ValidationError) as excinfo:
        UserCreateDTO(**data)

    assert expected_error_substring in str(excinfo.value)

@pytest.mark.parametrize("user_no", [0,4])
def test_user_register(
    service, 
    existing_users: list[LocalAccount], 
    users_data: list[UserCreateDTO], 
    user_no
    ):
    UsersService.register(
        service,
        existing_users[user_no].address,
        existing_users[user_no].key,
        users_data[user_no]
    )

    registered_user = UsersService.get_user_full(service, existing_users[user_no].address)

    assert users_data[user_no].title == registered_user.title
    assert users_data[user_no].description == registered_user.description
    assert users_data[user_no].telephones == ', '.join(registered_user.telephones)
    assert users_data[user_no].cities == ', '.join(registered_user.cities)
    assert users_data[user_no].emails ==', '.join(registered_user.emails)

def test_user_duplicate_register(
    service, 
    existing_users: list[LocalAccount], 
    users_data: list[UserCreateDTO], 
    ):
    UsersService.register(
        service,
        existing_users[0].address,
        existing_users[0].key,
        users_data[0]
    )

    with pytest.raises(RuntimeError):
        UsersService.register(
            service,
            existing_users[0].address,
            existing_users[0].key,
            users_data[0]
        )

def test_get_reputation(
    service,    
    registered_users
):
    gov: LocalAccount = registered_users(GOV)
    rep = UsersService.get_reputation(service, gov.address)
    assert rep == 0

def test_ban_user(
    service,    
    registered_users,
    existing_users
):
    # test not registered
    gov: LocalAccount = registered_users(GOV)
    guy: LocalAccount = existing_users[GUY]
    with pytest.raises(RuntimeError, match="User is not active"):
            UsersService.ban_user(
                service,
                gov.address,
                gov.key,
                guy.address,
                "Bad words"
            )

    # test not moderator    
    guy: LocalAccount = registered_users(GUY)
    with pytest.raises(RuntimeError, match="Permition denied"):
            UsersService.ban_user(
                service,
                guy.address,
                guy.key,
                gov.address,
                "Bad words"
            )

    # test OK
    tx_receipt = UsersService.ban_user(
        service,
        gov.address,
        gov.key,
        guy.address,
        "Bad words"
    )

    event = service.contract.events.UserBanned()
    event_args = event.process_receipt(tx_receipt)[0]['args']
    
    assert event_args['id'] == guy.address
    assert event_args['reason'] == "Bad words"

    user = UsersService.get_user_short(service, guy.address)
    assert user.status == UserStatus.Banned

    # test duplicate ban
    with pytest.raises(RuntimeError, match="User is not active"):
        UsersService.ban_user(
            service,
            gov.address,
            gov.key,
            guy.address,
            "Bad words"
        )

def test_delete_user(
    service,    
    registered_users,
    existing_users
):
    # test not registered
    gov: LocalAccount = registered_users(GOV)
    guy: LocalAccount = existing_users[GUY]
    with pytest.raises(RuntimeError, match="User is not in system"):
            UsersService.delete_user(
                service,
                gov.address,
                gov.key,
                guy.address,
                "Bad words"
            )

    # test not moderator    
    guy: LocalAccount = registered_users(GUY)
    with pytest.raises(RuntimeError, match="Permition denied"):
            UsersService.delete_user(
                service,
                guy.address,
                guy.key,
                gov.address,
                "Bad words"
            )

    # test OK
    tx_receipt = UsersService.delete_user(
        service,
        gov.address,
        gov.key,
        guy.address,
        "Bad words"
    )

    event = service.contract.events.UserDeleted()
    event_args = event.process_receipt(tx_receipt)[0]['args']
    
    assert event_args['id'] == guy.address
    assert event_args['reason'] == "Bad words"

    user = UsersService.get_user_short(service, guy.address)
    assert user.status == UserStatus.Deleted

    # test duplicate delete
    with pytest.raises(RuntimeError, match="User is not in system"):
        UsersService.delete_user(
            service,
            gov.address,
            gov.key,
            guy.address,
            "Bad words"
        )


def test_ban_and_unban_user(
    service,    
    registered_users,
    existing_users
):
    # test not registered
    gov: LocalAccount = registered_users(GOV)
    guy: LocalAccount = existing_users[GUY]
    with pytest.raises(RuntimeError, match="User is not banned"):
            UsersService.unban_user(
                service,
                gov.address,
                gov.key,
                guy.address,
                "forgiven"
            )

    # test not moderator    
    guy: LocalAccount = registered_users(GUY)
    with pytest.raises(RuntimeError, match="Permition denied"):
            UsersService.unban_user(
                service,
                guy.address,
                guy.key,
                gov.address,
                "forgiven"
            )

    UsersService.ban_user(
        service,
        gov.address,
        gov.key,
        guy.address,
        "Bad words"
    )

    # test OK
    tx_receipt = UsersService.unban_user(
        service,
        gov.address,
        gov.key,
        guy.address,
        "forgiven"
    )

    event = service.contract.events.UserUnbanned()
    event_args = event.process_receipt(tx_receipt)[0]['args']
    
    assert event_args['id'] == guy.address
    assert event_args['reason'] == "forgiven"

    user = UsersService.get_user_short(service, guy.address)
    assert user.status == UserStatus.Active

    # test duplicate unaban
    with pytest.raises(RuntimeError, match="User is not banned"):
        UsersService.unban_user(
            service,
            gov.address,
            gov.key,
            guy.address,
            "forgiven"
        )

    with pytest.raises(RuntimeError, match="User is not banned"):
        UsersService.unban_user(
            service,
            gov.address,
            gov.key,
            guy.address,
            "forgiven"
        )