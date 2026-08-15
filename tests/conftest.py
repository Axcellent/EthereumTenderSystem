import pytest
from web3 import Web3
from eth_account import Account
from eth_account.account import LocalAccount
from typing import Optional
from api import BlockchainService

@pytest.fixture(autouse=True)
def reset_blockchain(service):
    snapshot_id = service.web3.provider.make_request('evm_snapshot', [])['result']
    yield  
    service.web3.provider.make_request('evm_revert', [snapshot_id])

@pytest.fixture(scope="session")
def provider_url():
    return "http://127.0.0.1:7545"

@pytest.fixture(scope="session")
def contract_address():
    return "0x675fF4a6C7D0a3C26BB38c697854a40953912EBe"

@pytest.fixture(scope="session")
def abi_file():
    return "src/abi.json"

@pytest.fixture(scope="session")
def service(provider_url, contract_address, abi_file):
    return BlockchainService(provider_url, contract_address, abi_file)